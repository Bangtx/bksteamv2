<template lang="pug">
  div
    div(:style="{backgroundColor: '#FFF', marginTop: '16vh'}")
      div.text-red-600.text-center.font-bold.text-3xl.pb-6.hidden(class="md:block")
        div.flex.justify-center
          img.w-14(:src="`/img/icons/android-chrome-192x192.png`")
        div HỌC VIỆN STEAM BÁCH KHOA
      div
        v-layout(align-center justify-center)
          v-flex.justify-center
            div.bg-gray-50.border.rounded-lg.w-500.pb-2
              div.rounded-t-lg.bg-orange
                v-toolbar-title.py-3.ml-6.text-white.font-semibold Đăng Nhập
              v-card-text
                v-form
                  v-text-field(
                    prepend-icon="mdi-account" :label="'id'" type="text" v-model="userData.id"
                  )
                  v-text-field#password(
                    prepend-icon="mdi-key"
                    :label="'Mật khẩu'"
                    type="password"
                    v-model="userData.password"
                  )
                  v-checkbox(v-model="userData.is_teacher" label="Chọn nếu bạn là giáo viên" )
              v-card-actions
                v-spacer
                v-btn.bg-orange.mr-4( @click="onClickLogin()") Đăng Nhập
                v-btn(@click="onForgetId()") Quên ID
                v-btn Quên Mật Khẩu

    get-id-dialog(
      :value="isShowGetIdDialog"
      @on-close="isShowGetIdDialog = false"
    )

</template>

<script>
import { defineComponent, ref, getCurrentInstance } from 'vue'
import { api } from '@/plugins'
import { endpoints, urlPath } from '@/utils'
import GetIdDialog from './GetIdDialog.vue'
const Login = defineComponent({
  components: {
    GetIdDialog
  },
  setup() {
    const { $toast, $router } = getCurrentInstance().proxy
    const userData = ref({ id: '', password: '', is_teacher: false })
    const isShowGetIdDialog = ref(false)

    const onClickLogin = async () => {
      userData.value.id = userData.value.id.trim()
      userData.value.password = userData.value.password.trim()
      if (userData.value.id.length === 0) $toast.error('Vui lòng nhập mail/sđt')
      if (userData.value.password.length === 0) $toast.error('Vui lòng nhập mật khẩu')
      if (userData.value.id.length > 0 && userData.value.password.length > 0) {
        try {
          const { data } = await api.post(`${endpoints.AUTH}login`, userData.value)
          if (data.status !== 200) {
            $toast.error('Tài khoản mật khẩu không chính xác')
            return
          }
          localStorage.setItem('token', JSON.stringify(data.token))
          $router.push({
            name: urlPath.HOME.name
          })
        } catch (e) {
          $toast.error('Đăng nhập thấy bại')
        }
      }
    }

    const onForgetId = () => {
      isShowGetIdDialog.value = true
    }

    return {
      userData,
      onClickLogin,
      onForgetId,
      isShowGetIdDialog
    }
  }
})
export default Login
</script>

<style lang="sass">
.bg-orange
  background: #fb923c !important
  color: white !important
.w-500
  width: 300px
@media (min-width: 500px)
  .w-500
    width: 500px
</style>
