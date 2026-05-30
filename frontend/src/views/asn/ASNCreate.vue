<template>
  <div class="page-container">
    <el-page-header @back="$router.back()" content="创建入库单" />
    <el-card style="margin-top:16px;">
      <el-form :model="form" label-width="100px">
        <el-row :gutter="16">
          <el-col :span="8"><el-form-item label="供应商" required><el-select v-model="form.supplier" style="width:100%;"><el-option v-for="s in suppliers" :key="s.id" :label="s.name" :value="s.id" /></el-select></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="目标仓库" required><el-select v-model="form.warehouse" style="width:100%;"><el-option v-for="w in warehouses" :key="w.id" :label="w.name" :value="w.id" /></el-select></el-form-item></el-col>
        </el-row>
      </el-form>
      <el-divider content-position="left">入库明细</el-divider>
      <div style="margin-bottom:12px;"><el-button size="small" @click="showSelector=true">+ 添加商品</el-button></div>
      <el-table :data="form.items" border>
        <el-table-column label="序号" type="index" width="60" /><el-table-column label="商品" width="220"><template #default="{row}">{{row.goods_name||row.goods_code}}</template></el-table-column>
        <el-table-column label="数量" width="140"><template #default="{row,$index}"><el-input-number v-model="row.quantity" :min="1" size="small" /></template></el-table-column>
        <el-table-column label="操作" width="80"><template #default="{$index}"><el-button link type="danger" size="small" @click="form.items.splice($index,1)">删除</el-button></template></el-table-column>
      </el-table>
      <div style="margin-top:16px;display:flex;justify-content:space-between;">
        <span>共{{form.items.length}}种，总计{{totalQty}}</span>
        <div><el-button @click="$router.back()">取消</el-button><el-button type="primary" :loading="submitting" @click="submit">提交</el-button></div>
      </div>
    </el-card>
    <GoodsSelectorDialog v-model="showSelector" @confirm="addGoods" />
  </div>
</template>

<script setup lang="ts">
import { ref,reactive,computed,onMounted } from 'vue';import { ElMessage } from 'element-plus';import { asnApi } from '@/api/asn';import { supplierApi } from '@/api/supplier';import { warehouseApi } from '@/api/warehouse';import GoodsSelectorDialog from '@/components/common/GoodsSelectorDialog.vue'
const submitting=ref(false),showSelector=ref(false),suppliers=ref<any[]>([]),warehouses=ref<any[]>([])
const form=reactive<any>({supplier:'',warehouse:'',items:[]})
const totalQty=computed(()=>form.items.reduce((s:number,i:any)=>s+(i.quantity||0),0))
async function loadOptions(){suppliers.value=((await supplierApi.simple())as any)?.data||[];warehouses.value=((await warehouseApi.simple())as any)?.data||[]}
function addGoods(sel:any[]){for(const g of sel){if(!form.items.find((i:any)=>i.goods===g.id))form.items.push({goods:g.id,goods_code:g.code,goods_name:g.name,quantity:1})}}
async function submit(){if(!form.supplier||!form.warehouse||!form.items.length){ElMessage.warning('请完善信息');return};submitting.value=true;try{await asnApi.create({supplier:form.supplier,warehouse:form.warehouse,items:form.items.map((i:any)=>({goods:i.goods,quantity:i.quantity}))});ElMessage.success('创建成功');history.back()}finally{submitting.value=false}}
onMounted(loadOptions)
</script>
