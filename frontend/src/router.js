import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const Map = () => import('@/views/Map.vue')

export default new Router({
  routes: [{
    path: '/map',
		component: Map,
  }],
	mode: 'history'
})