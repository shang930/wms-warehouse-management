<template>
  <div class="sidebar" :class="{ collapsed: appStore.sidebarCollapsed }">
    <div class="logo"><el-icon :size="24"><Box /></el-icon><span v-show="!appStore.sidebarCollapsed" class="logo-text">WMS 仓储系统</span></div>
    <el-scrollbar>
      <el-menu :default-active="route.path" :collapse="appStore.sidebarCollapsed" :collapse-transition="false" :unique-opened="true" background-color="#304156" text-color="#bfcbd9" active-text-color="#409eff" router>
        <template v-for="menu in menuList" :key="menu.id">
          <template v-if="menu.children && menu.children.length === 1">
            <el-menu-item :index="menu.children[0].path">
              <el-icon><component :is="menu.icon" /></el-icon>
              <template #title>{{ menu.name }}</template>
            </el-menu-item>
          </template>
          <el-sub-menu v-else-if="menu.children && menu.children.length > 1" :index="menu.id">
            <template #title><el-icon><component :is="menu.icon || 'FolderOpened'" /></el-icon><span>{{ menu.name }}</span></template>
            <el-menu-item v-for="child in menu.children" :key="child.id" :index="child.path">{{ child.name }}</el-menu-item>
          </el-sub-menu>
        </template>
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useAppStore } from '@/store/modules/app'

const route = useRoute()
const appStore = useAppStore()

const menuList = [
  { id: '1', name: '仪表盘', icon: 'Odometer', children: [{ id: '1-1', name: '仪表盘', path: '/dashboard' }] },
  { id: '2', name: '商品管理', icon: 'Goods', children: [{ id: '2-1', name: '商品列表', path: '/goods/list' }] },
  { id: '3', name: '仓库管理', icon: 'Box', children: [{ id: '3-1', name: '仓库列表', path: '/warehouse/list' }] },
  { id: '4', name: '供应商管理', icon: 'Avatar', children: [{ id: '4-1', name: '供应商列表', path: '/supplier/list' }] },
  { id: '5', name: '客户管理', icon: 'UserFilled', children: [{ id: '5-1', name: '客户列表', path: '/customer/list' }] },
  { id: '6', name: '入库管理', icon: 'Upload', children: [{ id: '6-1', name: '入库单列表', path: '/asn/list' }, { id: '6-2', name: '创建入库单', path: '/asn/create' }] },
  { id: '7', name: '出库管理', icon: 'Download', children: [{ id: '7-1', name: '出库单列表', path: '/dn/list' }, { id: '7-2', name: '创建出库单', path: '/dn/create' }] },
  { id: '8', name: '库存管理', icon: 'Histogram', children: [{ id: '8-1', name: '库存总览', path: '/stock/overview' }, { id: '8-2', name: '库位库存', path: '/stock/location' }, { id: '8-3', name: '库存流水', path: '/stock/movement' }] },
  { id: '9', name: '盘点管理', icon: 'Check', children: [{ id: '9-1', name: '盘点列表', path: '/cyclecount/list' }] },
  { id: '10', name: '报表中心', icon: 'DataAnalysis', children: [{ id: '10-1', name: '入库报表', path: '/report/inbound' }, { id: '10-2', name: '出库报表', path: '/report/outbound' }, { id: '10-3', name: '库存报表', path: '/report/inventory' }, { id: '10-4', name: '数据大屏', path: '/report/screen' }] },
  { id: '11', name: '系统管理', icon: 'Setting', children: [{ id: '11-1', name: '用户管理', path: '/system/user' }, { id: '11-2', name: '角色管理', path: '/system/role' }, { id: '11-3', name: '部门管理', path: '/system/dept' }] },
]
</script>

<style lang="scss" scoped>
.sidebar { position: fixed; left: 0; top: 0; bottom: 0; width: var(--sidebar-width); background: #304156; z-index: 1001; transition: width 0.3s ease; overflow: hidden; &.collapsed { width: 64px; } }
.logo { height: var(--navbar-height); display: flex; align-items: center; justify-content: center; gap: 8px; color: #fff; font-size: 18px; font-weight: 600; border-bottom: 1px solid rgba(255,255,255,0.1); white-space: nowrap; }
.logo-text { font-size: 16px; }
.el-menu { border-right: none; }
.el-scrollbar { height: calc(100vh - var(--navbar-height)); }
</style>
