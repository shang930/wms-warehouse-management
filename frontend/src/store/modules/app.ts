import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false)
  const themeMode = ref<'light' | 'dark'>('light')
  function toggleSidebar() { sidebarCollapsed.value = !sidebarCollapsed.value }
  function setTheme(mode: 'light' | 'dark') { themeMode.value = mode; document.documentElement.setAttribute('data-theme', mode) }
  return { sidebarCollapsed, themeMode, toggleSidebar, setTheme }
})
