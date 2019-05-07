import Vue from 'vue'
import App from './App.vue'
import router from './router'
import config from './assets/js/config'
import utils from './assets/js/utils'
import BootstrapVue from 'bootstrap-vue'
import axios from 'axios'
import qs from 'qs'
import vueSmoothScroll from 'vue-smooth-scroll'

Vue.use(vueSmoothScroll)
Vue.use(BootstrapVue)

Vue.config.productionTip = false
axios.defaults.timeout = 60000
// axios compatible with IE 8-9
axios.interceptors.response.use(response => {
	// IE 8-9
	if (response.data == null && response.config.responseType === 'json' && response.request.responseText != null) {
		try {
			// eslint-disable-next-line no-param-reassign
			response.data = JSON.parse(response.request.responseText)
		} catch (e) {
			// ignored
		}
	}
	return response
})

let request = function (options) {
  let dataParams = options.data
	let data = {}
	let requestUrl = options.url

  for (let key in dataParams) {
		data[key] = dataParams[key]
  }
  data = qs.stringify(data)
	let method = options.method.toLowerCase()
	let needStrParam = method === 'get' || method === 'put' || method === 'delete'
	if(data.length && needStrParam){
		requestUrl += config.baseApi.indexOf('?')>=0 ? '&' : '?'
		requestUrl += data
  }
  
  return new Promise(function(resolve, reject){
		axios({
			url: config.baseApi + requestUrl,
			method: options.method,
			responseType: options.dataType || 'json',
			data: needStrParam ? '' : data
		}).then(res=>{
			if (res.data.success) {
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
