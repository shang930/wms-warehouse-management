<template>
  <div class="page-container">
    <div class="search-bar">
      <el-select v-model="filters.warehouse_id" placeholder="仓库" clearable style="width:180px;" @change="onWarehouseChange"><el-option v-for="w in warehouses" :key="w.id" :label="w.name" :value="w.id" /></el-select>
      <el-select v-model="filters.zone_id" placeholder="库区" clearable style="width:160px;"><el-option v-for="z in zones" :key="z.id" :label="z.name" :value="z.id" /></el-select>
      <el-select v-model="filters.attribute" placeholder="属性" clearable style="width:120px;"><el-option label="正常" value="N" /><el-option label="损坏" value="D" /><el-option label="暂存" value="H" /><el-option label="检验" value="I" /></el-select>
      <el-button type="primary" @click="fetchData">查询</el-button>
    </div>
    <div class="table-panel">
      <div class="toolbar">
        <el-button type="primary" @click="openDialog()">新建库位</el-button>
        <el-button type="success" @click="batchVisible=true">批量生成</el-button>
      </div>
      <el-table v-loading="loading" :data="list" stripe border>
        <el-table-column prop="code" label="库位编码" width="130" />
        <el-table-column prop="warehouse_name" label="仓库" width="120" />
        <el-table-column prop="zone_name" label="库区" width="120" />
        <el-table-column prop="row" label="排" width="60" align="center" />
        <el-table-column prop="col" label="列" width="60" align="center" />
        <el-table-column prop="level" label="层" width="60" align="center" />
        <el-table-column prop="attribute" label="属性" width="80" align="center">
          <template #default="{row}"><el-tag :type="attrTag(row.attribute)" size="small">{{attrLabel(row.attribute)}}</el-tag></template>
        </el-table-column>
        <el-table-column prop="max_capacity" label="最大容量" width="100" align="right" />
        <el-table-column prop="current_load" label="当前库存" width="100" align="right" />
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{row}"><el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button><el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button></template>
        </el-table-column>
      </el-table>
      <div style="margin-top:16px;display:flex;justify-content:flex-end;">
        <el-pagination v-model:current-page="page" v-model:page-size="pageSize" :total="total" :page-sizes="[10,20,50,100]" layout="total,sizes,prev,pager,next" @change="fetchData" />
      </div>
    </div>

    <!-- Edit Dialog -->
    <el-dialog v-model="dialogVisible" :title="editId?'编辑库位':'新建库位'" width="520px">
      <el-form :model="form" label-width="80px">
        <el-row :gutter="16">
          <el-col :span="12"><el-form-item label="仓库" required><el-select v-model="form.warehouse" style="width:100%;"><el-option v-for="w in warehouses" :key="w.id" :label="w.name" :value="w.id" /></el-select></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="库区"><el-select v-model="form.zone" style="width:100%;" clearable><el-option v-for="z in zones" :key="z.id" :label="z.name" :value="z.id" /></el-select></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="编码" required><el-input v-model="form.code" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="排"><el-input v-model="form.row" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="列"><el-input v-model="form.col" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="层"><el-input v-model="form.level" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="属性"><el-select v-model="form.attribute" style="width:100%;"><el-option label="正常" value="N" /><el-option label="损坏" value="D" /><el-option label="暂存" value="H" /><el-option label="检验" value="I" /></el-select></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="长(cm)"><el-input-number v-model="form.length" :min="0" style="width:100%;" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="宽(cm)"><el-input-number v-model="form.width" :min="0" style="width:100%;" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="高(cm)"><el-input-number v-model="form.height" :min="0" style="width:100%;" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="最大容量"><el-input-number v-model="form.max_capacity" :min="0" style="width:100%;" /></el-form-item></el-col>
        </el-row>
      </el-form>
      <template #footer><el-button @click="dialogVisible=false">取消</el-button><el-button type="primary" :loading="submitting" @click="handleSubmit">保存</el-button></template>
    </el-dialog>

    <!-- Batch Dialog -->
    <el-dialog v-model="batchVisible" title="批量生成库位" width="440px">
      <el-form :model="batchForm" label-width="80px">
        <el-form-item label="仓库" required><el-select v-model="batchForm.warehouse_id" style="width:100%;"><el-option v-for="w in warehouses" :key="w.id" :label="w.name" :value="w.id" /></el-select></el-form-item>
        <el-form-item label="库区"><el-select v-model="batchForm.zone_id" style="width:100%;" clearable><el-option v-for="z in zones" :key="z.id" :label="z.name" :value="z.id" /></el-select></el-form-item>
        <el-form-item label="起始排号"><el-input-number v-model="batchForm.row_start" :min="1" style="width:100%;" /></el-form-item>
        <el-row :gutter="12">
          <el-col :span="8"><el-form-item label="排数"><el-input-number v-model="batchForm.rows" :min="1" :max="99" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="列数"><el-input-number v-model="batchForm.cols" :min="1" :max="99" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="层数"><el-input-number v-model="batchForm.levels" :min="1" :max="99" /></el-form-item></el-col>
        </el-row>
      </el-form>
      <template #footer><el-button @click="batchVisible=false">取消</el-button><el-button type="primary" :loading="batchSubmitting" @click="handleBatchCreate">生成</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref,reactive,onMounted } from 'vue'
