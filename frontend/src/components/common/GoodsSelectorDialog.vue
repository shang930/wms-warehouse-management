<template>
  <el-dialog v-model="visible" title="选择商品" width="700px">
    <div style="margin-bottom:16px;"><el-input v-model="keyword" placeholder="搜索商品..." clearable style="width:300px;" @input="searchGoods" /></div>
    <el-table v-loading="tableLoading" :data="goods" stripe @selection-change="(v:any[])=>{selected=v}" max-height="400">
      <el-table-column type="selection" width="50" /><el-table-column prop="code" label="编码" width="140" /><el-table-column prop="name" label="名称" />
    </el-table>
    <template #footer><el-button @click="visible=false">取消</el-button><el-button type="primary" @click="confirm">确定({{selected.length}})</el-button></template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { goodsApi } from '@/api/goods'

const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{(e:'update:modelValue',v:boolean):void;(e:'confirm',v:any[]):void}>()
const visible = computed({get:()=>props.modelValue,set:(v)=>emit('update:modelValue',v)})
const keyword=ref(''),goods=ref<any[]>([]),selected=ref<any[]>([]),tableLoading=ref(false)

async function searchGoods(){tableLoading.value=true;try{const res:any=await goodsApi.list({page_size:100,search:keyword.value,is_active:true});goods.value=res?.data||[]}finally{tableLoading.value=false}}

function confirm(){emit('confirm',selected.value);visible.value=false}
</script>
