import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import svgLoader from 'vite-svg-loader' //svg画像をコンポーネントとして扱うためのパッケージ

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), svgLoader()],
  server: {
    host: true,
    watch: {
      usePolling: true
    },
    proxy: {
      "/api":{
        // バックエンドサーバーのベースURLを指定
        target: "http://backend:5001",
        changeOrigin: true,
        // 正規表現を使用: http://localhost:5173/api/ -> http://backend:5001/
        rewrite: (path) => path.replace(/^\/api/, '')
      },
    }
  },

})