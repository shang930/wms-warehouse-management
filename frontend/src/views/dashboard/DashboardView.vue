<template>
  <div class="dashboard">
    <div class="stat-cards">
      <div class="stat-card"><div class="stat-info"><h3>商品总数</h3><div class="stat-value">{{ stats.total_goods }}</div></div><div class="stat-icon" style="background:linear-gradient(135deg,#667eea,#764ba2);"><el-icon :size="28"><Goods /></el-icon></div></div>
      <div class="stat-card"><div class="stat-info"><h3>今日入库</h3><div class="stat-value">{{ stats.today_inbound }} <span style="font-size:16px;font-weight:400;">单</span></div></div><div class="stat-icon" style="background:linear-gradient(135deg,#43e97b,#38f9d7);"><el-icon :size="28"><Upload /></el-icon></div></div>
      <div class="stat-card"><div class="stat-info"><h3>今日出库</h3><div class="stat-value">{{ stats.today_outbound }} <span style="font-size:16px;font-weight:400;">单</span></div></div><div class="stat-icon" style="background:linear-gradient(135deg,#f093fb,#f5576c);"><el-icon :size="28"><Download /></el-icon></div></div>
      <div class="stat-card"><div class="stat-info"><h3>库存预警</h3><div class="stat-value" style="color:var(--color-danger);">{{ stats.alerts?.length || 0 }}</div></div><div class="stat-icon" style="background:linear-gradient(135deg,#fa709a,#fee140);"><el-icon :size="28"><WarningFilled /></el-icon></div></div>
    </div>
    <el-row :gutter="16" style="margin-bottom:16px;">
      <el-col :span="14"><el-card shadow="never"><template #header><span>📈 近30天出入库趋势</span></template><div ref="trendRef" style="height:320px;"></div></el-card></el-col>
      <el-col :span="10"><el-card shadow="never"><template #header><span>⏰ 待处理</span></template><div class="pending-list"><div class="pending-item"><span>待收货入库单</span><el-tag type="warning" size="large">{{ stats.pending_inbound }}</el-tag></div><div class="pending-item"><span>待发货出库单</span><el-tag type="warning" size="large">{{ stats.pending_outbound }}</el-tag></div><div class="pending-item"><span>库存不足预警</span><el-tag type="danger" size="large">{{ stats.alerts?.length || 0 }}</el-tag></div></div></el-card></el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { reportApi } from '@/api/report'

const trendRef = ref<HTMLElement>()
let trendChart: echarts.ECharts | null = null
const stats = ref<any>({ total_goods:0, total_stock:0, today_inbound:0, today_outbound:0, pending_inbound:0, pending_outbound:0, alerts:[] })

async function fetchStats() { const res: any = await reportApi.dashboard(); if (res.code === 200) stats.value = res.data }

function initChart() {
  if (!trendRef.value) return
  trendChart = echarts.init(trendRef.value)
  trendChart.setOption({
    tooltip: { trigger: 'axis' }, legend: { data: ['入库', '出库'] },
    xAxis: { type: 'category', data: Array.from({length:30},(_,i)=>`${i+1}日`) },
    yAxis: { type: 'value' },
    series: [
      { name:'入库',type:'line',smooth:true,data:Array.from({length:30},()=>Math.floor(Math.random()*25+5)),lineStyle:{color:'#67c23a'},itemStyle:{color:'#67c23a'} },
      { name:'出库',type:'line',smooth:true,data:Array.from({length:30},()=>Math.floor(Math.random()*20+5)),lineStyle:{color:'#e6a23c'},itemStyle:{color:'#e6a23c'} },
    ],
    grid: { left:50, right:20, top:30, bottom:30 },
  })
}

function handleResize() { trendChart?.resize() }
onMounted(async () => { await fetchStats(); nextTick(initChart); window.addEventListener('resize', handleResize) })
onUnmounted(() => { window.removeEventListener('resize', handleResize); trendChart?.dispose() })
</script>

<style lang="scss" scoped>
.pending-list { .pending-item { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; &:not(:last-child){border-bottom:1px solid #f0f0f0;} } }
</style>
