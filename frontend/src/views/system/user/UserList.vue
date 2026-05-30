<template>
  <div class="page-container">
    <div class="search-bar"><el-input v-model="search" placeholder="搜索用户..." clearable style="width:240px;" /><el-button type="primary" @click="fetchData">查询</el-button></div>
    <div class="table-panel">
      <div class="toolbar"><el-button type="primary" @click="openDialog()">新建用户</el-button></div>
      <el-table v-loading="loading" :data="list" stripe border>
        <el-table-column prop="username" label="用户名" width="140" /><el-table-column prop="first_name" label="姓名" width="120" /><el-table-column prop="email" label="邮箱" /><el-table-column prop="phone" label="手机号" width="140" /><el-table-column prop="department_name" label="部门" width="120" />
        <el-table-column label="操作" width="160"><template #default="{row}"><el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button><el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button></template></el-table-column>
      </el-table>
    </div>
    <el-dialog v-model="dialogVisible" :title="editId?'编辑用户':'新建用户'" width="500px"><el-form :model="form" label-width="80px"><el-form-item label="用户名" required><el-input v-model="form.username" /></el-form-item><el-form-item label="姓名"><el-input v-model="form.first_name" /></el-form-item><el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item><el-form-item label="手机"><el-input v-model="form.phone" /></el-form-item><el-form-item label="密码"><el-input v-model="form.password" type="password" :placeholder="editId?'留空不修改':''" /></el-form-item></el-form><template #footer><el-button @click="dialogVisible=false">取消</el-button><el-button type="primary" :loading="submitting" @click="handleSubmit">保存</el-button></template></el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref,reactive,onMounted } from 'vue';import { ElMessage,ElMessageBox } from 'element-plus';import { userApi } from '@/api/system'
const loading=ref(false),submitting=ref(false),list=ref<any[]>([]),search=ref('')
const dialogVisible=ref(false),editId=ref(''),form=reactive({username:'',first_name:'',email:'',phone:'',password:''})
async function fetchData(){loading.value=true;try{const res:any=await userApi.list({search:search.value});if(res.code===200)list.value=res.data}finally{loading.value=false}}
function openDialog(row?:any){if(row){editId.value=row.id;form.username=row.username;form.first_name=row.first_name;form.email=row.email;form.phone=row.phone;form.password=''}else{editId.value='';form.username='';form.first_name='';form.email='';form.phone='';form.password=''};dialogVisible.value=true}
async function handleSubmit(){submitting.value=true;try{const data:any={username:form.username,first_name:form.first_name,email:form.email,phone:form.phone};if(form.password)data.password=form.password;if(editId.value){await userApi.update(editId.value,data);ElMessage.success('更新成功')}else{await userApi.create(data);ElMessage.success('创建成功')};dialogVisible.value=false;fetchData()}finally{submitting.value=false}}
async function handleDelete(row:any){await ElMessageBox.confirm('确定删除?','确认',{type:'warning'});await userApi.remove(row.id);ElMessage.success('删除成功');fetchData()}
onMounted(fetchData)
</script>
