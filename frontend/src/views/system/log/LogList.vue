<template>
  <div class="page-container">
    <div class="search-bar">
      <el-select v-model="filters.action" placeholder="操作类型" clearable style="width:140px;">
        <el-option label="创建" value="CREATE" /><el-option label="更新" value="UPDATE" /><el-option label="删除" value="DELETE" /><el-option label="登录" value="LOGIN" /><el-option label="登出" value="LOGOUT" />
      </el-select>
      <el-select v-model="filters.module" placeholder="操作模块" clearable style="width:140px;">
        <el-option label="认证" value="认证" /><el-option label="用户" value="用户" /><el-option label="商品" value="商品" /><el-option label="入库" value="入库" /><el-option label="出库" value="出库" /><el-option label="库存" value="库存" />
      </el-select>
      <el-input v-model="search" placeholder="搜索用户/详情..." clearable style="width:200px;" />
      <el-button type="primary" @click="fetchData">查询</el-button>
      <el-button @click="exportData">导出CSV</el-button>
    </div>
    <div class="table-panel">
      <el-table v-loading="loading" :data="list" stripe border>
        <el-table-column prop="username" label="操作人" width="120" />
        <el-table-column label="类型" width="90">
          <template #default="{row}"><el-tag :type="actionTag(row.action)" size="small">{{row.action}}</el-tag></template>
        </el-table-column>
        <el-table-column prop="module" label="模块" width="100" />
        <el-table-column prop="detail" label="详情" min-width="200" show-overflow-tooltip />
        <el-table-column prop="ip_address" label="IP地址" width="140" />
        <el-table-column prop="created_at" label="时间" width="180">
          <template #default="{row}">{{formatTime(row.created_at)}}</template>
        </el-table-column>
      </el-table>
      <div style="margin-top:16px;display:flex;justify-content:flex-end;">
        <el-pagination v-model:current-page="page" v-model:page-size="pageSize" :total="total" :page-sizes="[10,20,50]" layout="total,sizes,prev,pager,next" @change="fetchData" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref,reactive,onMounted } from 'vue'
import { logApi } from '@/api/system'
import { exportCSV } from '@/utils'

const loading=ref(false),list=ref<any[]>([]),page=ref(1),pageSize=ref(20),total=ref(0),search=ref('')
const filters=reactive({action:null as string|null,module:null as string|null})

type TagType = 'primary' | 'success' | 'warning' | 'info' | 'danger'
function actionTag(a:string): TagType { const m: Record<string,TagType> = {CREATE:'info',UPDATE:'warning',DELETE:'danger',LOGIN:'success',LOGOUT:'info'}; return m[a] || 'info' }
function formatTime(t:string){return t ? new Date(t).toLocaleString('zh-CN',{hour12:false}) : ''}

async function fetchData(){
  loading.value=true
  try{
    const params:any={page:page.value,page_size:pageSize.value}
    if(filters.action)params.action=filters.action
    if(filters.module)params.module=filters.module
    if(search.value)params.search=search.value
    const res:any=await logApi.list(params)
    if(res.code===200){list.value=res.data;total.value=res.meta?.total||0}
  }finally{loading.value=false}
}

function exportData(){
  exportCSV('操作日志',['操作人','操作类型','模块','详情','IP地址','时间'],
    list.value.map(l=>[l.username,l.action,l.module,l.detail||'',l.ip_address||'',formatTime(l.created_at)]))
}

onMounted(fetchData)
</script>
