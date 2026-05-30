<template>
  <div class="page-container">
    <div class="search-bar">
      <el-input v-model="search" placeholder="搜索商品..." clearable style="width:240px;" />
      <el-button type="primary" @click="fetchData">查询</el-button>
    </div>
    <div class="table-panel">
      <div class="toolbar"><el-button type="primary" @click="openDialog()">新建商品</el-button></div>
      <el-table v-loading="loading" :data="list" stripe border>
        <el-table-column prop="code" label="商品编码" width="140" />
        <el-table-column prop="name" label="商品名称" />
        <el-table-column prop="category_name" label="分类" width="120" />
        <el-table-column prop="unit_name" label="单位" width="80" />
        <el-table-column prop="spec" label="规格" width="140" />
        <el-table-column prop="safety_stock" label="安全库存" width="100" align="right" />
        <el-table-column prop="total_stock" label="当前库存" width="100" align="right">
          <template #default="{row}"><span :style="{color:row.total_stock<row.safety_stock?'var(--color-danger)':''}">{{row.total_stock}}</span></template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{row}"><el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button><el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button></template>
        </el-table-column>
      </el-table>
      <div style="margin-top:16px;display:flex;justify-content:flex-end;"><el-pagination v-model:current-page="page" v-model:page-size="pageSize" :total="total" :page-sizes="[10,20,50]" layout="total,sizes,prev,pager,next" @change="fetchData" /></div>
    </div>
    <el-dialog v-model="dialogVisible" :title="editId?'编辑商品':'新建商品'" width="600px">
      <el-form :model="form" label-width="80px">
        <el-row :gutter="16">
          <el-col :span="12"><el-form-item label="编码" required><el-input v-model="form.code" :disabled="!!editId" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="名称" required><el-input v-model="form.name" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="分类"><el-select v-model="form.category" style="width:100%;"><el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" /></el-select></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="单位"><el-select v-model="form.unit" style="width:100%;"><el-option v-for="u in units" :key="u.id" :label="u.name" :value="u.id" /></el-select></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="规格"><el-input v-model="form.spec" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="条码"><el-input v-model="form.barcode" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="安全库存"><el-input-number v-model="form.safety_stock" :min="0" style="width:100%;" /></el-form-item></el-col>
        </el-row>
      </el-form>
      <template #footer><el-button @click="dialogVisible=false">取消</el-button><el-button type="primary" :loading="submitting" @click="handleSubmit">保存</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { goodsApi, categoryApi, unitApi } from '@/api/goods'

const loading=ref(false),submitting=ref(false),list=ref<any[]>([]),categories=ref<any[]>([]),units=ref<any[]>([])
const page=ref(1),pageSize=ref(20),total=ref(0),search=ref('')
const dialogVisible=ref(false),editId=ref('')
const form=reactive<any>({code:'',name:'',category:'',unit:'',spec:'',barcode:'',safety_stock:0})

async function fetchData(){loading.value=true;try{const res:any=await goodsApi.list({page:page.value,page_size:pageSize.value,search:search.value});if(res.code===200){list.value=res.data;total.value=res.meta?.total||0}}finally{loading.value=false}}
async function loadOptions(){const[catRes,unitRes]=await Promise.all([categoryApi.tree(),unitApi.list()])
  const flatCats=(nodes:any[]):any[]=>{let r:any[]=[];for(const n of nodes){r.push(n);if(n.children)r=r.concat(flatCats(n.children))}return r}
  categories.value=flatCats((catRes as any)?.data||[]);units.value=(unitRes as any)?.data||[]}

function openDialog(row?:any){if(row){editId.value=row.id;Object.assign(form,row)}else{editId.value='';Object.assign(form,{code:'',name:'',category:'',unit:'',spec:'',barcode:'',safety_stock:0})}dialogVisible.value=true}

async function handleSubmit(){submitting.value=true;try{if(editId.value){await goodsApi.update(editId.value,{...form});ElMessage.success('更新成功')}else{await goodsApi.create({...form});ElMessage.success('创建成功')}dialogVisible.value=false;fetchData()}finally{submitting.value=false}}

async function handleDelete(row:any){await ElMessageBox.confirm('确定删除?','确认',{type:'warning'});await goodsApi.remove(row.id);ElMessage.success('删除成功');fetchData()}

onMounted(()=>{loadOptions();fetchData()})
</script>
