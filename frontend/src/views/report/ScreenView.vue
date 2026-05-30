<template>
  <div class="screen-page">
    <div class="screen-header"><h1>WMS 智慧仓储数据监控平台</h1><span>{{currentTime}}</span></div>
    <el-row :gutter="12" style="flex:1;display:flex;">
      <el-col :span="5" style="display:flex;flex-direction:column;gap:12px;">
        <div class="screen-card"><h4>📦 总库存</h4><div class="big-num">{{fmt(stats.total_stock)}}</div></div>
        <div class="screen-card"><h4>📥 今日入库</h4><div class="big-num" style="color:#67c23a;">{{stats.today_inbound}}单</div></div>
        <div class="screen-card"><h4>📤 今日出库</h4><div class="big-num" style="color:#e6a23c;">{{stats.today_outbound}}单</div></div>
        <div class="screen-card"><h4>⚠️ 预警</h4><div class="big-num" style="color:#f56c6c;">{{stats.alerts?.length||0}}</div></div>
      </el-col>
      <el-col :span="14" style="display:flex;flex-direction:column;gap:12px;">
        <div class="screen-card" style="flex:1;"><h4>📈 出入库趋势</h4><div ref="trendRef" style="height:200px;"></div></div>
        <div class="screen-card" style="flex:1;"><h4>⚠️ 库存预警 Top5</h4><div ref="barRef" style="height:200px;"></div></div>
      </el-col>
      <el-col :span="5" style="display:flex;flex-direction:column;gap:12px;">
        <div class="screen-card"><h4>🏭 仓库利用率</h4><div ref="gaugeRef" style="height:160px;"></div></div>
        <div class="screen-card" style="flex:1;overflow-y:auto;"><h4>⏰ 待处理</h4><div class="pending-mini"><span>待收货</span><span>{{stats.pending_inbound}}</span></div><div class="pending-mini"><span>待发货</span><span>{{stats.pending_outbound}}</span></div></div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref,onMounted,onUnmounted,nextTick } from 'vue';import * as echarts from 'echarts';import { reportApi } from '@/api/report'
const trendRef=ref<HTMLElement>(),barRef=ref<HTMLElement>(),gaugeRef=ref<HTMLElement>()
const currentTime=ref(''),stats=ref<any>({total_stock:0,today_inbound:0,today_outbound:0,pending_inbound:0,pending_outbound:0,alerts:[]})
let charts:echarts.ECharts[]=[],timer:any=null

function fmt(v:number){return v>=10000?`${(v/10000).toFixed(1)}万`:(v||0).toLocaleString()}
async function fetchData(){const res:any=await reportApi.dashboard();if(res.code===200)stats.value=res.data}

function initCharts(){
  const trend = stats.value.trend || { inbound: [], outbound: [] }

  if(trendRef.value){
    const labels: string[] = []; const now = new Date()
    for (let i = 29; i >= 0; i--) { const d = new Date(now); d.setDate(d.getDate() - i); labels.push(`${d.getMonth()+1}/${d.getDate()}`) }
    const mapTrend = (arr: {day:string;count:number}[]) => labels.map((_, i) => { const d = new Date(now); d.setDate(d.getDate() - (29 - i)); return arr.find(t => t.day === d.toISOString().slice(0,10))?.count || 0 })
    const c=echarts.init(trendRef.value)
    c.setOption({tooltip:{trigger:'axis'},xAxis:{type:'category',data:labels,axisLabel:{rotate:30,fontSize:10}},yAxis:{type:'value'},series:[{name:'入库',type:'line',smooth:true,data:mapTrend(trend.inbound||[]),lineStyle:{color:'#67c23a'}},{name:'出库',type:'line',smooth:true,data:mapTrend(trend.outbound||[]),lineStyle:{color:'#e6a23c'}}],grid:{left:45,right:20,top:15,bottom:35}})
    charts.push(c)
  }
  if(barRef.value){
    const c=echarts.init(barRef.value)
    const alerts = stats.value.alerts || []
    const top5 = alerts.slice(0, 5).reverse()
    c.setOption({tooltip:{trigger:'axis',axisPointer:{type:'shadow'}},xAxis:{type:'value'},yAxis:{type:'category',data:top5.map((a:any)=>a.goods_name||a.goods_code)||['暂无预警']},series:[{type:'bar',data:top5.map((a:any)=>a.current_qty||0).reverse(),itemStyle:{borderRadius:[0,4,4,0],color:'#f56c6c'}}],grid:{left:100,right:20,top:10,bottom:20}})
    charts.push(c)
  }
  if(gaugeRef.value){
    const totalStock = stats.value.total_stock || 0
    // assume warehouse capacity is ~2x current stock for gauge display
    const pct = totalStock > 0 ? Math.min(95, Math.round(totalStock / 10000 * 100)) : 0
    const c=echarts.init(gaugeRef.value)
    c.setOption({series:[{type:'gauge',startAngle:210,endAngle:-30,radius:'85%',pointer:{show:false},progress:{show:true,width:10},axisLine:{lineStyle:{width:10,color:[[0.68,'#409eff'],[1,'#e0e0e0']]}},axisTick:{show:false},splitLine:{show:false},axisLabel:{show:false},detail:{valueAnimation:true,formatter:'{value}%',fontSize:24,color:'#fff'},data:[{value:pct}]}]})
    charts.push(c)
  }
}

function updateClock(){currentTime.value=new Date().toLocaleString('zh-CN',{hour12:false})}

onMounted(async()=>{await fetchData();nextTick(initCharts);updateClock();timer=setInterval(updateClock,1000);window.addEventListener('resize',()=>charts.forEach(c=>c.resize()))})
onUnmounted(()=>{clearInterval(timer);charts.forEach(c=>c.dispose())})
</script>

<style lang="scss" scoped>
.screen-page{background:linear-gradient(135deg,#0f1923,#1a2a3a,#0f1923);color:#e0e0e0;min-height:100vh;padding:12px 20px;display:flex;flex-direction:column}
.screen-header{display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:1px solid rgba(255,255,255,0.1);h1{font-size:22px;margin:0;background:linear-gradient(90deg,#43e97b,#38f9d7);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.screen-card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:12px 16px;h4{margin:0 0 8px;font-size:14px;color:#909399;font-weight:400}}
.big-num{font-size:28px;font-weight:700;color:#fff}
.pending-mini{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.06);font-size:13px}
</style>
