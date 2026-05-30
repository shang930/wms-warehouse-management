<template>
  <div class="page-container">
    <el-tabs v-model="activeTab" @tab-change="onTabChange">
      <el-tab-pane label="商品分类" name="category">
        <div class="toolbar" style="margin-bottom:12px;"><el-button type="primary" @click="openCatDialog()">新建分类</el-button></div>
        <el-table v-loading="catLoading" :data="catTree" row-key="id" border stripe default-expand-all>
          <el-table-column prop="name" label="名称" width="200" />
          <el-table-column prop="code" label="编码" width="160" />
          <el-table-column prop="sort" label="排序" width="80" align="right" />
          <el-table-column label="操作" width="160">
            <template #default="{row}"><el-button link type="primary" size="small" @click="openCatDialog(row)">编辑</el-button><el-button link type="danger" size="small" @click="handleCatDelete(row)">删除</el-button></template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="计量单位" name="unit">
        <div class="toolbar" style="margin-bottom:12px;"><el-button type="primary" @click="openUnitDialog()">新建单位</el-button></div>
        <el-table v-loading="unitLoading" :data="units" border stripe>
          <el-table-column prop="name" label="名称" width="200" />
          <el-table-column prop="code" label="编码" width="160" />
          <el-table-column label="操作" width="160">
            <template #default="{row}"><el-button link type="primary" size="small" @click="openUnitDialog(row)">编辑</el-button><el-button link type="danger" size="small" @click="handleUnitDelete(row)">删除</el-button></template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="品牌" name="brand">
        <div class="toolbar" style="margin-bottom:12px;"><el-button type="primary" @click="openBrandDialog()">新建品牌</el-button></div>
        <el-table v-loading="brandLoading" :data="brands" border stripe>
          <el-table-column prop="name" label="品牌名称" />
          <el-table-column label="操作" width="160">
            <template #default="{row}"><el-button link type="primary" size="small" @click="openBrandDialog(row)">编辑</el-button><el-button link type="danger" size="small" @click="handleBrandDelete(row)">删除</el-button></template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <!-- Category Dialog -->
    <el-dialog v-model="catVisible" :title="catEditId?'编辑分类':'新建分类'" width="460px">
      <el-form :model="catForm" label-width="80px">
        <el-form-item label="名称" required><el-input v-model="catForm.name" /></el-form-item>
        <el-form-item label="编码" required><el-input v-model="catForm.code" /></el-form-item>
        <el-form-item label="上级分类"><el-tree-select v-model="catForm.parent" :data="catTreeForSelect" :props="{label:'name',value:'id',children:'children'}" placeholder="无(顶级分类)" clearable check-strictly style="width:100%;" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="catForm.sort" :min="0" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="catVisible=false">取消</el-button><el-button type="primary" :loading="catSubmitting" @click="handleCatSubmit">保存</el-button></template>
    </el-dialog>

    <!-- Unit Dialog -->
    <el-dialog v-model="unitVisible" :title="unitEditId?'编辑单位':'新建单位'" width="400px">
      <el-form :model="unitForm" label-width="80px">
        <el-form-item label="名称" required><el-input v-model="unitForm.name" /></el-form-item>
        <el-form-item label="编码" required><el-input v-model="unitForm.code" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="unitVisible=false">取消</el-button><el-button type="primary" :loading="unitSubmitting" @click="handleUnitSubmit">保存</el-button></template>
    </el-dialog>

    <!-- Brand Dialog -->
    <el-dialog v-model="brandVisible" :title="brandEditId?'编辑品牌':'新建品牌'" width="400px">
      <el-form :model="brandForm" label-width="80px">
        <el-form-item label="名称" required><el-input v-model="brandForm.name" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="brandVisible=false">取消</el-button><el-button type="primary" :loading="brandSubmitting" @click="handleBrandSubmit">保存</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref,reactive,onMounted } from 'vue'
import { ElMessage,ElMessageBox } from 'element-plus'
import { categoryApi, unitApi, brandApi } from '@/api/goods'

const activeTab=ref('category')

