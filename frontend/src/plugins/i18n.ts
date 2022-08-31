import Vue from 'vue'
import VueI18n from 'vue-i18n'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import ja from '../locale/ja.json'

Vue.use(VueI18n)

const i18n = new VueI18n({
  locale: 'ja',
  messages: {
    ja
  }
})

export default i18n
