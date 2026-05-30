import request from '@/utils/request'
export const supplierApi = {
  list: (params?:any)=>request.get('/suppliers/', params),
  simple: ()=>request.get('/suppliers/simple/'),
  create: (data:any)=>request.post('/suppliers/', data),
  update: (id:string,data:any)=>request.put(`/suppliers/${id}/`, data),
  remove: (id:string)=>request.delete(`/suppliers/${id}/`),
}
