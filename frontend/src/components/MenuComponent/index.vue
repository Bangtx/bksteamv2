<template lang="pug">
  div
    portal(to="header-action")
      v-icon.nav-icon(@click="openMenuList()") mdi-format-align-justify

    .mt-16(v-if="isResponsive && isOpenMenu")
      div(v-if="isAdmin && isResponsive && isOpenMenu" v-for="item in menuAdmins")
        v-list-item(@click="nextPage(item.event)")
          v-icon {{ item.icon }}
          span {{ item.text }}
        v-divider
      div(v-if="member.type_member === 'teacher' && !isAdmin && isResponsive && isOpenMenu" v-for="item in menuTeachers")
        v-list-item(@click="nextPage(item.event)")
          v-icon {{ item.icon }}
          span {{ item.text }}
        v-divider
      div(v-if="member.type_member === 'student' && !isAdmin && isResponsive && isOpenMenu" v-for="item in menuStudents")
        v-list-item(@click="nextPage(item.event)")
          v-icon {{ item.icon }}
          span {{ item.text }}
        v-divider

    .bg-white.border-r.pb-2.fixed.bottom-0.z-10.w-full.content-center(class="md:bg-gray-50 md:relative md:h-screen md:w-60")
      .text-sm.content-center.text-left.justify-between(class="md:mt-12 md:w-60 md:fixed md:left-0 md:top-0 md:content-start")
        .list-reset.flex.justify-between.flex-row.pt-3.px-2.text-center.text-gray-600(class="md:flex-col md:py-3 md:px-2 md:text-left")
          .relative(
            class="md:block md:px-6 md:py-3 md:pt-6"
            v-if="isAdmin" v-for="item in menuAdmins"
          )
            a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" @click="nextPage(item.event)")
              v-icon.hidden {{ item.icon }}
              span.hidden(class="md:ml-4 md:block") {{ item.text }}

          .relative(
            class="md:block md:px-6 md:py-3 md:pt-6"
            v-if="member.type_member === 'teacher' && !isAdmin" v-for="item in menuTeachers"
          )
            a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" @click="nextPage(item.event)")
              v-icon.hidden {{ item.icon }}
              span.hidden(class="md:ml-4 md:block") {{ item.text }}

          .relative(
            class="md:block md:px-6 md:py-3 md:pt-6"
            v-if="member.type_member === 'student' && !isAdmin" v-for="item in menuStudents"
          )
            a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" @click="nextPage(item.event)")
              v-icon.hidden {{ item.icon }}
              span.hidden(class="md:ml-4 md:block") {{ item.text }}

</template>

<script>
import { defineComponent, ref, getCurrentInstance } from 'vue'
import { urlPath } from '@/utils'
import {HOME_WORK_STUDENT, NOTI} from "@/utils/urlPath";

const MenuComponent = defineComponent({
  props: {
    isAdmin: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  setup() {
    const { $router, $route } = getCurrentInstance().proxy
    const classroomID = $route.params.classroomId
    const member = ref(JSON.parse(localStorage.getItem('token')))
    const isResponsive = ref(window.screen.width < 750)
    const isOpenMenu = ref(false)

    const menuTeachers = [
      { icon: 'mdi-home', text: 'Trang ch???', event: urlPath.CLASS_HOME.name },
      { icon: 'mdi-tooltip-account', text: '??i???m danh', event: urlPath.ROLL_CALL.name },
      { icon: 'mdi-book-account-outline', text: '??i???m s???', event: urlPath.SCORE.name },
      { icon: 'mdi-notification-clear-all', text: 'Th??ng b??o', event: urlPath.NOTI.name },
      { icon: 'mdi-fleur-de-lis', text: 'Giao B??i T???p', event: urlPath.HOME_WORK.name },
      { icon: 'mdi-file-alert-outline', text: 'Giao B??i T???p File', event: urlPath.HOME_WORK_FILE.name },
      { icon: 'mdi-book-edit-outline', text: 'K???t qu??? l??m b??i', event: urlPath.HOME_WORK_SCORE.name },
      { icon: 'mdi-flip-horizontal', text: 'T??? H???c', event: urlPath.SELF_LEARNING.name }
    ]

    const menuAdmins = [
      { icon: 'mdi-home', text: 'Qu???n l?? m??n h???c', event: urlPath.CLASS_MANAGEMENT.name },
      { icon: 'mdi-home', text: 'Qu???n l?? h???c vi??n', event: urlPath.STUDENT_MANAGEMENT.name },
      { icon: 'mdi-home', text: 'Qu???n l?? gi??o vi??n', event: urlPath.TEACHER_MANAGEMENT.name }
    ]

    const menuStudents = [
      { icon: 'mdi-home', text: 'Trang ch???', event: urlPath.CLASS_HOME.name },
      { icon: 'mdi-tooltip-account', text: '??i???m danh', event: urlPath.ROLL_CALL.name },
      { icon: 'mdi-book-account-outline', text: '??i???m s???', event: urlPath.SCORE.name },
      { icon: 'mdi-notification-clear-all', text: 'Th??ng b??o', event: urlPath.NOTI_STUDENT.name },
      { icon: 'mdi-fleur-de-lis', text: 'B??i t???p', event: urlPath.HOME_WORK_STUDENT.name },
      { icon: 'mdi-file-alert-outline', text: 'B??i t???p file', event: urlPath.HOME_WORK_FILE_STUDENT.name },
      { icon: 'mdi-flip-horizontal', text: '??k t??? H???c', event: urlPath.SELF_LEARNING.name }
    ]

    if (!localStorage.getItem('token')) member.value = { type_member: 'teacher' }
    else member.value = JSON.parse(localStorage.getItem('token'))

    window.addEventListener('resize', (event) => {
      isResponsive.value = document.body.clientWidth < 750
    })

    const nextPage = (pathName) => {
      $router.push({
        name: pathName,
        params: {
          classroomId: classroomID
        }
      })
    }

    const openMenuList = () => {
      isOpenMenu.value = !isOpenMenu.value
    }

    return {
      member,
      isResponsive,
      menuTeachers,
      menuAdmins,
      menuStudents,
      openMenuList,
      isOpenMenu,
      nextPage
    }
  }
})

export default MenuComponent
</script>

<style lang="sass">
.relative a:hover
  cursor: pointer
@media (min-width: 850px)
  .nav-icon
    display: none !important
</style>