// --- Category ---
const catLoading=ref(false),catSubmitting=ref(false),catVisible=ref(false),catEditId=ref('')
const catTree=ref<any[]>([])
const catForm=reactive({name:'',code:'',parent:null as any,sort:0})
async function loadCategories(){catLoading.value=true;try{const res:any=await categoryApi.tree();catTree.value=res?.data||[]}finally{catLoading.value=false}}
const catTreeForSelect = catTree // same data
function openCatDialog(row?:any){
  if(row){catEditId.value=row.id;catForm.name=row.name;catForm.code=row.code;catForm.parent=row.parent||null;catForm.sort=row.sort}
  else{catEditId.value='';catForm.name='';catForm.code='';catForm.parent=null;catForm.sort=0}
  catVisible.value=true
}
async function handleCatSubmit(){
  catSubmitting.value=true
  try{
    const data:any={name:catForm.name,code:catForm.code,sort:catForm.sort}
    if(catForm.parent)data.parent=catForm.parent;else data.parent=null
    if(catEditId.value){await categoryApi.update(catEditId.value,data);ElMessage.success('更新成功')}
    else{await categoryApi.create(data);ElMessage.success('创建成功')}
    catVisible.value=false;loadCategories()
  }finally{catSubmitting.value=false}
}
async function handleCatDelete(row:any){await ElMessageBox.confirm('确定删除?','确认',{type:'warning'});await categoryApi.remove(row.id);ElMessage.success('删除成功');loadCategories()}

// --- Unit ---
const unitLoading=ref(false),unitSubmitting=ref(false),unitVisible=ref(false),unitEditId=ref('')
const units=ref<any[]>([])
const unitForm=reactive({name:'',code:''})
async function loadUnits(){unitLoading.value=true;try{const res:any=await unitApi.list({page_size:200});units.value=res?.data||[]}finally{unitLoading.value=false}}
function openUnitDialog(row?:any){
  if(row){unitEditId.value=row.id;unitForm.name=row.name;unitForm.code=row.code}
  else{unitEditId.value='';unitForm.name='';unitForm.code=''}
  unitVisible.value=true
}
async function handleUnitSubmit(){
  unitSubmitting.value=true
  try{
    if(unitEditId.value){await unitApi.update(unitEditId.value,{...unitForm});ElMessage.success('更新成功')}
    else{await unitApi.create({...unitForm});ElMessage.success('创建成功')}
    unitVisible.value=false;loadUnits()
  }finally{unitSubmitting.value=false}
}
async function handleUnitDelete(row:any){await ElMessageBox.confirm('确定删除?','确认',{type:'warning'});await unitApi.remove(row.id);ElMessage.success('删除成功');loadUnits()}

// --- Brand ---
const brandLoading=ref(false),brandSubmitting=ref(false),brandVisible=ref(false),brandEditId=ref('')
const brands=ref<any[]>([])
const brandForm=reactive({name:''})
async function loadBrands(){brandLoading.value=true;try{const res:any=await brandApi.list({page_size:200});brands.value=res?.data||[]}finally{brandLoading.value=false}}
function openBrandDialog(row?:any){
  if(row){brandEditId.value=row.id;brandForm.name=row.name}
  else{brandEditId.value='';brandForm.name=''}
  brandVisible.value=true
}
async function handleBrandSubmit(){
  brandSubmitting.value=true
  try{
    if(brandEditId.value){await brandApi.update(brandEditId.value,{...brandForm});ElMessage.success('更新成功')}
    else{await brandApi.create({...brandForm});ElMessage.success('创建成功')}
    brandVisible.value=false;loadBrands()
  }finally{brandSubmitting.value=false}
}
async function handleBrandDelete(row:any){await ElMessageBox.confirm('确定删除?','确认',{type:'warning'});await brandApi.remove(row.id);ElMessage.success('删除成功');loadBrands()}

const loadMap:Record<string,()=>void>={category:loadCategories,unit:loadUnits,brand:loadBrands}
function onTabChange(tab:any){loadMap[tab]?.()}
onMounted(loadCategories)
</script>
