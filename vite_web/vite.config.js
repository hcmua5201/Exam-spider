import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
    server: {
    host: '0.0.0.0',
    port: 5179,
    https: false,
    cors: true,
    changeOrigin: true,
    proxy: {
      '/api': {                                 //内网穿透放后端端口
        target: 'http://127.0.0.1:5000/',      //后端接口的根目录
        changeOrigin: true,                    //是否跨域
        rewrite: (path) => path.replace(/^\/api/, ''),
      },

    },
  }
})
