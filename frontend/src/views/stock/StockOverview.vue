<template>
  <div class="page-container">
    <div class="search-bar"><el-select v-model="filters.warehouse_id" placeholder="仓库" clearable style="width:180px;"><el-option v-for="w in warehouses" :key="w.id" :label="w.name" :value="w.id" /></el-select><el-button type="primary" @click="fetchData">查询</el-button></div>
    <div class="table-panel">
      <el-table v-loading="loading" :data="list" stripe border>
        <el-table-column prop="goods_code" label="商品编码" width="140" /><el-table-column prop="goods_name" label="商品名称" /><el-table-column prop="unit_name" label="单位" width="80" /><el-table-column prop="warehouse_name" label="仓库" width="140" /><el-table-column prop="bin_code" label="库位" width="120" /><el-table-column prop="quantity" label="数量" width="120" align="right" />
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref,reactive,onMounted } from 'vue';import { stockApi } from '@/api/stock';import { warehouseApi } from '@/api/warehouse'
const loading=ref(false),list=ref<any[]>([]),warehouses=ref<any[]>([]),filters=reactive({warehouse_id:null as string|null})
async function fetchData(){loading.value=true;try{const res:any=await stockApi.list({page_size:100,...filters});if(res.code===200){list.value=res.data}}finally{loading.value=false}}
onMounted(async()=>{const r:any=await warehouseApi.simple();warehouses.value=r?.data||[];fetchData()})
</script>
