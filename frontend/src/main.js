import Vue from 'vue'
import App from './App.vue'
import router from './router'
import config from './assets/js/config'
import utils from './assets/js/utils'
import BootstrapVue from 'bootstrap-vue'
import axios from 'axios'
//import qs from 'qs'
import vueSmoothScroll from 'vue-smooth-scroll'
import SuiVue from 'semantic-ui-vue'
import 'semantic-ui-css/semantic.min.css'
import VueFlashMessage from 'vue-flash-message'
require('vue-flash-message/dist/vue-flash-message.min.css')

Vue.use(VueFlashMessage)
Vue.use(SuiVue)
Vue.use(vueSmoothScroll)
Vue.use(BootstrapVue)

Vue.config.productionTip = false

axios.defaults.timeout = 600000
// axios compatible with IE 8-9
axios.interceptors.response.use(response => {
	return response
})
axios.interceptors.request.use(config => {
  const API_KEY = '227415ba68c811e9b1a48c8590c7151e'
  config.headers = {
    'Content-Type': 'application/json',
    'X-API-KEY': API_KEY,
	}
	console.log(this,config)
  return config
},err => {
  return Promise.reject(err)
})

let request = function (options) {
	let method = options.method.toLowerCase()
	console.log(options.data)
  return new Promise(function(resolve, reject){
		axios({
			url: options.url,
			method: method,
			data: options.data
		}).then(res=>{
			if (res.status == 200 && res.data && res.data.err_msg === 'success') {
				resolve(res.data)
			} else {
				reject(res.data)
			}
		}).catch(e=>{
			reject(e)
		})
	})
}
Vue.prototype.$axios = axios
Vue.prototype.$ajax = request
Vue.prototype.siteConfig = config
Vue.prototype.siteUtils = utils

Vue.prototype.setTitle = function(title){
	document.title = title
}

Vue.prototype.goBack = function(){
	window.history.length > 1 ? router.go(-1) : router.push('/')
}

const app = new Vue({
  el: '#app',
  router,
  render: h => h(App)
});
app.$mount('#app');
