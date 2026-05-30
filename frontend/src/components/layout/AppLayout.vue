<template>
  <div class="app-layout">
    <Sidebar />
    <div class="main-area" :class="{ collapsed: appStore.sidebarCollapsed }">
      <Navbar />
      <TagsView />
      <div class="app-main">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAppStore } from '@/store/modules/app'
import Sidebar from './Sidebar.vue'
import Navbar from './Navbar.vue'
import TagsView from './TagsView.vue'

const appStore = useAppStore()
</script>

<style lang="scss" scoped>
.app-layout { display: flex; height: 100vh; overflow: hidden; }
.main-area { flex: 1; display: flex; flex-direction: column; margin-left: var(--sidebar-width); transition: margin-left 0.3s ease; overflow: hidden; &.collapsed { margin-left: 64px; } }
.app-main { flex: 1; overflow-y: auto; padding: 16px; background: #f0f2f5; }
</style>
