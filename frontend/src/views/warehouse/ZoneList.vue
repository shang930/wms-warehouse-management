<template>
  <div class="page-container">
    <div class="search-bar">
      <el-select v-model="filters.warehouse_id" placeholder="选择仓库" clearable style="width:200px;">
        <el-option v-for="w in warehouses" :key="w.id" :label="w.name" :value="w.id" />
      </el-select>
      <el-button type="primary" @click="fetchData">查询</el-button>
    </div>
    <div class="table-panel">
      <div class="toolbar"><el-button type="primary" @click="openDialog()">新建库区</el-button></div>
      <el-table v-loading="loading" :data="list" stripe border>
        <el-table-column prop="code" label="编码" width="140" />
        <el-table-column prop="name" label="名称" width="160" />
        <el-table-column prop="warehouse_name" label="所属仓库" width="140" />
        <el-table-column prop="sort" label="排序" width="80" align="right" />
        <el-table-column label="操作" width="160">
          <template #default="{row}"><el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button><el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button></template>
        </el-table-column>
      </el-table>
      <div style="margin-top:16px;display:flex;justify-content:flex-end;">
        <el-pagination v-model:current-page="page" v-model:page-size="pageSize" :total="total" :page-sizes="[10,20,50]" layout="total,sizes,prev,pager,next" @change="fetchData" />
      </div>
    </div>
    <el-dialog v-model="dialogVisible" :title="editId?'编辑库区':'新建库区'" width="460px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="所属仓库" required><el-select v-model="form.warehouse" style="width:100%;"><el-option v-for="w in warehouses" :key="w.id" :label="w.name" :value="w.id" /></el-select></el-form-item>
        <el-form-item label="编码" required><el-input v-model="form.code" /></el-form-item>
        <el-form-item label="名称" required><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.sort" :min="0" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="dialogVisible=false">取消</el-button><el-button type="primary" :loading="submitting" @click="handleSubmit">保存</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref,reactive,onMounted } from 'vue'
import { ElMessage,ElMessageBox } from 'element-plus'
import { warehouseApi, zoneApi } from '@/api/warehouse'

const loading=ref(false),submitting=ref(false),list=ref<any[]>([])
const page=ref(1),pageSize=ref(20),total=ref(0),warehouses=ref<any[]>([])
const filters=reactive({warehouse_id:null as string|null})
const dialogVisible=ref(false),editId=ref('')
const form=reactive({warehouse:'',code:'',name:'',sort:0})

async function fetchData(){loading.value=true;try{const res:any=await zoneApi.list({page:page.value,page_size:pageSize.value,...filters});if(res.code===200){list.value=res.data;total.value=res.meta?.total||0}}finally{loading.value=false}}

function openDialog(row?:any){
  if(row){editId.value=row.id;form.warehouse=row.warehouse;form.code=row.code;form.name=row.name;form.sort=row.sort}
  else{editId.value='';form.warehouse='';form.code='';form.name='';form.sort=0}
  dialogVisible.value=true
}

async function handleSubmit(){
  submitting.value=true
  try{
    if(editId.value){await zoneApi.update(editId.value,{...form});ElMessage.success('更新成功')}
    else{await zoneApi.create({...form});ElMessage.success('创建成功')}
    dialogVisible.value=false;fetchData()
  }finally{submitting.value=false}
}

async function handleDelete(row:any){await ElMessageBox.confirm('确定删除?','确认',{type:'warning'});await zoneApi.remove(row.id);ElMessage.success('删除成功');fetchData()}

onMounted(async()=>{
  const r:any=await warehouseApi.simple()
  warehouses.value=r?.data||[]
  fetchData()
})
</script>
