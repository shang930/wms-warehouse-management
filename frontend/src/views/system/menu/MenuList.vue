<template>
  <div class="page-container">
    <div class="table-panel">
      <div class="toolbar"><el-button type="primary" @click="openDialog()">新建菜单</el-button></div>
      <el-table v-loading="loading" :data="list" row-key="id" default-expand-all stripe border>
        <el-table-column prop="name" label="菜单名称" width="200" /><el-table-column prop="code" label="权限标识" width="180" /><el-table-column label="类型" width="80"><template #default="{row}"><el-tag size="small">{{({D:'目录',M:'菜单',B:'按钮'} as any)[row.menu_type]}}</el-tag></template></el-table-column><el-table-column prop="path" label="路由" width="160" /><el-table-column prop="sort" label="排序" width="80" align="right" />
        <el-table-column label="操作" width="160"><template #default="{row}"><el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button><el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button></template></el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref,reactive,onMounted } from 'vue';import { ElMessage,ElMessageBox } from 'element-plus';import { menuApi } from '@/api/system'
const loading=ref(false),list=ref<any[]>([])
function flattenTree(nodes:any[]):any[]{let r:any[]=[];for(const n of nodes){r.push(n);if(n.children)r=r.concat(flattenTree(n.children))}return r}
async function fetchData(){loading.value=true;try{const res:any=await menuApi.tree();list.value=flattenTree(res?.data||[])}finally{loading.value=false}}
function openDialog(row?:any){if(row){ElMessage.info('编辑菜单请通过后台管理系统')}else{ElMessage.info('新建菜单请通过后台管理系统')}}
async function handleDelete(row:any){await ElMessageBox.confirm('确定删除?','确认',{type:'warning'});await menuApi.remove(row.id);ElMessage.success('删除成功');fetchData()}
onMounted(fetchData)
</script>
