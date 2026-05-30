<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="report-header">
          <span>📤 出库报表</span>
          <div class="report-actions">
            <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" value-format="YYYY-MM-DD" size="small" style="width:260px;" />
            <el-select v-model="customerId" placeholder="客户" clearable size="small" style="width:160px;"><el-option v-for="c in customers" :key="c.id" :label="c.name" :value="c.id" /></el-select>
            <el-button type="primary" size="small" @click="fetchData">查询</el-button>
            <el-button size="small" @click="exportData">导出CSV</el-button>
          </div>
        </div>
      </template>
      <el-row :gutter="16" style="margin-bottom:16px;">
        <el-col :span="8"><div class="stat-card"><h4>出库总单数</h4><div class="stat-value">{{data.total_orders}}</div></div></el-col>
        <el-col :span="8"><div class="stat-card"><h4>出库总量</h4><div class="stat-value">{{data.total_quantity}}</div></div></el-col>
        <el-col :span="8"><div class="stat-card"><h4>客户数</h4><div class="stat-value">{{data.by_customer?.length||0}}</div></div></el-col>
      </el-row>
      <div ref="chartRef" style="height:300px;margin-bottom:16px;"></div>
      <el-table :data="data.by_customer||[]" border stripe>
        <el-table-column prop="customer__name" label="客户" />
        <el-table-column prop="count" label="出库单数" width="140" align="right" />
        <el-table-column prop="total_qty" label="出库总量" width="140" align="right" />
        <el-table-column label="占比" width="120" align="right">
          <template #default="{row}">{{((row.total_qty/(data.total_quantity||1))*100).toFixed(1)}}%</template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { reportApi } from '@/api/report'
import { customerApi } from '@/api/customer'
import { exportCSV } from '@/utils'

const dateRange=ref<[string,string]|null>(null)
const customerId=ref('')
const customers=ref<any[]>([])
const chartRef=ref<HTMLElement>()
let chart: echarts.ECharts|null=null
const data=ref<any>({total_orders:0,total_quantity:0,by_customer:[]})

async function fetchData(){
  const params:any={}
  if(dateRange.value){params.start_date=dateRange.value[0];params.end_date=dateRange.value[1]}
  if(customerId.value)params.customer_id=customerId.value
  const res:any=await reportApi.outbound(params)
  if(res.code===200){data.value=res.data;nextTick(renderChart)}
}

function renderChart(){
  if(!chartRef.value)return
  if(!chart)chart=echarts.init(chartRef.value)
  const items=data.value.by_customer||[]
  chart.setOption({
    tooltip:{trigger:'axis',axisPointer:{type:'shadow'}},
    xAxis:{type:'category',data:items.map((i:any)=>i.customer__name),axisLabel:{rotate:30}},
    yAxis:{type:'value'},
    series:[{name:'出库单数',type:'bar',data:items.map((i:any)=>i.count),itemStyle:{color:'#e6a23c'}}],
    grid:{left:60,right:20,top:20,bottom:80},
  })
}

function exportData(){
  const items=data.value.by_customer||[]
  exportCSV('出库报表',['客户','出库单数','出库总量','占比(%)'],
    items.map((i:any)=>[i.customer__name,i.count,i.total_qty,((i.total_qty/(data.value.total_quantity||1))*100).toFixed(1)]))
}

onMounted(async()=>{
  const r:any=await customerApi.simple();customers.value=r?.data||[]
  fetchData()
})
onUnmounted(()=>chart?.dispose())
</script>

<style lang="scss" scoped>
.report-header{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;}
.report-actions{display:flex;gap:8px;align-items:center;flex-wrap:wrap;}
</style>
