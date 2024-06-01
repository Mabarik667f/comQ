import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LoginView from '@/views/LoginView.vue'
import store from '@/store'


const authGuard = async (to, from, next) => {
  store.dispatch('verifyToken');
  if(!store.state.auth.isAuth) {
    next('/login')
  } else {
    next()
  }
}

const userAuth = async (to, from, next) => {
  if(store.state.auth.isAuth) {
    next('/');
  } else {
    next();
  }
}

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    beforeEnter: authGuard
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
    beforeEnter: authGuard
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    beforeEnter: userAuth
    
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    beforeEnter: userAuth
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  store.dispatch('setIsAuth').then(() => {
    next();
  });
})
export default router
