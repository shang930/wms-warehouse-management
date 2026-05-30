<template>
  <div class="page-container"><el-card><template #header>📦 库存报表</template><div class="stat-cards"><div class="stat-card"><div class="stat-info"><h3>商品种类</h3><div class="stat-value">{{data.total_items}}</div></div></div><div class="stat-card"><div class="stat-info"><h3>总库存量</h3><div class="stat-value">{{data.total_quantity}}</div></div></div></div><el-table :data="data.details||[]" border stripe max-height="500"><el-table-column prop="goods_code" label="商品编码" width="140" /><el-table-column prop="goods_name" label="商品名称" /><el-table-column prop="warehouse_name" label="仓库" width="120" /><el-table-column prop="bin_code" label="库位" width="100" /><el-table-column prop="quantity" label="数量" width="100" align="right" /></el-table></el-card></div>
</template>
<script setup lang="ts">
import { ref,onMounted } from 'vue';import { reportApi } from '@/api/report'
const data=ref<any>({total_items:0,total_quantity:0,details:[]})
onMounted(async()=>{const res:any=await reportApi.inventory();if(res.code===200)data.value=res.data})
</script>
