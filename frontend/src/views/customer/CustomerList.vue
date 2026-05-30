<template>
  <div class="page-container">
    <div class="search-bar"><el-input v-model="search" placeholder="搜索客户..." clearable style="width:240px;" /><el-button type="primary" @click="fetchData">查询</el-button></div>
    <div class="table-panel">
      <div class="toolbar"><el-button type="primary" @click="openDialog()">新建客户</el-button></div>
      <el-table v-loading="loading" :data="list" stripe border>
        <el-table-column prop="code" label="编码" width="140" /><el-table-column prop="name" label="名称" /><el-table-column prop="contact_person" label="联系人" width="120" /><el-table-column prop="contact_phone" label="电话" width="140" />
        <el-table-column label="操作" width="160"><template #default="{row}"><el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button><el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button></template></el-table-column>
      </el-table>
    </div>
    <el-dialog v-model="dialogVisible" :title="editId?'编辑客户':'新建客户'" width="500px"><el-form :model="form" label-width="80px"><el-form-item label="编码" required><el-input v-model="form.code" :disabled="!!editId" /></el-form-item><el-form-item label="名称" required><el-input v-model="form.name" /></el-form-item><el-form-item label="联系人"><el-input v-model="form.contact_person" /></el-form-item><el-form-item label="电话"><el-input v-model="form.contact_phone" /></el-form-item><el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item></el-form><template #footer><el-button @click="dialogVisible=false">取消</el-button><el-button type="primary" :loading="submitting" @click="handleSubmit">保存</el-button></template></el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref,reactive,onMounted } from 'vue';import { ElMessage,ElMessageBox } from 'element-plus';import { customerApi } from '@/api/customer'
const loading=ref(false),submitting=ref(false),list=ref<any[]>([]),page=ref(1),pageSize=ref(20),total=ref(0),search=ref('')
const dialogVisible=ref(false),editId=ref(''),form=reactive({code:'',name:'',contact_person:'',contact_phone:'',email:''})
async function fetchData(){loading.value=true;try{const res:any=await customerApi.list({page:page.value,page_size:pageSize.value,search:search.value});if(res.code===200){list.value=res.data;total.value=res.meta?.total||0}}finally{loading.value=false}}
function openDialog(row?:any){if(row){editId.value=row.id;Object.assign(form,row)}else{editId.value='';Object.assign(form,{code:'',name:'',contact_person:'',contact_phone:'',email:''})};dialogVisible.value=true}
async function handleSubmit(){submitting.value=true;try{if(editId.value){await customerApi.update(editId.value,{...form});ElMessage.success('更新成功')}else{await customerApi.create({...form});ElMessage.success('创建成功')};dialogVisible.value=false;fetchData()}finally{submitting.value=false}}
async function handleDelete(row:any){await ElMessageBox.confirm('确定删除?','确认',{type:'warning'});await customerApi.remove(row.id);ElMessage.success('删除成功');fetchData()}
onMounted(fetchData)
</script>
