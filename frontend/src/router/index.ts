import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import NProgress from 'nprogress'
import AppLayout from '@/components/layout/AppLayout.vue'

const LoginView = () => import('@/views/login/LoginView.vue')
const DashboardView = () => import('@/views/dashboard/DashboardView.vue')
const GoodsList = () => import('@/views/goods/GoodsList.vue')
const WarehouseList = () => import('@/views/warehouse/WarehouseList.vue')
const SupplierList = () => import('@/views/supplier/SupplierList.vue')
const CustomerList = () => import('@/views/customer/CustomerList.vue')
const StockOverview = () => import('@/views/stock/StockOverview.vue')
const StockLocation = () => import('@/views/stock/StockLocation.vue')
const StockMovementList = () => import('@/views/stock/StockMovementList.vue')
const ASNList = () => import('@/views/asn/ASNList.vue')
const ASNCreate = () => import('@/views/asn/ASNCreate.vue')
const ASNDetail = () => import('@/views/asn/ASNDetail.vue')
const DNList = () => import('@/views/dn/DNList.vue')
const DNCreate = () => import('@/views/dn/DNCreate.vue')
const DNDetail = () => import('@/views/dn/DNDetail.vue')
const CycleCountList = () => import('@/views/cyclecount/CycleCountList.vue')
const ReportInbound = () => import('@/views/report/ReportInbound.vue')
const ReportOutbound = () => import('@/views/report/ReportOutbound.vue')
const ReportInventory = () => import('@/views/report/ReportInventory.vue')
const ReportScreen = () => import('@/views/report/ScreenView.vue')
const UserList = () => import('@/views/system/user/UserList.vue')
const RoleList = () => import('@/views/system/role/RoleList.vue')
const DeptList = () => import('@/views/system/dept/DeptList.vue')
const MenuList = () => import('@/views/system/menu/MenuList.vue')

export const constantRoutes: RouteRecordRaw[] = [
  { path: '/login', name: 'Login', component: LoginView, meta: { title: '登录', hidden: true } },
  { path: '/', component: AppLayout, redirect: '/dashboard',
    children: [{ path: 'dashboard', name: 'Dashboard', component: DashboardView, meta: { title: '仪表盘', icon: 'Odometer' } }] },
]

export const asyncRoutes: RouteRecordRaw[] = [
  { path: '/goods', component: AppLayout, meta: { title: '商品管理', icon: 'Goods' },
    children: [
      { path: 'list', name: 'GoodsList', component: GoodsList, meta: { title: '商品列表' } },
      { path: 'data', name: 'GoodsData', component: () => import('@/views/goods/GoodsDataManage.vue'), meta: { title: '基础数据', hidden: true } },
    ] },
  { path: '/warehouse', component: AppLayout, meta: { title: '仓库管理', icon: 'Box' },
    children: [
      { path: 'list', name: 'WarehouseList', component: WarehouseList, meta: { title: '仓库列表' } },
      { path: 'zone', name: 'ZoneList', component: () => import('@/views/warehouse/ZoneList.vue'), meta: { title: '库区管理' } },
      { path: 'bin', name: 'BinList', component: () => import('@/views/warehouse/BinList.vue'), meta: { title: '库位管理' } },
    ] },
  { path: '/supplier', component: AppLayout, meta: { title: '供应商管理', icon: 'Avatar' },
    children: [{ path: 'list', name: 'SupplierList', component: SupplierList, meta: { title: '供应商列表' } }] },
  { path: '/customer', component: AppLayout, meta: { title: '客户管理', icon: 'UserFilled' },
    children: [{ path: 'list', name: 'CustomerList', component: CustomerList, meta: { title: '客户列表' } }] },
  { path: '/asn', component: AppLayout, meta: { title: '入库管理', icon: 'Upload' },
    children: [
      { path: 'list', name: 'ASNList', component: ASNList, meta: { title: '入库单列表' } },
      { path: 'create', name: 'ASNCreate', component: ASNCreate, meta: { title: '创建入库单', hidden: true } },
      { path: 'detail/:id', name: 'ASNDetail', component: ASNDetail, meta: { title: '入库单详情', hidden: true } },
    ] },
  { path: '/dn', component: AppLayout, meta: { title: '出库管理', icon: 'Download' },
    children: [
      { path: 'list', name: 'DNList', component: DNList, meta: { title: '出库单列表' } },
      { path: 'create', name: 'DNCreate', component: DNCreate, meta: { title: '创建出库单', hidden: true } },
      { path: 'detail/:id', name: 'DNDetail', component: DNDetail, meta: { title: '出库单详情', hidden: true } },
    ] },
  { path: '/stock', component: AppLayout, meta: { title: '库存管理', icon: 'Histogram' },
    children: [
      { path: 'overview', name: 'StockOverview', component: StockOverview, meta: { title: '库存总览' } },
      { path: 'location', name: 'StockLocation', component: StockLocation, meta: { title: '库位库存' } },
      { path: 'movement', name: 'StockMovement', component: StockMovementList, meta: { title: '库存流水' } },
    ] },
  { path: '/cyclecount', component: AppLayout, meta: { title: '盘点管理', icon: 'Check' },
    children: [
      { path: 'list', name: 'CycleCountList', component: CycleCountList, meta: { title: '盘点列表' } },
      { path: 'detail/:id', name: 'CycleCountDetail', component: () => import('@/views/cyclecount/CycleCountDetail.vue'), meta: { title: '盘点详情', hidden: true } },
    ] },
  { path: '/report', component: AppLayout, meta: { title: '报表中心', icon: 'DataAnalysis' },
    children: [
      { path: 'inbound', name: 'ReportInbound', component: ReportInbound, meta: { title: '入库报表' } },
      { path: 'outbound', name: 'ReportOutbound', component: ReportOutbound, meta: { title: '出库报表' } },
      { path: 'inventory', name: 'ReportInventory', component: ReportInventory, meta: { title: '库存报表' } },
      { path: 'screen', name: 'ReportScreen', component: ReportScreen, meta: { title: '数据大屏' } },
    ] },
  { path: '/system', component: AppLayout, meta: { title: '系统管理', icon: 'Setting' },
    children: [
      { path: 'user', name: 'UserList', component: UserList, meta: { title: '用户管理' } },
      { path: 'role', name: 'RoleList', component: RoleList, meta: { title: '角色管理' } },
      { path: 'dept', name: 'DeptList', component: DeptList, meta: { title: '部门管理' } },
      { path: 'menu', name: 'MenuList', component: MenuList, meta: { title: '菜单管理' } },
      { path: 'log', name: 'LogList', component: () => import('@/views/system/log/LogList.vue'), meta: { title: '操作日志' } },
    ] },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes: [...constantRoutes, ...asyncRoutes],
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach(async (to, _from, next) => {
  NProgress.start()
  if (to.path === '/login') { next(); return }
  const { useUserStore } = await import('@/store/modules/user')
  const userStore = useUserStore()
  if (!userStore.token) { next('/login'); return }
  if (!userStore.userInfo) await userStore.fetchUserInfo()
  next()
})

router.afterEach(() => { NProgress.done() })
export default router
