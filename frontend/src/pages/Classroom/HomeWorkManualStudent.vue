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
            v-col(cols="12")
              span.total-result(:style="totalCorrect/totalRequire < 0.85 ? 'background-color: red' : 'background-color: green'")
                | {{ totalCorrect/totalRequire*100 }} % --> {{ totalCorrect/totalRequire < 0.85 ? 'Chưa hoàn thành' : 'Hoàn thành'}}
            v-col(cols="12")
              span Số Câu Đúng {{ homeWorkResults.filter(e => e.is_correct).length }} /
              span Số Câu Đã Làm {{ homeWorkResults.length }} /
              span Tổng Số Câu Bắt Buộc {{ homeWorks.filter(e => e.have_to_do).length }} /
              span Tổng Số Câu {{ homeWorks.length }}

          .rounded-lg.overflow-auto.shadow-xs.mt-4(class="lg:px-10")
            .w-full.overflow-auto.rounded-lg(style="max-height: 600px; max-width: 1600px;")
              v-list
                v-list-group(
                  v-for="homeWork, index in homeWorks" :key='index' no-action
                  :style="curHomeWork.id === homeWork.id ? 'background-color: #ffe3c1' : (homeWork.have_to_do ? 'background-color: #c5ffc5': '')"
                  @click="curHomeWork = homeWork"
                )
                  template(v-slot:activator='')
                    v-list-item-content
                      v-list-item-title(v-html="homeWork.question")
                      audio(v-if="homeWork.audio" controls)
                        source(:src="homeWork.audio")
                  v-list-item
                    div(v-if="homeWork.multi_choice")
                      v-radio-group(row v-model="homeWork.answer_student")
                        v-radio(:label="homeWork.option_1" :value="homeWork.option_1")
                        v-radio(:label="homeWork.option_2" :value="homeWork.option_2")
                        v-radio(:label="homeWork.option_3" :value="homeWork.option_3")
                    div(v-else)
                      v-text-field(label="Trả lời" v-model="homeWork.answer_student")
                  v-divider
          v-list-item
            v-spacer
            button.flex.mt-4.mr-16.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(
              @click="onSubmit"
              class='hover:bg-orange-300 focus:outline-none'
            )
              span.text-base Nộp Bài
</template>

<script>
import { defineComponent, ref, onMounted, getCurrentInstance } from 'vue'
import { NotificationDialog, EditRollCallDialog, HeaderBar, MenuComponent, QuestionDialog, DateRange } from '@/components'
import { api } from '@/plugins'
import { endpoints } from '@/utils'
import { firstday, lastday } from './index'
import moment from "moment";

const HomeWorkManualStudent = defineComponent({
  components: {
    NotificationDialog, EditRollCallDialog, HeaderBar, MenuComponent, QuestionDialog, DateRange
  },
  setup() {
    const { $toast, $route } = getCurrentInstance().proxy
    const classroomID = $route.params.classroomId
    const homeWorks = ref([])
    const homeWorksBase = ref([])
    const curHomeWork = ref({})
    const homeWorkResults = ref([])
    const isOpenAddQuestionDialog = ref(false)
    const isAdd = ref(false)
    const member = JSON.parse(localStorage.getItem('token'))
    const dateStart = ref(moment(firstday).format('YYYY-MM-DD'))
    const dateEnd = ref(moment(lastday).format('YYYY-MM-DD'))
    const showRequire = ref(false)
    const totalCorrect = ref(0)
    const totalRequire = ref(0)

    const calculator = () => {
      totalCorrect.value = homeWorkResults.value.filter(e => e.is_correct).length
      totalRequire.value = homeWorks.value.filter(e => e.have_to_do).length
    }

    const getData = async () => {
      try {
        const data = await Promise.all([
          api.get(`${endpoints.HOME_WORK}?classroom=${classroomID}&date_from=${dateStart.value}&date_to=${dateEnd.value}`),
          api.get(`${endpoints.HOME_WORK_RESULT}?classroom=${classroomID}&student=${member.id}&date_from=${dateStart.value}&date_to=${dateEnd.value}`)
        ])

        const [{ data: hwData }, { data: hwrData }] = data

        homeWorksBase.value = hwData.map(e => {
          return {...e, answer_student: null }
        })
        homeWorks.value = JSON.parse(JSON.stringify(homeWorksBase.value))
        homeWorkResults.value = hwrData
      } catch (e) {
        $toast.error('Get data failed')
      }
      calculator()
      getCurrentInstance()?.proxy?.$forceUpdate()
    }

    const toShowRequire = () => {
      if (showRequire.value) homeWorks.value = homeWorksBase.value.filter(e => e.have_to_do)
      else homeWorks.value = JSON.parse(JSON.stringify(homeWorksBase.value))
    }

    const reload = async () => {
      await getData()
    }

    const getBody = () => {
      const body = homeWorks.value
        .filter(e => e.answer_student)
        .map(e => {
          return {
            home_work: e.id,
            student: member.id,
            answer: e.answer_student,
            is_correct: e.answer_student.trim() === e.answer.trim()
          }
        })
      return body
    }

    const onSubmit = async () => {
      const body = getBody()
      try {
        await api.post(endpoints.HOME_WORK_RESULT, body)
        $toast.success('Save data successful')
        await getData()
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const goToDate = async () => {
      await getData()
    }

    const setDate = (startDate, endDate) => {
      dateStart.value = startDate
      dateEnd.value = endDate
    }

    onMounted(async () => {
      await getData()
    })

    return {
      homeWorks,
      isOpenAddQuestionDialog,
      isAdd,
      reload,
      homeWorkResults,
      curHomeWork,
      dateStart,
      dateEnd,
      setDate,
      goToDate,
      showRequire,
      toShowRequire,
      onSubmit,
      totalCorrect,
      totalRequire
    }
  }
})

export default HomeWorkManualStudent
</script>

<style lang="sass">
.total-result
  font-size: 19px
  color: white
  padding: 10px
  border-radius: 12px
</style>