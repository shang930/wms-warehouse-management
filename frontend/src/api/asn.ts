import request from '@/utils/request'
export const asnApi = {
  list: (params?:any)=>request.get('/asn/', params),
  detail: (id:string)=>request.get(`/asn/${id}/`),
  create: (data:any)=>request.post('/asn/', data),
  update: (id:string,data:any)=>request.put(`/asn/${id}/`, data),
  remove: (id:string)=>request.delete(`/asn/${id}/`),
  changeStatus: (id:string,data:{status:number;items?:any[]})=>request.patch(`/asn/${id}/status/`, data),
}
