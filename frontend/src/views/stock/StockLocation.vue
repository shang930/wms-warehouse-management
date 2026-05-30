<template>
  <div class="page-container">
    <div class="search-bar"><el-select v-model="warehouseId" placeholder="选择仓库" style="width:200px;" @change="loadBins"><el-option v-for="w in warehouses" :key="w.id" :label="w.name" :value="w.id" /></el-select></div>
    <el-card v-if="warehouseId"><div v-if="bins.length" style="display:flex;flex-wrap:wrap;gap:12px;"><div v-for="b in bins" :key="b.id" class="bin-cell" :class="binClass(b)"><div class="bin-code">{{b.code}}</div><div class="bin-load">{{b.current_load||0}}</div></div></div><el-empty v-else /></el-card>
    <el-empty v-else description="请选择仓库" />
  </div>
</template>

<script setup lang="ts">
import { ref,onMounted } from 'vue';import { binApi } from '@/api/warehouse';import { warehouseApi } from '@/api/warehouse'
const bins=ref<any[]>([]),warehouses=ref<any[]>([]),warehouseId=ref('')
async function loadBins(){if(!warehouseId.value)return;const res:any=await binApi.list({warehouse_id:warehouseId.value,page_size:200});bins.value=res?.data||[]}
function binClass(b:any){if(b.attribute==='D')return'bin-damaged';if(b.attribute==='H')return'bin-holding';return'bin-normal'}
onMounted(async()=>{const r:any=await warehouseApi.simple();warehouses.value=r?.data||[]})
</script>

<style lang="scss" scoped>
.bin-cell{width:80px;height:80px;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:8px;cursor:pointer;font-size:13px;transition:all 0.2s;border:2px solid #ddd;&:hover{transform:scale(1.05)}}
.bin-normal{background:#e8f5e9;border-color:#a5d6a7}
.bin-damaged{background:#ffebee;border-color:#ef9a9a}
.bin-holding{background:#e3f2fd;border-color:#90caf9}
.bin-code{font-weight:600;color:#303133}
.bin-load{font-size:11px;color:#909399;margin-top:4px}
</style>
