<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header"><h1>WMS 仓库管理系统</h1><p>Warehouse Management System</p></div>
      <el-form ref="formRef" :model="form" :rules="rules" size="large" @keyup.enter="handleLogin">
        <el-form-item prop="username"><el-input v-model="form.username" placeholder="用户名" /></el-form-item>
        <el-form-item prop="password"><el-input v-model="form.password" type="password" placeholder="密码" show-password /></el-form-item>
        <el-form-item><el-button type="primary" :loading="loading" class="login-btn" @click="handleLogin">{{ loading ? '登录中...' : '登 录' }}</el-button></el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, FormInstance } from 'element-plus'
import { useUserStore } from '@/store/modules/user'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const form = reactive({ username: 'admin', password: 'admin123' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function handleLogin() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try { const ok = await userStore.login(form.username, form.password); if (ok) { ElMessage.success('登录成功'); router.push('/dashboard') } }
  finally { loading.value = false }
}
</script>

<style lang="scss" scoped>
.login-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.login-card { width: 400px; padding: 48px 40px 32px; background: #fff; border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,0.15); }
.login-header { text-align: center; margin-bottom: 36px; h1 { font-size: 24px; color: #303133; margin: 0 0 8px; } p { font-size: 13px; color: #909399; margin: 0; } }
.login-btn { width: 100%; }
</style>
