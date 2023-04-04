import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import StockDetail from '../views/StockDetail.vue'
import Portfolio from '../views/Portfolio.vue'
import SignUp from '../views/SignUp.vue'
import Login from '../views/Login.vue'
import PersonalProfile from '../views/PersonalProfile.vue'
import store from '../store'

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
  },
  {
    path: '/profile',
    name: 'PersonalProfile',
    component: PersonalProfile,
    meta: {
      requireLogin: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({ name: 'LogIn', query: { to: to.path } });
  } else {
    next()
  }
})

export default router
