import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@element-plus/icons-vue'
import Cookies from 'Vue-Cookies'
import App from './App.vue'

const app = createApp(App)
app.use(Cookies)
app.use(ElementPlus)
app.mount('#app')
