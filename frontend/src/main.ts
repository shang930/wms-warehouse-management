import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './store'
import 'normalize.css'
import 'element-plus/dist/index.css'
import 'nprogress/nprogress.css'
import './assets/styles/global.scss'

const app = createApp(App)
app.use(pinia)
app.use(router)
app.mount('#app')