import { ElMessage,ElMessageBox } from 'element-plus'
import { warehouseApi, zoneApi, binApi } from '@/api/warehouse'

const loading=ref(false),submitting=ref(false),list=ref<any[]>([])
const page=ref(1),pageSize=ref(20),total=ref(0)
const warehouses=ref<any[]>([]),zones=ref<any[]>([])
const filters=reactive({warehouse_id:null as string|null,zone_id:null as string|null,attribute:null as string|null})

const dialogVisible=ref(false),editId=ref('')
const form=reactive<any>({warehouse:'',zone:null,code:'',row:'',col:'',level:'',attribute:'N',length:null,width:null,height:null,max_capacity:null})

const batchVisible=ref(false),batchSubmitting=ref(false)
const batchForm=reactive({warehouse_id:'',zone_id:'',row_start:1,rows:3,cols:5,levels:3})

function attrTag(v:string){return ({N:'',D:'danger',H:'warning',I:'info'} as any)[v]||''}
function attrLabel(v:string){return ({N:'正常',D:'损坏',H:'暂存',I:'检验'} as any)[v]||v}

async function loadWarehouses(){const r:any=await warehouseApi.simple();warehouses.value=r?.data||[]}
async function loadZones(warehouseId?:string|null){
  const params:any={page_size:500}
  if(warehouseId)params.warehouse_id=warehouseId
  const r:any=await zoneApi.list(params)
  zones.value=r?.data||[]
}
function onWarehouseChange(val:string|null){filters.zone_id=null;loadZones(val);fetchData()}

async function fetchData(){loading.value=true;try{const params:any={page:page.value,page_size:pageSize.value};if(filters.warehouse_id)params.warehouse_id=filters.warehouse_id;if(filters.zone_id)params.zone_id=filters.zone_id;if(filters.attribute)params.attribute=filters.attribute;const res:any=await binApi.list(params);if(res.code===200){list.value=res.data;total.value=res.meta?.total||0}}finally{loading.value=false}}

function openDialog(row?:any){
  if(row){editId.value=row.id;form.warehouse=row.warehouse;form.zone=row.zone;form.code=row.code;form.row=row.row;form.col=row.col;form.level=row.level;form.attribute=row.attribute;form.length=row.length;form.width=row.width;form.height=row.height;form.max_capacity=row.max_capacity}
  else{editId.value='';Object.assign(form,{warehouse:'',zone:null,code:'',row:'',col:'',level:'',attribute:'N',length:null,width:null,height:null,max_capacity:null})}
  dialogVisible.value=true
}

async function handleSubmit(){
  submitting.value=true
  try{
    if(editId.value){await binApi.update(editId.value,{...form});ElMessage.success('更新成功')}
    else{await binApi.create({...form});ElMessage.success('创建成功')}
    dialogVisible.value=false;fetchData()
  }finally{submitting.value=false}
}

async function handleDelete(row:any){await ElMessageBox.confirm('确定删除?','确认',{type:'warning'});await binApi.remove(row.id);ElMessage.success('删除成功');fetchData()}

async function handleBatchCreate(){
  if(!batchForm.warehouse_id){ElMessage.warning('请选择仓库');return}
  batchSubmitting.value=true
  try{await binApi.batchCreate(batchForm);ElMessage.success('批量生成成功');batchVisible.value=false;fetchData()}
  finally{batchSubmitting.value=false}
}

onMounted(async()=>{await loadWarehouses();await loadZones();fetchData()})
</script>
