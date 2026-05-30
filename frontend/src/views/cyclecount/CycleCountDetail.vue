<template>
  <div class="page-container" v-loading="loading">
    <el-page-header @back="$router.back()" :content="`盘点单 — ${detail.count_no||''}`" />
    <el-card style="margin-top:16px;" v-if="detail.id">
      <el-descriptions :column="3" border>
        <el-descriptions-item label="盘点单号">{{detail.count_no}}</el-descriptions-item>
        <el-descriptions-item label="仓库">{{detail.warehouse_name}}</el-descriptions-item>
        <el-descriptions-item label="状态"><el-tag :type="statusType(detail.status)">{{detail.status_display}}</el-tag></el-descriptions-item>
        <el-descriptions-item label="操作人">{{detail.operator_name}}</el-descriptions-item>
        <el-descriptions-item label="盘点项数">{{detail.total_items}}</el-descriptions-item>
        <el-descriptions-item label="差异项">{{detail.diff_items}}</el-descriptions-item>
      </el-descriptions>

      <el-divider>盘点明细</el-divider>
      <div v-if="detail.status===1" style="text-align:center;padding:40px;">
        <p style="color:#909399;margin-bottom:16px;">盘点尚未开始，点击下方按钮生成盘点记录</p>
        <el-button type="primary" @click="doStart">开始盘点</el-button>
      </div>

      <template v-else-if="detail.status===2">
        <div style="margin-bottom:12px;display:flex;gap:12px;">
          <el-input v-model="searchText" placeholder="搜索商品..." clearable style="width:240px;" />
          <el-tag type="warning">盘点中 — 请录入实盘数量</el-tag>
        </div>
        <el-table :data="filteredRecords" border stripe max-height="500">
          <el-table-column type="index" label="序号" width="60" />
          <el-table-column prop="goods_code" label="商品编码" width="140" />
          <el-table-column prop="goods_name" label="商品名称" min-width="160" />
          <el-table-column prop="bin_code" label="库位" width="110" />
          <el-table-column prop="system_quantity" label="系统数量" width="110" align="right" />
          <el-table-column label="实盘数量" width="160" align="center">
            <template #default="{row,$index}">
              <el-input-number v-model="actualQtys[$index]" :min="0" :precision="2" size="small" style="width:140px;" />
            </template>
          </el-table-column>
          <el-table-column label="差异" width="100" align="right">
            <template #default="{row,$index}">
              <span :style="{color:(actualQtys[$index]||0)-row.system_quantity!==0?'var(--color-danger)':''}">
                {{((actualQtys[$index]||0)-row.system_quantity).toFixed(2)}}
              </span>
            </template>
          </el-table-column>
        </el-table>
        <div style="margin-top:16px;display:flex;justify-content:space-between;">
          <span>差异项: {{diffCount}} / {{detail.records?.length||0}}</span>
          <el-button type="primary" :loading="completing" @click="doComplete">完成盘点</el-button>
        </div>
      </template>

      <template v-else>
        <el-table :data="detail.records||[]" border stripe max-height="500">
          <el-table-column type="index" label="序号" width="60" />
          <el-table-column prop="goods_code" label="商品编码" width="140" />
          <el-table-column prop="goods_name" label="商品名称" />
          <el-table-column prop="bin_code" label="库位" width="110" />
          <el-table-column prop="system_quantity" label="系统数量" width="110" align="right" />
          <el-table-column prop="actual_quantity" label="实盘数量" width="110" align="right" />
          <el-table-column label="差异" width="110" align="right">
            <template #default="{row}">
              <span :style="{color:row.difference!==0?'var(--color-danger)':''}">{{row.difference}}</span>
            </template>
          </el-table-column>
          <el-table-column prop="counter_name" label="盘点人" width="100" />
        </el-table>

        <div style="margin-top:16px;text-align:right;" v-if="detail.status===3">
          <el-button type="warning" @click="doAdjust">调整库存 ({{detail.diff_items}}项差异)</el-button>
        </div>
      </template>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref,computed,onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage,ElMessageBox } from 'element-plus'
import { cycleCountApi } from '@/api/cyclecount'

const route=useRoute()
const loading=ref(false),completing=ref(false)
const detail=ref<any>({})
const actualQtys=ref<number[]>([])
const searchText=ref('')

const filteredRecords = computed(() => {
  const records = detail.value.records || []
  if (!searchText.value) return records
  const kw = searchText.value.toLowerCase()
  return records.filter((r:any) => r.goods_code?.toLowerCase().includes(kw) || r.goods_name?.toLowerCase().includes(kw) || r.bin_code?.toLowerCase().includes(kw))
})

const diffCount = computed(() => {
  return (detail.value.records||[]).filter((r:any,i:number) => ((actualQtys.value[i]||0) - r.system_quantity) !== 0).length
})

type TagType = 'primary' | 'success' | 'warning' | 'info' | 'danger'
function statusType(s:number): TagType { const m: Record<number,TagType> = {1:'info',2:'warning',3:'primary',4:'success'}; return m[s] || 'info' }

async function fetch(){
  loading.value=true
  try{
    const res:any=await cycleCountApi.detail(route.params.id as string)
    if(res.code===200){
      detail.value=res.data
      actualQtys.value=(res.data.records||[]).map((r:any)=>r.actual_quantity||r.system_quantity||0)
    }
  }finally{loading.value=false}
}

async function doStart(){
  await cycleCountApi.start(detail.value.id)
  ElMessage.success('盘点已开始')
  fetch()
}

async function doComplete(){
  if(detail.value.records.length===0){ElMessage.warning('没有盘点记录');return}
  await ElMessageBox.confirm('确认完成盘点? 完成后将无法修改实盘数量。','确认',{type:'warning'})
  completing.value=true
  try{
    const entries = detail.value.records.map((r:any,i:number)=>({record_id:r.id,actual_quantity:(actualQtys.value[i]||0).toString()}))
    await cycleCountApi.complete(detail.value.id,{entries})
    ElMessage.success('盘点已完成')
    fetch()
  }finally{completing.value=false}
}

async function doAdjust(){
  const diffItems = detail.value.diff_items||0
  await ElMessageBox.confirm(`确定根据盘点结果调整库存? 将调整${diffItems}项差异。`,'确认调整',{type:'warning'})
  await cycleCountApi.adjust(detail.value.id)
  ElMessage.success('库存已调整')
  fetch()
}

onMounted(fetch)
</script>
