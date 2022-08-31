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
              span Số Câu Đúng {{ homeWorkFileResults.filter(e => e.is_correct).length }} /
              span Số Câu Đã Làm {{ homeWorkFileResults.length }} /
              span Tổng Số Câu Bắt Buộc {{ homeWorkFiles.filter(e => e.have_to_do).length }} /
              span Tổng Số Câu {{ homeWorkFiles.length }}

          .rounded-lg.overflow-auto.shadow-xs.mt-4(class="lg:px-10")
            .w-full.overflow-auto.rounded-lg(style="max-height: 600px; max-width: 1600px;")
              v-list
                v-list-group(
                  v-for="homeWorkFile, index in homeWorkFiles" :key='index' no-action
                  :style="homeWorkFile.have_to_do ? 'background-color: #c5ffc5': ''"
                  @click="curHomeWorkFile = homeWorkFile"
                )
                  template(v-slot:activator='')
                    v-list-item
                      span {{ homeWorkFile.description }}
                      v-spacer
                      i.watch(@click="watchFile(homeWorkFile.file_url)") xem đề bài
                      v-spacer
                      span {{ homeWorkFile.score ? homeWorkFile.score.toString() + 'điểm' : 'chưa có điểm' }}
                      v-spacer
                      span.watch(
                        :style="homeWorkFile.isCompleted ? 'background-color: #ffff55': ''"
                        @click="reWatch(homeWorkFile)"
                      ) {{ homeWorkFile.isCompleted ? 'Xem lại' : 'Chưa làm' }}
                  v-list-item(v-if="!homeWorkFileResults.find(e => e.home_work_file === homeWorkFile.id)")
                    v-text-field(label="Trả lời (link driver quyền sửa)" v-model="homeWorkFile.file_result_url")
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

const HomeWorkFileStudent = defineComponent({
  components: {
    NotificationDialog, EditRollCallDialog, HeaderBar, MenuComponent, QuestionDialog, DateRange
  },
  setup() {
    const { $toast, $route } = getCurrentInstance().proxy
    const classroomID = $route.params.classroomId
    const homeWorkFiles = ref([])
    const homeWorkFilesBase = ref([])
    const curHomeWorkFile = ref({})
    const homeWorkFileResults = ref([])
    const isOpenAddQuestionDialog = ref(false)
    const isAdd = ref(false)
    const member = JSON.parse(localStorage.getItem('token'))
    const dateStart = ref(moment(firstday).format('YYYY-MM-DD'))
    const dateEnd = ref(moment(lastday).format('YYYY-MM-DD'))
    const showRequire = ref(false)
    const totalCorrect = ref(0)
    const totalRequire = ref(0)

    // const calculator = () => {
    //   totalCorrect.value = homeWorkFileResults.value.filter(e => e.is_correct).length
    //   totalRequire.value = homeWorkFiles.value.filter(e => e.have_to_do).length
    // }

    const getData = async () => {
      try {
        const data = await Promise.all([
          api.get(`${endpoints.HOME_WORK_FILE}?classroom=${classroomID}&student=${member.id}&date_from=${dateStart.value}&date_to=${dateEnd.value}`),
          api.get(`${endpoints.HOME_WORK_FILE_RESULT}?classroom=${classroomID}&student=${member.id}&date_from=${dateStart.value}&date_to=${dateEnd.value}`)
        ])

        const [{ data: hwData }, { data: hwrData }] = data

        homeWorkFileResults.value = hwrData
        homeWorkFilesBase.value = hwData.map(homeWorkFile => {
          return {
            ...homeWorkFile,
            isCompleted: !!homeWorkFileResults.value.find(e => e.home_work_file === homeWorkFile.id),
            file_result_url: null
          }
        })
        homeWorkFiles.value = JSON.parse(JSON.stringify(homeWorkFilesBase.value))
      } catch (e) {
        $toast.error('Get data failed')
      }
      // calculator()
      getCurrentInstance()?.proxy?.$forceUpdate()
    }

    const toShowRequire = () => {
      if (showRequire.value) homeWorkFiles.value = homeWorkFilesBase.value.filter(e => e.have_to_do)
      else homeWorkFiles.value = JSON.parse(JSON.stringify(homeWorkFilesBase.value))
    }

    const reload = async () => {
      await getData()
    }

    const getBody = () => {
      const body = homeWorkFiles.value
        .filter(e => e.file_result_url)
        .map(e => {
          return {
            home_work_file: e.id,
            student: member.id,
            file_result_url: e.file_result_url
          }
        })
      return body
    }

    const onSubmit = async () => {
      const body = getBody()
      console.log(body)
      try {
        await api.post(endpoints.HOME_WORK_FILE_RESULT, body)
        $toast.success('Save data successful')
        await getData()
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const goToDate = async () => {
      await getData()
    }

    const watchFile = (url) => {
      window.open(url)
    }

    const reWatch = (homeWorkFile) => {
      const url = homeWorkFileResults.value.find(e => e.home_work_file === homeWorkFile.id)?.file_result_url
      if (url) watchFile(url)
    }

    const setDate = (startDate, endDate) => {
      dateStart.value = startDate
      dateEnd.value = endDate
    }

    onMounted(async () => {
      await getData()
    })

    return {
      homeWorkFiles,
      isOpenAddQuestionDialog,
      isAdd,
      reload,
      homeWorkFileResults,
      curHomeWorkFile,
      dateStart,
      dateEnd,
      setDate,
      goToDate,
      showRequire,
      toShowRequire,
      onSubmit,
      totalCorrect,
      totalRequire,
      watchFile,
      reWatch
    }
  }
})

export default HomeWorkFileStudent
</script>

<style lang="sass" scoped>
.total-result
  font-size: 19px
  color: white
  padding: 10px
  border-radius: 12px
.watch
  cursor: pointer
  text-decoration: underline
  color: #0e68af
</style>