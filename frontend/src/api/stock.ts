import request from '@/utils/request'
export const stockApi = {
  list: (params?:any)=>request.get('/stock/', params),
  overview: (params?:any)=>request.get('/stock/overview/', params),
  alerts: (params?:any)=>request.get('/stock/alerts/', params),
  move: (data:any)=>request.post('/stock/move/', data),
  movements: (params?:any)=>request.get('/stock/movements/', params),
}
