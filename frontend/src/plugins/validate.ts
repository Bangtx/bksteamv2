import Vue from 'vue'
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate'
import * as rules from 'vee-validate/dist/rules'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import { messages } from 'vee-validate/dist/locale/ja.json'

Object.keys(rules).forEach((rule) => {
  extend(rule, {
    ...rules[rule as keyof typeof rules], // copies rule configuration
    message: messages[rule as keyof typeof messages] // assign message
  })
})

Vue.component('ValidationProvider', ValidationProvider)
Vue.component('ValidationObserver', ValidationObserver)
