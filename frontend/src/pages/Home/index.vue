<template lang="pug">
  div
    .bg-gray-50.min-h-screen
      header-bar
      div.banner-content
        img.hidden.w-full.h-auto(class="md:block" :src="`${baseUrl}/img/banner2.png`" alt="")
        img.w-full.h-auto(class="md:hidden" :src="`${baseUrl}/img/banner1.png`" alt="")
      .px-4.text-gray-800(class="md:px-8")
        .flex.items-center.gap-4.mt-8
          button.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(class="hover:bg-orange-300 focus:outline-none")
            svg.h-6.w-6(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
              path(stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6")
            span.text-base Thêm lớp
          button.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(class="hover:bg-orange-300 focus:outline-none")
            svg.h-6.w-6(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
              path(stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6")
            span.text-base Button 2
        .flex.items-center.gap-2.py-4.mt-4
          svg.h-7.w-7(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
            path(stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16")
          .text-3xl Danh sách lớp
        // class list
        .grid.gap-6.mb-8(class="md:grid-cols-2 xl:grid-cols-4")
          div(
            v-for="classroom in classrooms"
            :key="classroom.id"
          )
            class-button(
              :class-name="classroom.name"
              @on-click="openClassroom(classroom.id)"
            )

</template>

<script>
import { defineComponent, onMounted, ref, getCurrentInstance } from 'vue'
import { HeaderBar, ClassButton } from '@/components'
import { urlPath, endpoints } from '@/utils'
import { api } from '@/plugins'

const Home = defineComponent({
  components: {
    HeaderBar,
    ClassButton
  },
  setup() {
    const { $router, $toast } = getCurrentInstance().proxy
    // const baseUrl = process.env.VUE_APP_WEB_URL_PRO
    const baseUrl = process.env.VUE_APP_WEB_URL
    const classrooms = ref([])

    const member = JSON.parse(localStorage.getItem('token'))

    const openClassroom = (classroomId) => {
      $router.push({
        name: urlPath.CLASS_HOME.name,
        params: {
          classroomId: String(classroomId)
        }
      })
    }

    const getData = async () => {
      try {
        const url =
          member.type_member === 'teacher'
            ? `${endpoints.CLASSROOM}?teacher_id=${member.id}`
            : `${endpoints.CLASSROOM}?student_id=${member.id}`
        const { data } = await api.get(url)
        classrooms.value = data
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    onMounted(async () => {
      await getData()
    })
    return {
      openClassroom,
      classrooms,
      baseUrl,
      member
    }
  }
})
export default Home
</script>

<style lang="sass">
.banner-content
  padding-top: 72px
</style>
