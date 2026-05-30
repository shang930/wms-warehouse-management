<template>
  <div class="page-container">
    <div class="table-panel">
      <div class="toolbar"><el-button type="primary" @click="openDialog()">新建部门</el-button></div>
      <el-table v-loading="loading" :data="list" row-key="id" default-expand-all stripe border>
        <el-table-column prop="name" label="部门名称" width="200" /><el-table-column prop="code" label="编码" width="160" /><el-table-column prop="sort" label="排序" width="80" align="right" />
        <el-table-column label="操作" width="160"><template #default="{row}"><el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button><el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button></template></el-table-column>
      </el-table>
    </div>
    <el-dialog v-model="dialogVisible" :title="editId?'编辑部门':'新建部门'" width="500px"><el-form :model="form" label-width="80px"><el-form-item label="名称" required><el-input v-model="form.name" /></el-form-item><el-form-item label="编码" required><el-input v-model="form.code" /></el-form-item><el-form-item label="排序"><el-input-number v-model="form.sort" :min="0" /></el-form-item></el-form><template #footer><el-button @click="dialogVisible=false">取消</el-button><el-button type="primary" :loading="submitting" @click="handleSubmit">保存</el-button></template></el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref,reactive,onMounted } from 'vue';import { ElMessage,ElMessageBox } from 'element-plus';import { deptApi } from '@/api/system'
const loading=ref(false),submitting=ref(false),list=ref<any[]>([])
const dialogVisible=ref(false),editId=ref(''),form=reactive({name:'',code:'',sort:0})
function flattenTree(nodes:any[]):any[]{let r:any[]=[];for(const n of nodes){r.push(n);if(n.children)r=r.concat(flattenTree(n.children))}return r}
async function fetchData(){loading.value=true;try{const res:any=await deptApi.tree();list.value=flattenTree(res?.data||[])}finally{loading.value=false}}
function openDialog(row?:any){if(row){editId.value=row.id;form.name=row.name;form.code=row.code;form.sort=row.sort||0}else{editId.value='';form.name='';form.code='';form.sort=0};dialogVisible.value=true}
async function handleSubmit(){submitting.value=true;try{if(editId.value){await deptApi.update(editId.value,{...form});ElMessage.success('更新成功')}else{await deptApi.create({...form});ElMessage.success('创建成功')};dialogVisible.value=false;fetchData()}finally{submitting.value=false}}
async function handleDelete(row:any){await ElMessageBox.confirm('确定删除?','确认',{type:'warning'});await deptApi.remove(row.id);ElMessage.success('删除成功');fetchData()}
onMounted(fetchData)
</script>
