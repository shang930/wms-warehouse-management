<template>
  <div class="page-container" v-loading="loading">
    <el-page-header @back="$router.back()" :content="`入库单 — ${detail.asn_no||''}`" />
    <el-card style="margin-top:16px;" v-if="detail.id">
      <el-descriptions :column="3" border>
        <el-descriptions-item label="单号">{{detail.asn_no}}</el-descriptions-item><el-descriptions-item label="供应商">{{detail.supplier_name}}</el-descriptions-item><el-descriptions-item label="仓库">{{detail.warehouse_name}}</el-descriptions-item>
        <el-descriptions-item label="状态"><el-tag :type="statusType(detail.status)">{{detail.status_display}}</el-tag></el-descriptions-item><el-descriptions-item label="数量">{{detail.total_quantity}}</el-descriptions-item><el-descriptions-item label="操作人">{{detail.operator_name}}</el-descriptions-item>
      </el-descriptions>
      <el-divider>明细</el-divider>
      <el-table :data="detail.items" border><el-table-column prop="goods_code" label="编码" width="140" /><el-table-column prop="goods_name" label="名称" /><el-table-column prop="quantity" label="应入数量" width="100" align="right" /><el-table-column prop="actual_quantity" label="实收数量" width="100" align="right" /></el-table>
      <div style="margin-top:16px;text-align:right;" v-if="detail.status<4"><el-button type="primary" @click="advance">{{({1:'确认到货',2:'确认卸货',3:'确认上架'} as any)[detail.status]}}</el-button></div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref,onMounted } from 'vue';import { useRoute } from 'vue-router';import { ElMessage } from 'element-plus';import { asnApi } from '@/api/asn'
const route=useRoute();const loading=ref(false);const detail=ref<any>({})
async function fetch(){loading.value=true;try{const res:any=await asnApi.detail(route.params.id as string);detail.value=res?.data||{}}finally{loading.value=false}}
function statusType(s:number){return({1:'info',2:'warning',3:'primary',4:'success'} as any)[s]||'info'}
async function advance(){await asnApi.changeStatus(detail.value.id,{status:detail.value.status+1});ElMessage.success('状态更新');fetch()}
onMounted(fetch)
</script>
