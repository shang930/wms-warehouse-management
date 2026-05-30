import request from '@/utils/request'
export const warehouseApi = {
  list: (params?:any)=>request.get('/warehouses/', params),
  simple: ()=>request.get('/warehouses/simple/'),
  create: (data:any)=>request.post('/warehouses/', data),
  update: (id:string,data:any)=>request.put(`/warehouses/${id}/`, data),
  remove: (id:string)=>request.delete(`/warehouses/${id}/`),
}
export const zoneApi = {
  list: (params?:any)=>request.get('/warehouses/zones/', params),
  simple: (params?:any)=>request.get('/warehouses/zones/?page_size=500', params),
  create: (data:any)=>request.post('/warehouses/zones/', data),
  update: (id:string,data:any)=>request.put(`/warehouses/zones/${id}/`, data),
  remove: (id:string)=>request.delete(`/warehouses/zones/${id}/`),
}
export const binApi = {
  list: (params?:any)=>request.get('/warehouses/bins/', params),
  simple: (params?:any)=>request.get('/warehouses/bins/simple/', params),
  create: (data:any)=>request.post('/warehouses/bins/', data),
  update: (id:string,data:any)=>request.put(`/warehouses/bins/${id}/`, data),
  remove: (id:string)=>request.delete(`/warehouses/bins/${id}/`),
  batchCreate: (data:any)=>request.post('/warehouses/bins/batch_create/', data),
}
