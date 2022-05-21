import { createRouter, createWebHashHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: DashboardView
  },
  {
    path: '/cloud/',
    name: 'cloud',
    component: () => import(/* webpackChunkName: "cld" */ '../views/CloudView.vue')
  },
  {
    path: '/pics/',
    name: 'pics',
    component: () => import(/* webpackChunkName: "pics" */ '../views/PicsView.vue')
  },
  {
    path: '/vids/',
    name: 'vids',
    component: () => import(/* webpackChunkName: "vds" */ '../views/VidsView.vue')
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
