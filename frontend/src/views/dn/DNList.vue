<template>
  <div class="page-container">
    <div class="search-bar"><el-select v-model="filters.status" placeholder="状态" clearable style="width:140px;"><el-option label="草稿" :value="1" /><el-option label="已确认" :value="2" /><el-option label="已拣货" :value="3" /><el-option label="已发货" :value="4" /></el-select><el-button type="primary" @click="fetchData">查询</el-button></div>
    <div class="table-panel">
      <div class="toolbar"><el-button type="primary" @click="$router.push('/dn/create')">新建出库单</el-button></div>
      <el-table v-loading="loading" :data="list" stripe border>
        <el-table-column prop="dn_no" label="出库单号" width="180" /><el-table-column prop="customer_name" label="客户" width="160" /><el-table-column prop="warehouse_name" label="仓库" width="120" />
        <el-table-column label="状态" width="100"><template #default="{row}"><el-tag :type="statusType(row.status)" size="small">{{row.status_display}}</el-tag></template></el-table-column>
        <el-table-column prop="total_quantity" label="总数量" width="100" align="right" /><el-table-column prop="tracking_no" label="物流单号" width="140" />
        <el-table-column label="操作" width="200" fixed="right"><template #default="{row}"><el-button link type="primary" size="small" @click="$router.push(`/dn/detail/${row.id}`)">详情</el-button><el-button v-if="row.status<4" link type="success" size="small" @click="advanceStatus(row)">下一状态</el-button><el-button v-if="row.status===1" link type="danger" size="small" @click="handleDelete(row)">删除</el-button></template></el-table-column>
      </el-table>
      <div style="margin-top:16px;display:flex;justify-content:flex-end;"><el-pagination v-model:current-page="page" v-model:page-size="pageSize" :total="total" :page-sizes="[10,20,50]" layout="total,sizes,prev,pager,next" @change="fetchData" /></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref,reactive,onMounted } from 'vue';import { ElMessage,ElMessageBox } from 'element-plus';import { dnApi } from '@/api/dn'
const loading=ref(false),list=ref<any[]>([]),page=ref(1),pageSize=ref(20),total=ref(0),filters=reactive({status:null as number|null})
async function fetchData(){loading.value=true;try{const res:any=await dnApi.list({page:page.value,page_size:pageSize.value,...filters});if(res.code===200){list.value=res.data;total.value=res.meta?.total||0}}finally{loading.value=false}}
function statusType(s:number){return({1:'info',2:'warning',3:'primary',4:'success'} as any)[s]||'info'}
async function advanceStatus(row:any){await ElMessageBox.confirm('确定状态变更?','确认',{type:'warning'});await dnApi.changeStatus(row.id,{status:row.status+1});ElMessage.success('状态更新成功');fetchData()}
async function handleDelete(row:any){await ElMessageBox.confirm('确定删除?','确认',{type:'warning'});await dnApi.remove(row.id);ElMessage.success('删除成功');fetchData()}
onMounted(fetchData)
</script>
