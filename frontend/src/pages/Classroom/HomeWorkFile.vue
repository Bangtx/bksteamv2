<template lang="pug">
  .bg-gray-50.min-h-screen
    header-bar
    .flex.flex-col(class="md:flex-row")
      menu-component(:is-admin="false")
      #main.main-content.flex-1.py-20(class='md:pb-5')
        .px-4.text-gray-700(class='md:px-8')
          v-row
            v-col(cols="6")
              date-range(
                :date-start="dateStart"
                :date-end="dateEnd"
                :go-to-date="goToDate"
                @on-change-date="setDate"
              )
            v-col(cols="6")
              v-checkbox(label="Chỉ hiển thị câu hỏi bắt buộc" v-model="showRequire" @click="toShowRequire")
          .flex.justify-between.items-center
            .text-lg Danh sách câu hỏi
            button.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(
              @click="openQuestionDialog('add')"
              class='hover:bg-orange-300 focus:outline-none'
            )
              svg.h-6.w-6(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
                path(stroke-linecap='round' stroke-linejoin='round' d='M12 6v6m0 0v6m0-6h6m-6 0H6')
              span.text-base Thêm câu hỏi

          .rounded-lg.overflow-auto.shadow-xs.mt-4(class="lg:px-10")
            .w-full.overflow-auto.rounded-lg(style="max-height: 600px; max-width: 1550px;")
              div(v-for="homeWorkFile, index in HomeWorksFile.filter(e => e.is_global)" )
                v-list-item(@click="openQuestionDialog('edit', homeWorkFile)" :style="homeWorkFile.have_to_do ? 'background-color: #c5ffc5': ''")
                  h3 {{ index + 1 }}
                  v-spacer
                  span {{ homeWorkFile.description }}
                  v-spacer
                  i.watch(@click.stop="watchFile(homeWorkFile.file_url)") xem ngay
                  v-spacer
                  span {{ homeWorkFile.date }}
                v-divider
          .flex.justify-between.items-center
            .text-lg Danh sách câu hỏi riêng
          .rounded-lg.overflow-auto.shadow-xs.mt-4(class="lg:px-10")
            .w-full.overflow-auto.rounded-lg(style="max-height: 600px; max-width: 1550px;")
              div(v-for="homeWorkFile, index in HomeWorksFile.filter(e => !e.is_global)" )
                v-list-item(@click="openQuestionDialog('edit', homeWorkFile)" :style="homeWorkFile.have_to_do ? 'background-color: #c5ffc5': ''")
                  h3 {{ index + 1 }}
                  v-spacer
                  span {{ homeWorkFile.description }}
                  v-spacer
                  i.watch(@click.stop="watchFile(homeWorkFile.file_url)") xem ngay
                  v-spacer
                  span {{ homeWorkFile.date }}
                v-divider

    question-file-dialog(
      :value="isOpenAddQuestionDialog"
      :classroom="classroom"
      :units="units"
      :question-file="curQuestionFile"
      :is-add="isAdd"
      @re-load="reload"
      @on-close="isOpenAddQuestionDialog = false"
    )

</template>

<script>
import { defineComponent, ref, onMounted, getCurrentInstance } from 'vue'
import { NotificationDialog, EditRollCallDialog, HeaderBar, MenuComponent, QuestionFileDialog, DateRange } from '@/components'
import { api } from '@/plugins'
import { endpoints } from '@/utils'
import { firstday, lastday } from './index'
import moment from "moment/moment";

const HomeWorkFile = defineComponent({
  components: {
    NotificationDialog, EditRollCallDialog, HeaderBar, MenuComponent, QuestionFileDialog, DateRange
  },
  setup() {
    const { $toast, $route } = getCurrentInstance().proxy
    const classroomID = $route.params.classroomId
    const HomeWorksFile = ref([])
    const HomeWorksFileBase = ref([])
    const units = ref([])
    const classroom = ref({})
    const teacher = ref({})
    const isOpenAddQuestionDialog = ref(false)
    const curQuestionFile = ref({})
    const isAdd = ref(false)
    const dateStart = ref(moment(firstday).format('YYYY-MM-DD'))
    const dateEnd = ref(moment(lastday).format('YYYY-MM-DD'))
    const showRequire = ref(false)

    const getData = async () => {
      try {
        const data = await Promise.all([
          api.get(`${endpoints.CLASSROOM}${classroomID}`),
          api.get(`${endpoints.TEACHER}?classroom=${classroomID}`),
          api.get(`${endpoints.HOME_WORK_FILE}?classroom=${classroomID}&date_from=${dateStart.value}&date_to=${dateEnd.value}`),
          api.get(`${endpoints.UNIT}?classroom=${classroomID}`)
        ])

        const [{ data: ClassData }, { data: TeaData }, { data: hwData }, { data: untData }] = data

        classroom.value = ClassData
        teacher.value = TeaData[0]
        HomeWorksFileBase.value = hwData
        HomeWorksFile.value = JSON.parse(JSON.stringify(HomeWorksFileBase.value))
        units.value = untData
      } catch (e) {
        $toast.error('Get data failed')
      }
      getCurrentInstance()?.proxy?.$forceUpdate()
    }

    const reload = async () => {
      await getData()
    }

    const openQuestionDialog = (mode, homeWork=null) => {
      if (homeWork) curQuestionFile.value = homeWork
      isOpenAddQuestionDialog.value = true
      isAdd.value = mode === 'add'
    }

    const goToDate = async () => {
      await getData()
    }

    const toShowRequire = () => {
      if (showRequire.value) HomeWorksFile.value = HomeWorksFileBase.value.filter(e => e.have_to_do)
      else HomeWorksFile.value = JSON.parse(JSON.stringify(HomeWorksFileBase.value))
    }

    const setDate = (startDate, endDate) => {
      dateStart.value = startDate
      dateEnd.value = endDate
    }

    const watchFile = (url) => {
      window.open(url)
    }

    onMounted(async () => {
      await getData()
    })

    return {
      classroom,
      teacher,
      HomeWorksFile,
      openQuestionDialog,
      isOpenAddQuestionDialog,
      units,
      curQuestionFile,
      isAdd,
      reload,
      dateStart,
      dateEnd,
      goToDate,
      setDate,
      toShowRequire,
      showRequire,
      watchFile
    }
  }
})

export default HomeWorkFile
</script>

<style lang="sass" scoped>
.watch
  cursor: pointer
  text-decoration: underline
  color: #0e68af
</style>