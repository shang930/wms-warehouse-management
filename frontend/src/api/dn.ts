import request from '@/utils/request'
export const dnApi = {
  list: (params?:any)=>request.get('/dn/', params),
  detail: (id:string)=>request.get(`/dn/${id}/`),
  create: (data:any)=>request.post('/dn/', data),
  update: (id:string,data:any)=>request.put(`/dn/${id}/`, data),
  remove: (id:string)=>request.delete(`/dn/${id}/`),
  changeStatus: (id:string,data:{status:number;items?:any[];tracking_no?:string})=>request.patch(`/dn/${id}/status/`, data),
}
