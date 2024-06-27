import { createRouter, createWebHistory } from 'vue-router'
import Cookies from "js-cookie";
import HomeView from '../views/HomeView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LoginView from '@/views/LoginView.vue'
import store from '@/store'
import ProfileView from '@/views/ProfileView.vue'
import MainChat from '@/components/MainChat.vue'


const authGuard = async (to, from, next) => {
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
    beforeEnter: authGuard,
    children: [
      {
        path: '/chat/:pk',
        name: 'chat-detail',
        component: MainChat,
        props: true,
        beforeEnter: (to, from, next) => {
          if (Cookies.get('chat') == to.params.pk) {
            next()
          } else {
            next('/')
          }
        }
      }
      
    ]
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
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    beforeEnter: authGuard
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


router.beforeEach((to, from, next) => {
  
  store.dispatch('setIsAuth').then(() => {
    store.dispatch('getChatDataCookies')
    next();
  });
})
export default router
