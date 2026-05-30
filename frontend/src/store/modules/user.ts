import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as apiLogin, getCurrentUser } from '@/api/auth'
import { setToken, removeToken } from '@/utils/auth'
import router from '@/router'

interface UserInfo {
  id: string; username: string; first_name: string; email: string
  phone: string; avatar: string | null
  department_info: { id: string; name: string; code: string } | null
  roles_info: { id: string; name: string }[]
}

export const useUserStore = defineStore('user', () => {
  const token = ref<string>('')
  const userInfo = ref<UserInfo | null>(null)

  async function login(username: string, password: string) {
    const res: any = await apiLogin({ username, password })
    if (res.code === 200) { token.value = res.data.access; userInfo.value = res.data.user; setToken(res.data.access); return true }
    return false
  }

  async function fetchUserInfo() {
    const res: any = await getCurrentUser()
    if (res.code === 200) userInfo.value = res.data
  }

  function logout() { token.value = ''; userInfo.value = null; removeToken(); router.push('/login') }

  return { token, userInfo, login, fetchUserInfo, logout }
}, { persist: { key: 'wms-user', storage: localStorage, paths: ['token'] } })
