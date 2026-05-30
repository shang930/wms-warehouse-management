<template>
  <div class="page-container"><el-card><template #header>📥 入库报表</template><div class="stat-cards"><div class="stat-card"><div class="stat-info"><h3>入库总单数</h3><div class="stat-value">{{data.total_orders}}</div></div></div><div class="stat-card"><div class="stat-info"><h3>入库总量</h3><div class="stat-value">{{data.total_quantity}}</div></div></div></div><el-table :data="data.by_supplier||[]" border stripe><el-table-column prop="supplier__name" label="供应商" /><el-table-column prop="count" label="单数" width="120" align="right" /><el-table-column prop="total_qty" label="总量" width="140" align="right" /></el-table></el-card></div>
</template>
<script setup lang="ts">
import { ref,onMounted } from 'vue';import { reportApi } from '@/api/report'
const data=ref<any>({total_orders:0,total_quantity:0,by_supplier:[]})
onMounted(async()=>{const res:any=await reportApi.inbound();if(res.code===200)data.value=res.data})
</script>
