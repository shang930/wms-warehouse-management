import request from '@/utils/request'
export const customerApi = {
  list: (params?:any)=>request.get('/customers/', params),
  simple: ()=>request.get('/customers/simple/'),
  create: (data:any)=>request.post('/customers/', data),
  update: (id:string,data:any)=>request.put(`/customers/${id}/`, data),
  remove: (id:string)=>request.delete(`/customers/${id}/`),
}
