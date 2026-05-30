<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="report-header">
          <span>📦 库存报表</span>
          <div class="report-actions">
            <el-select v-model="warehouseId" placeholder="仓库" clearable size="small" style="width:160px;"><el-option v-for="w in warehouses" :key="w.id" :label="w.name" :value="w.id" /></el-select>
            <el-select v-model="categoryId" placeholder="分类" clearable size="small" style="width:160px;"><el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" /></el-select>
            <el-button type="primary" size="small" @click="fetchData">查询</el-button>
            <el-button size="small" @click="exportData">导出CSV</el-button>
          </div>
        </div>
      </template>
      <el-row :gutter="16" style="margin-bottom:16px;">
        <el-col :span="12"><div class="stat-card"><h4>商品种类</h4><div class="stat-value">{{data.total_items}}</div></div></el-col>
        <el-col :span="12"><div class="stat-card"><h4>总库存量</h4><div class="stat-value">{{data.total_quantity}}</div></div></el-col>
      </el-row>
      <el-table :data="data.details||[]" border stripe max-height="450">
        <el-table-column prop="goods_code" label="商品编码" width="140" />
        <el-table-column prop="goods_name" label="商品名称" min-width="160" />
        <el-table-column prop="warehouse_name" label="仓库" width="120" />
        <el-table-column prop="bin_code" label="库位" width="100" />
        <el-table-column prop="quantity" label="数量" width="100" align="right" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { reportApi } from '@/api/report'
import { warehouseApi } from '@/api/warehouse'
import { categoryApi } from '@/api/goods'
import { exportCSV } from '@/utils'

const warehouseId=ref(''),categoryId=ref('')
const warehouses=ref<any[]>([]),categories=ref<any[]>([])
const data=ref<any>({total_items:0,total_quantity:0,details:[]})

async function fetchData(){
  const params:any={}
  if(warehouseId.value)params.warehouse_id=warehouseId.value
  if(categoryId.value)params.category_id=categoryId.value
  const res:any=await reportApi.inventory(params)
  if(res.code===200)data.value=res.data
}

function exportData(){
  const details=data.value.details||[]
  exportCSV('库存报表',['商品编码','商品名称','仓库','库位','数量'],
    details.map((d:any)=>[d.goods_code,d.goods_name,d.warehouse_name,d.bin_code,d.quantity]))
}

onMounted(async()=>{
  const[wRes,cRes]=await Promise.all([warehouseApi.simple(),categoryApi.tree()])
  warehouses.value=wRes?.data||[]
  const flatten=(nodes:any[]):any[]=>{let r:any[]=[];for(const n of nodes){r.push(n);if(n.children)r=r.concat(flatten(n.children))}return r}
  categories.value=flatten(cRes?.data||[])
  fetchData()
})
</script>

<style lang="scss" scoped>
.report-header{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;}
.report-actions{display:flex;gap:8px;align-items:center;flex-wrap:wrap;}
</style>
