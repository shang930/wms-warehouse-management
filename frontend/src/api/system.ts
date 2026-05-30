import request from '@/utils/request'
export const userApi = {
  list: (params?:any)=>request.get('/users/', params),
  create: (data:any)=>request.post('/users/', data),
  update: (id:string,data:any)=>request.put(`/users/${id}/`, data),
  remove: (id:string)=>request.delete(`/users/${id}/`),
  batchStatus: (data:any)=>request.put('/users/batch-status/', data),
}
export const roleApi = {
  list: (params?:any)=>request.get('/users/roles/', params),
  create: (data:any)=>request.post('/users/roles/', data),
  update: (id:string,data:any)=>request.put(`/users/roles/${id}/`, data),
  remove: (id:string)=>request.delete(`/users/roles/${id}/`),
  allMenus: ()=>request.get('/users/roles/all_menus/'),
}
export const deptApi = {
  list: (params?:any)=>request.get('/users/departments/', params),
  tree: ()=>request.get('/users/departments/tree/'),
  create: (data:any)=>request.post('/users/departments/', data),
  update: (id:string,data:any)=>request.put(`/users/departments/${id}/`, data),
  remove: (id:string)=>request.delete(`/users/departments/${id}/`),
}
export const menuApi = {
  list: (params?:any)=>request.get('/users/menus/', params),
  tree: ()=>request.get('/users/menus/tree/'),
  userMenus: ()=>request.get('/users/menus/user_menus/'),
  create: (data:any)=>request.post('/users/menus/', data),
  update: (id:string,data:any)=>request.put(`/users/menus/${id}/`, data),
  remove: (id:string)=>request.delete(`/users/menus/${id}/`),
}
