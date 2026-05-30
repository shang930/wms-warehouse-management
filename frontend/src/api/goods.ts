import request from '@/utils/request'
export const goodsApi = {
  list: (params?:any)=>request.get('/goods/', params),
  simple: ()=>request.get('/goods/simple/'),
  create: (data:any)=>request.post('/goods/', data),
  update: (id:string,data:any)=>request.put(`/goods/${id}/`, data),
  remove: (id:string)=>request.delete(`/goods/${id}/`),
}
export const categoryApi = {
  list: (params?:any)=>request.get('/goods/categories/', params),
  tree: ()=>request.get('/goods/categories/tree/'),
  create: (data:any)=>request.post('/goods/categories/', data),
  update: (id:string,data:any)=>request.put(`/goods/categories/${id}/`, data),
  remove: (id:string)=>request.delete(`/goods/categories/${id}/`),
}
export const unitApi = {
  list: (params?:any)=>request.get('/goods/units/', params),
  create: (data:any)=>request.post('/goods/units/', data),
  update: (id:string,data:any)=>request.put(`/goods/units/${id}/`, data),
  remove: (id:string)=>request.delete(`/goods/units/${id}/`),
}
