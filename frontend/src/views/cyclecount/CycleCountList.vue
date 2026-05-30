<template>
  <div class="page-container">
    <div class="search-bar"><el-select v-model="filters.status" placeholder="状态" clearable style="width:140px;"><el-option label="草稿" :value="1" /><el-option label="盘点中" :value="2" /><el-option label="已完成" :value="3" /></el-select><el-button type="primary" @click="fetchData">查询</el-button></div>
    <div class="table-panel">
      <div class="toolbar"><el-button type="primary" @click="openCreate">创建盘点</el-button></div>
      <el-table v-loading="loading" :data="list" stripe border>
        <el-table-column prop="count_no" label="盘点单号" width="180" /><el-table-column prop="warehouse_name" label="仓库" width="140" />
        <el-table-column label="状态" width="100"><template #default="{row}"><el-tag :type="statusType(row.status)" size="small">{{row.status_display}}</el-tag></template></el-table-column>
        <el-table-column prop="total_items" label="盘点项数" width="100" align="right" /><el-table-column prop="diff_items" label="差异项" width="80" align="right" />
        <el-table-column label="操作" width="180"><template #default="{row}"><el-button v-if="row.status===1" link type="primary" size="small" @click="doStart(row)">开始</el-button><el-button v-if="row.status===3" link type="warning" size="small" @click="doAdjust(row)">调整</el-button></template></el-table-column>
      </el-table>
    </div>
    <el-dialog v-model="createVisible" title="创建盘点" width="400px"><el-form :model="createForm" label-width="80px"><el-form-item label="仓库"><el-select v-model="createForm.warehouse" style="width:100%;"><el-option v-for="w in warehouses" :key="w.id" :label="w.name" :value="w.id" /></el-select></el-form-item><el-form-item label="备注"><el-input v-model="createForm.remark" /></el-form-item></el-form><template #footer><el-button @click="createVisible=false">取消</el-button><el-button type="primary" @click="handleCreate">创建</el-button></template></el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref,reactive,onMounted } from 'vue';import { ElMessage } from 'element-plus';import { cycleCountApi } from '@/api/cyclecount';import { warehouseApi } from '@/api/warehouse'
const loading=ref(false),list=ref<any[]>([]),warehouses=ref<any[]>([]),filters=reactive({status:null as number|null}),createVisible=ref(false),createForm=reactive({warehouse:'',remark:''})
async function fetchData(){loading.value=true;try{const res:any=await cycleCountApi.list({...filters});if(res.code===200){list.value=res.data}}finally{loading.value=false}}
function statusType(s:number){return({1:'info',2:'warning',3:'primary',4:'success'} as any)[s]||'info'}
function openCreate(){createForm.warehouse='';createForm.remark='';createVisible.value=true}
async function handleCreate(){await cycleCountApi.create({warehouse:createForm.warehouse,remark:createForm.remark});ElMessage.success('创建成功');createVisible.value=false;fetchData()}
async function doStart(row:any){await cycleCountApi.start(row.id);ElMessage.success('已开始');fetchData()}
async function doAdjust(row:any){await cycleCountApi.adjust(row.id);ElMessage.success('已调整');fetchData()}
onMounted(async()=>{const r:any=await warehouseApi.simple();warehouses.value=r?.data||[];fetchData()})
</script>
