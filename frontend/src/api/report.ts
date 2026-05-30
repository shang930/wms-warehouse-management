import request from '@/utils/request'
export const reportApi = {
  dashboard: (params?:any)=>request.get('/reports/dashboard/', params),
  inbound: (params?:any)=>request.get('/reports/inbound/', params),
  outbound: (params?:any)=>request.get('/reports/outbound/', params),
  inventory: (params?:any)=>request.get('/reports/inventory/', params),
  summary: (params?:any)=>request.get('/reports/summary/', params),
}
