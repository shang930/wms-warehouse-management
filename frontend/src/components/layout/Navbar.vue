<template>
  <div class="navbar">
    <div class="navbar-left">
      <el-icon class="collapse-btn" @click="appStore.toggleSidebar()"><Fold v-if="!appStore.sidebarCollapsed" /><Expand v-else /></el-icon>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item v-if="matched.length > 1">{{ matched[0]?.meta?.title || '' }}</el-breadcrumb-item>
        <el-breadcrumb-item>{{ matched[matched.length - 1]?.meta?.title || '' }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="navbar-right">
      <el-tooltip content="全屏"><el-icon class="action-icon" @click="toggleFullScreen"><FullScreen /></el-icon></el-tooltip>
      <el-dropdown trigger="click" @command="handleCommand">
        <div class="user-info">
          <el-avatar :size="32">{{ userStore.userInfo?.first_name?.[0] || userStore.userInfo?.username?.[0] || 'U' }}</el-avatar>
          <span class="username">{{ userStore.userInfo?.first_name || userStore.userInfo?.username || '' }}</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="password">修改密码</el-dropdown-item>
            <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/store/modules/app'
import { useUserStore } from '@/store/modules/user'

const route = useRoute()
const appStore = useAppStore()
const userStore = useUserStore()
const matched = computed(() => route.matched)

function toggleFullScreen() { if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen() }
function handleCommand(cmd: string) { if (cmd === 'logout') userStore.logout() }
</script>

<style lang="scss" scoped>
.navbar { height: var(--navbar-height); background: #fff; display: flex; align-items: center; justify-content: space-between; padding: 0 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); z-index: 999; }
.navbar-left,.navbar-right { display: flex; align-items: center; gap: 12px; }
.collapse-btn { font-size: 20px; cursor: pointer; color: #606266; &:hover{color:var(--color-primary);} }
.action-icon { font-size: 18px; color: #606266; cursor: pointer; padding: 6px; border-radius: 4px; &:hover{background:#f5f5f5;color:var(--color-primary);} }
.user-info { display: flex; align-items: center; gap: 8px; cursor: pointer; padding: 4px 8px; border-radius: 6px; &:hover{background:#f5f5f5;} .username{font-size:14px;color:#303133;} }
</style>
