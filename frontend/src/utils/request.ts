import axios, { AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/modules/user'

const service = axios.create({ baseURL: import.meta.env.VITE_API_BASE || '/api/v1', timeout: 30000 })

service.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const userStore = useUserStore()
  if (userStore.token) config.headers.Authorization = `Bearer ${userStore.token}`
  return config
}, (error) => Promise.reject(error))

service.interceptors.response.use(
  (response: AxiosResponse) => {
    const data = response.data
    if (response.status === 200 || response.status === 201) {
      if (data.code && data.code !== 200 && data.code !== 201) { ElMessage.error(data.message || '请求失败'); return Promise.reject(data) }
      return data
    }
    return data
  },
  (error) => {
    if (error.response) {
      const { status } = error.response
      if (status === 401) { ElMessage.error('登录已过期，请重新登录'); const userStore = useUserStore(); userStore.logout(); window.location.href = '/login' }
      else if (status === 403) ElMessage.error('没有权限执行此操作')
      else if (status === 500) ElMessage.error('服务器内部错误')
      else ElMessage.error(error.response.data?.message || '网络错误')
    } else ElMessage.error('网络连接失败，请检查网络')
    return Promise.reject(error)
  }
)

export default service
export function get<T=any>(url:string, params?:any):Promise<T> { return service.get(url, { params }) }
export function post<T=any>(url:string, data?:any):Promise<T> { return service.post(url, data) }
export function put<T=any>(url:string, data?:any):Promise<T> { return service.put(url, data) }
export function patch<T=any>(url:string, data?:any):Promise<T> { return service.patch(url, data) }
export function del<T=any>(url:string):Promise<T> { return service.delete(url) }
