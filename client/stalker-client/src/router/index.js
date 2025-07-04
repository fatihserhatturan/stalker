import { createRouter, createWebHistory } from 'vue-router'
import ChatComponent from '../components/ChatComponent.vue'

const routes = [
  {
    path: '/',
    name: 'Chat',
    component: ChatComponent
  }
  // DocumentViewer artık ayrı bir route değil, ChatComponent içinde kullanılıyor
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
