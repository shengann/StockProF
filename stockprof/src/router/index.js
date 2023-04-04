import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import StockDetail from '../views/StockDetail.vue'
import Portfolio from '../views/Portfolio.vue'
import SignUp from '../views/SignUp.vue'
import Login from '../views/Login.vue'

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
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: SignUp,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
