import request from '@/utils/request'
export const cycleCountApi = {
  list: (params?:any)=>request.get('/cyclecount/', params),
  detail: (id:string)=>request.get(`/cyclecount/${id}/`),
  create: (data:any)=>request.post('/cyclecount/', data),
  start: (id:string)=>request.post(`/cyclecount/${id}/start/`),
  complete: (id:string,data:any)=>request.post(`/cyclecount/${id}/complete/`, data),
  adjust: (id:string)=>request.post(`/cyclecount/${id}/adjust/`),
}
