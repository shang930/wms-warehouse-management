# WMS 仓库管理系统

[![Vue](https://img.shields.io/badge/Vue-3.4-4FC08D?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Element Plus](https://img.shields.io/badge/Element_Plus-2.7-409EFF?logo=element&logoColor=white)](https://element-plus.org/)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-A30000?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)

一个功能完整的现代化仓库管理系统（WMS），涵盖入库、出库、库存、盘点、资产、报表等核心仓储业务流程。

---

## ✨ 功能概览

| 模块 | 功能描述 |
|------|---------|
| 📊 **数据看板** | 实时统计卡片、30天出入库趋势图、待处理订单面板 |
| 📦 **商品管理** | 商品 CRUD、分类树、单位/品牌管理、条形码支持 |
| 🏭 **仓库管理** | 多仓库、库区、库位三级管理，支持行列层坐标定位 |
| 🚚 **入库管理** | ASN 四步流程：草稿 → 已到达 → 已卸载 → 已上架 |
| 📤 **出库管理** | DN 四步流程：草稿 → 已确认 → 已拣货 → 已发货 |
| 📋 **库存管理** | 实时库存列表、库存总览、库存移动、安全库存预警 |
| 🔄 **盘点管理** | 全流程盘点：创建 → 开始 → 记录 → 完成 → 调整 |
| 🏢 **供应商管理** | 供应商 CRUD（含联系人、银行、税务信息） |
| 👥 **客户管理** | 客户 CRUD（含收货地址） |
| 🏗️ **资产管理** | 资产与托盘管理 |
| 📈 **报表中心** | 入库/出库/库存报表、综合汇总、数据大屏 |
| ⚙️ **系统管理** | 用户、角色、部门、菜单权限、操作日志 |

### 🎨 特色亮点

- 🔐 **JWT 认证**：8小时 Access Token + 7天 Refresh Token，自动续期
- 📡 **WebSocket 实时推送**：库存变动和安全预警即时通知
- 📱 **响应式布局**：适配桌面端与移动端
- 🌐 **动态菜单**：基于角色的动态菜单加载
- 🧭 **多标签页导航**：支持标签页打开、关闭、刷新
- 🗑️ **软删除**：关键数据软删除机制，可恢复
- 🆔 **UUID 主键**：所有模型使用 UUID v4 作为主键
- 📄 **API 文档**：自动生成 Swagger + ReDoc 接口文档
- 📊 **Excel 导出**：报表支持导出为 Excel 文件
- 📷 **条码生成**：内置商品条码生成功能

---

## 🏗️ 技术栈

### 前端

| 技术 | 版本 | 说明 |
|------|------|------|
| [Vue 3](https://vuejs.org/) | ^3.4.27 | 渐进式前端框架 (Composition API) |
| [TypeScript](https://www.typescriptlang.org/) | ^5.4.5 | 类型安全 |
| [Vite](https://vitejs.dev/) | ^5.2.12 | 极速构建工具 |
| [Element Plus](https://element-plus.org/) | ^2.7.5 | 企业级 UI 组件库 |
| [Pinia](https://pinia.vuejs.org/) | ^2.1.7 | 轻量级状态管理 |
| [Vue Router](https://router.vuejs.org/) | ^4.3.2 | 路由管理 (Hash 模式) |
| [ECharts](https://echarts.apache.org/) | ^5.5.0 | 可视化图表 |
| [Axios](https://axios-http.com/) | ^1.7.2 | HTTP 客户端 |
| [dayjs](https://day.js.org/) | ^1.11.11 | 日期处理 |

### 后端

| 技术 | 版本 | 说明 |
|------|------|------|
| [Django](https://www.djangoproject.com/) | 4.2 | Web 框架 |
| [Django REST Framework](https://www.django-rest-framework.org/) | 3.14 | RESTful API 框架 |
| [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/) | 5.3 | JWT 认证 |
| [Django Channels](https://channels.readthedocs.io/) | 4.0 | WebSocket 支持 |
| [Celery](https://docs.celeryq.dev/) | 5.3 | 异步任务队列 |
| [Redis](https://redis.io/) | 5.0 | 缓存 & 消息代理 |
| [PostgreSQL](https://www.postgresql.org/) | 15 | 生产数据库 |
| [drf-spectacular](https://drf-spectacular.readthedocs.io/) | 0.27 | OpenAPI 文档 |
| [openpyxl](https://openpyxl.readthedocs.io/) | 3.1 | Excel 导入导出 |
| [python-barcode](https://python-barcode.readthedocs.io/) | 0.15 | 条码生成 |

---

## 📁 项目结构

```
wms-project/
├── frontend/                          # Vue 3 + Vite 前端
│   ├── src/
│   │   ├── api/                       # API 请求封装
│   │   │   ├── auth.ts              # 认证接口
│   │   │   ├── goods.ts             # 商品接口
│   │   │   ├── warehouse.ts         # 仓库接口
│   │   │   ├── asn.ts               # 入库接口
│   │   │   ├── dn.ts                # 出库接口
│   │   │   ├── stock.ts             # 库存接口
│   │   │   ├── cyclecount.ts        # 盘点接口
│   │   │   ├── report.ts            # 报表接口
│   │   │   ├── supplier.ts          # 供应商接口
│   │   │   ├── customer.ts          # 客户接口
│   │   │   └── system.ts            # 系统管理接口
│   │   ├── components/               # 公共组件
│   │   │   ├── layout/              # 布局组件 (侧边栏/导航栏/标签页)
│   │   │   └── common/              # 通用业务组件
│   │   ├── router/                   # 路由配置
│   │   ├── store/                    # Pinia 状态管理
│   │   ├── utils/                    # 工具函数
│   │   ├── views/                    # 页面组件
│   │   │   ├── dashboard/           # 数据看板
│   │   │   ├── goods/               # 商品管理
│   │   │   ├── warehouse/           # 仓库管理
│   │   │   ├── asn/                 # 入库管理
│   │   │   ├── dn/                  # 出库管理
│   │   │   ├── stock/               # 库存管理
│   │   │   ├── cyclecount/          # 盘点管理
│   │   │   ├── supplier/            # 供应商
│   │   │   ├── customer/            # 客户
│   │   │   ├── report/              # 报表中心
│   │   │   ├── system/              # 系统管理
│   │   │   └── login/               # 登录
│   │   └── assets/                   # 静态资源 & 全局样式
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── backend/                           # Django REST 后端
│   ├── apps/
│   │   ├── users/                    # 用户、角色、部门、菜单、操作日志
│   │   ├── goods/                    # 商品主数据
│   │   ├── warehouse/                # 仓库层级
│   │   ├── supplier/                 # 供应商管理
│   │   ├── customer/                 # 客户管理
│   │   ├── stock/                    # 库存 & WebSocket
│   │   ├── asn/                      # 入库 (ASN)
│   │   ├── dn/                       # 出库 (DN)
│   │   ├── cyclecount/               # 盘点
│   │   ├── capital/                  # 资产 & 托盘
│   │   └── report/                   # 报表聚合
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py              # 通用配置
│   │   │   ├── dev.py               # 开发环境
│   │   │   └── prod.py              # 生产环境
│   │   ├── urls.py                   # 路由入口
│   │   ├── asgi.py                   # ASGI (HTTP + WebSocket)
│   │   ├── wsgi.py                   # WSGI
│   │   └── celery.py                 # Celery 配置
│   ├── utils/                        # 工具类
│   │   ├── mixins.py                # UUID 模型 / 软删除
│   │   ├── pagination.py            # 统一分页
│   │   ├── permissions.py           # 权限控制
│   │   └── exceptions.py            # 异常处理
│   ├── requirements.txt
│   └── manage.py
│
└── .gitignore
```

---

## 🚀 快速开始

### 环境要求

- **Node.js** >= 18
- **Python** >= 3.10
- **PostgreSQL** >= 14 (生产环境)
- **Redis** >= 6 (生产环境，用于 Channels & Celery)

### 后端启动

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
source venv/bin/activate   # Linux / macOS
# 或
venv\Scripts\activate      # Windows

# 4. 安装依赖
pip install -r requirements.txt

# 5. 执行数据库迁移
python manage.py migrate

# 6. 创建超级用户
python manage.py createsuperuser

# 7. 启动开发服务器
python manage.py runserver 8000
```

开发环境默认使用 SQLite 数据库，无需额外配置。

API 地址：http://127.0.0.1:8000/api/v1/

API 文档：
- Swagger UI：http://127.0.0.1:8000/api/docs/
- ReDoc：http://127.0.0.1:8000/api/redoc/

### 前端启动

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev
```

前端开发服务器运行在 http://localhost:9528，自动代理 `/api` 请求到后端 http://127.0.0.1:8000。

### 生产部署

```bash
# 后端 - 设置环境变量
export DJANGO_SETTINGS_MODULE=config.settings.prod
export DB_NAME=wms_db
export DB_USER=wms_user
export DB_PASSWORD=your_password
export REDIS_URL=redis://127.0.0.1:6379/0
export DJANGO_SECRET_KEY=your-secret-key
export ALLOWED_HOSTS=your-domain.com
export CORS_ORIGINS=https://your-frontend.com

# 启动 WSGI
gunicorn config.wsgi -w 4 -b 0.0.0.0:8000

# 启动 ASGI (WebSocket)
daphne -p 8001 config.asgi:application

# 启动 Celery Worker
celery -A config worker -l info

# 前端 - 构建生产包
cd frontend
npm run build
# 将 dist/ 目录部署到 Nginx 等静态服务器
```

---

## 📡 WebSocket 事件

连接地址：`ws://host:8001/ws/stock/`

| 事件 | 说明 |
|------|------|
| `stock_changed` | 库存数量变动时推送 |
| `safety_stock_alert` | 库存低于安全库存时告警 |

---

## 🔌 API 接口

| 模块 | 前缀 | 说明 |
|------|------|------|
| 认证 | `POST /api/v1/auth/login/` | JWT 登录 |
| 认证 | `POST /api/v1/auth/token/refresh/` | 刷新 Token |
| 用户 | `GET /api/v1/users/users/` | 用户列表 |
| 角色 | `GET /api/v1/users/roles/` | 角色列表 |
| 部门 | `GET /api/v1/users/departments/` | 部门列表 |
| 菜单 | `GET /api/v1/users/menus/` | 菜单列表 |
| 商品 | `GET /api/v1/goods/goods/` | 商品列表 |
| 仓库 | `GET /api/v1/warehouses/warehouses/` | 仓库列表 |
| 库区 | `GET /api/v1/warehouses/zones/` | 库区列表 |
| 库位 | `GET /api/v1/warehouses/bins/` | 库位列表 |
| 供应商 | `GET /api/v1/suppliers/` | 供应商列表 |
| 客户 | `GET /api/v1/customers/` | 客户列表 |
| 入库 | `GET /api/v1/asn/` | 入库单列表 |
| 出库 | `GET /api/v1/dn/` | 出库单列表 |
| 库存 | `GET /api/v1/stock/` | 库存列表 |
| 盘点 | `GET /api/v1/cyclecount/` | 盘点列表 |
| 资产 | `GET /api/v1/assets/assets/` | 资产列表 |
| 报表 | `GET /api/v1/reports/dashboard/` | 看板统计 |

> 完整接口文档请查看 Swagger UI：http://127.0.0.1:8000/api/docs/

---

## 📊 业务流程

### 入库流程

```
草稿 (draft) → 已到达 (arrived) → 已卸载 (unloaded) → 已上架 (putaway)
```

### 出库流程

```
草稿 (draft) → 已确认 (confirmed) → 已拣货 (picked) → 已发货 (shipped)
```

### 盘点流程

```
创建盘点任务 → 开始盘点 → 录入实盘数量（自动计算差异） → 完成盘点 → 库存调整
```

---

## ⚙️ 配置说明

### 开发环境 (`config/settings/dev.py`)

- `DEBUG = True`
- 数据库：SQLite3
- Channels 层：内存模式
- Celery：eager 模式（同步执行）

### 生产环境 (`config/settings/prod.py`)

配置通过环境变量注入：

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `DJANGO_SECRET_KEY` | Django 密钥 | 必填 |
| `DB_NAME` | 数据库名 | `wms_db` |
| `DB_USER` | 数据库用户 | `wms_user` |
| `DB_PASSWORD` | 数据库密码 | 必填 |
| `DB_HOST` | 数据库主机 | `127.0.0.1` |
| `DB_PORT` | 数据库端口 | `5432` |
| `REDIS_URL` | Redis 地址 | `redis://127.0.0.1:6379/0` |
| `ALLOWED_HOSTS` | 允许的主机 | 必填（逗号分隔） |
| `CORS_ORIGINS` | CORS 允许的源 | 必填（逗号分隔） |

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'feat: add amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 提交 Pull Request

建议遵循 [Conventional Commits](https://www.conventionalcommits.org/) 提交规范。

---

## 📄 License

[MIT](LICENSE)

---

## 👤 作者

- **shang930**
- GitHub: [@shang930](https://github.com/shang930)

---

**Built with ❤️ using Vue 3 + Django REST Framework**
