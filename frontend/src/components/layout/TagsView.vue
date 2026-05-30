<template>
  <div class="tags-view">
    <el-scrollbar>
      <div class="tags-wrapper">
        <el-tag v-for="tag in tagsStore.visitedTags" :key="tag.path" :closable="!tag.affix" :effect="tagsStore.activeTag === tag.path ? 'dark' : 'plain'" size="default" @click="goTo(tag)" @close="closeTag(tag)">{{ tag.title }}</el-tag>
      </div>
    </el-scrollbar>
    <el-dropdown trigger="click" class="tags-dropdown">
      <el-button size="small" text>更多<el-icon><ArrowDown /></el-icon></el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="tagsStore.closeOtherTags(activeTag)">关闭其他</el-dropdown-item>
          <el-dropdown-item @click="tagsStore.closeAllTags()">关闭全部</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTagsStore } from '@/store/modules/tags'

const router = useRouter()
const tagsStore = useTagsStore()
const activeTag = computed(() => tagsStore.activeTag)

function goTo(tag: any) { router.push(tag.path) }
function closeTag(tag: any) { tagsStore.removeTag(tag.path); if (tagsStore.activeTag !== tag.path) return; router.push(tagsStore.activeTag) }
</script>

<style lang="scss" scoped>
.tags-view { height: var(--tags-view-height); background: #fff; display: flex; align-items: center; padding: 0 12px; border-bottom: 1px solid #e4e7ed; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.el-scrollbar { flex: 1; white-space: nowrap; overflow: hidden; }
.tags-wrapper { display: inline-flex; align-items: center; gap: 6px; padding: 4px 0; }
.el-tag { cursor: pointer; user-select: none; border-radius: 4px; }
.tags-dropdown { flex-shrink: 0; margin-left: 8px; border-left: 1px solid #e4e7ed; padding-left: 8px; }
</style>
