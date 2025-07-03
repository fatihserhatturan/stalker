import { createRouter, createWebHistory } from 'vue-router'
import ChatComponent from '../components/ChatComponent.vue'
import DocumentViewer from '../components/DocumentViewer.vue'

const routes = [
  {
    path: '/',
    name: 'Chat',
    component: ChatComponent
  },
  {
    path: '/document',
    name: 'Document',
    component: DocumentViewer
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
