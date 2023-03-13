import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import StockDetail from '../views/StockDetail.vue'
import Portfolio from '../views/Portfolio.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/:ticker',
    name: 'StockDetail',
    component: StockDetail
  },
  {
    path: '/portfolio',
    name: 'Portfolio',
    component: Portfolio,
    props: route => ({ message: route.params.message })
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
