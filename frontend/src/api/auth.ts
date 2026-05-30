import request from '@/utils/request'
export function login(data: { username: string; password: string }) { return request.post('/auth/login/', data) }
export function getCurrentUser() { return request.get('/auth/me/') }
export function changePassword(data: any) { return request.post('/auth/change-password/', data) }
