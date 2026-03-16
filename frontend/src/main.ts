import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import Vue3Toastify, { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const pinia = createPinia()
const app = createApp(App)

app.use(router)
app.use(pinia)

app.use(Vue3Toastify, {
  position: toast.POSITION.TOP_CENTER,
  duration: 3000,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: true,
  closeButton: 'button',
})

app.mount('#app')
