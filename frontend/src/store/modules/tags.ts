import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { RouteLocationNormalized } from 'vue-router'

interface TagItem { path: string; name: string; title: string; affix?: boolean }

export const useTagsStore = defineStore('tags', () => {
  const visitedTags = ref<TagItem[]>([{ path: '/dashboard', name: 'Dashboard', title: '仪表盘', affix: true }])
  const activeTag = ref('/dashboard')

  function addTag(route: RouteLocationNormalized) {
    if (!visitedTags.value.find(t => t.path === route.path)) {
      visitedTags.value.push({ path: route.path, name: route.name as string, title: route.meta?.title as string || route.name as string })
    }
    activeTag.value = route.path
  }

  function removeTag(path: string) {
    const idx = visitedTags.value.findIndex(t => t.path === path)
    if (idx === -1 || visitedTags.value[idx].affix) return
    visitedTags.value.splice(idx, 1)
    if (activeTag.value === path) { const last = visitedTags.value[visitedTags.value.length - 1]; activeTag.value = last?.path || '/dashboard' }
  }

  function closeOtherTags(path: string) { visitedTags.value = visitedTags.value.filter(t => t.path === path || t.affix); activeTag.value = path }
  function closeAllTags() { visitedTags.value = visitedTags.value.filter(t => t.affix); activeTag.value = visitedTags.value[0]?.path || '/dashboard' }
  return { visitedTags, activeTag, addTag, removeTag, closeOtherTags, closeAllTags }
})
