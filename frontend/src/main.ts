import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import { i18n, vuetify } from './plugins'
import Toast from 'vue-toastification'
import PortalVue from 'portal-vue'
import 'vue-toastification/dist/index.css'

Vue.config.productionTip = false
Vue.use(PortalVue)
Vue.use(Toast, { hideProgressBar: true })

new Vue({
  router,
  store,
  vuetify,
  i18n,
  render: h => h(App)
}).$mount('#app')
