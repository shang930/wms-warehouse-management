<template>
  <div class="page-container">
    <div class="search-bar"><el-select v-model="filters.movement_type" placeholder="变动类型" clearable style="width:140px;"><el-option label="入库" :value="1" /><el-option label="出库" :value="2" /><el-option label="移库" :value="3" /></el-select><el-button type="primary" @click="fetchData">查询</el-button></div>
    <div class="table-panel">
      <el-table v-loading="loading" :data="list" stripe border>
        <el-table-column prop="goods_code" label="商品编码" width="140" /><el-table-column prop="goods_name" label="商品名称" /><el-table-column label="类型" width="100"><template #default="{row}">{{({1:'入库',2:'出库',3:'移库',4:'盘点',5:'报损'} as any)[row.movement_type]}}</template></el-table-column>
        <el-table-column prop="quantity" label="数量" width="100" align="right" /><el-table-column prop="ref_no" label="关联单号" width="180" /><el-table-column prop="operator_name" label="操作人" width="100" /><el-table-column prop="created_at" label="时间" width="160" />
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref,reactive,onMounted } from 'vue';import { stockApi } from '@/api/stock'
const loading=ref(false),list=ref<any[]>([]),filters=reactive({movement_type:null as number|null})
async function fetchData(){loading.value=true;try{const res:any=await stockApi.movements({page_size:100,...filters});if(res.code===200){list.value=res.data}}finally{loading.value=false}}
onMounted(fetchData)
</script>
