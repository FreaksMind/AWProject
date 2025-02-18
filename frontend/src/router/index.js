import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Navigation from "../components/Navigation.vue";
import store from '@/store';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/query',
      name: 'query',
      component: () => import('../views/QueryView.vue')
    },
    {
      path: '/tree',
      name: 'tree',
      component: () => import('../views/TreeView.vue')
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/SearchView.vue')
    },
    {
      path: '/visualize',
      name: 'visualize',
      component: () => import('../views/VisualView.vue')
    }
  ]
})

export default router
