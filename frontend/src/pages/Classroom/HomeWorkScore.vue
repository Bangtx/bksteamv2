<template lang="pug">
  .bg-gray-50.min-h-screen
    header-bar
    .flex.flex-col(class="md:flex-row")
      menu-component(:is-admin="false")
      #main.main-content.flex-1.py-20(class='md:pb-5')
        .px-4.text-gray-700(class='md:px-8')
          h1.flex.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
            svg.h-6.w-6.mr-1(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
              path(stroke-linecap='round' stroke-linejoin='round' d='M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6')
            div Kết quả làm bài
          .rounded-lg.overflow-auto.shadow-xs.mt-4(class="lg:px-10")
            .w-full.overflow-auto.rounded-lg(style="max-height: 600px; max-width: 1550px;")
              table.w-full.whitespace-nowrap.rounded-lg.border
                thead
                  tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                    th.px-1.py-1.text-center.border.sticky.w-10.l-0 STT
                    th.px-1.py-1.text-center.border.border.sticky.w-10.l-0 Mã HS
                    th.px-1.py-1.border Họ tên
                    th.px-1.py-1.border Trạng thái (toàn khóa học)

                tbody.bg-white
                  tr.text-gray-700(v-for="(student, index) in students" :key="student.id")
                    td.px-2.py-1.border.text-center {{ index + 1 }}
                    td.px-2.py-1.border {{ student.id }}
                    td.px-2.py-1.border {{ student.name }}
                    td.px-2.py-1.border
                      span {{ student.score }} / {{ total }} --->
                      span(:style="student.score / total < 0.85 ? 'color: red' : 'color: green'") {{ student.score / total < 0.85 ? 'Chưa đạt' : 'Đạt' }}
          h1.flex.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
            svg.h-6.w-6.mr-1(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
              path(stroke-linecap='round' stroke-linejoin='round' d='M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6')
            div Kết quả làm bài file
          .rounded-lg.overflow-auto.shadow-xs.mt-4(class="lg:px-10")
            .w-full.overflow-auto.rounded-lg(style="max-height: 600px; max-width: 1550px;")
              v-list
                v-list-group(
                  v-for="student, index in students" :key='index' no-action
                )
                  template(v-slot:activator='')
                    v-list-item
                      span {{ student.name }}
                  v-list-item(v-for="result in student.homeWorkFileResults")
                    span {{ result.homeWorkFile.description }}
                    v-spacer
                    i.watch(@click="watchFile(result.homeWorkFile.file_url)") xem đề
                    v-spacer
                    i.watch(@click="watchFile(result.file_result_url)") bài làm
                    v-spacer
                    v-checkbox(
                      readonly
                      :label="Number(result.score) >= 8 ? 'Đạt' : 'Chưa đạt'"
                      :value="Number(result.score) >= 8"
                      color="blue"
                    )
                    v-spacer
                    button.flex.mt-4.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(
                      @click="onAddScore(result)"
                      class='hover:bg-orange-300 focus:outline-none'
                    )
                      span.text-base Chấm điểm
                  v-divider
    add-score-dialog(
      :value="isAddScoreDialog"
      :home-work="curHomeWorkFile"
      :re-load="getData"
      @on-close="isAddScoreDialog = false"
    )
</template>

<script>
import { defineComponent, ref, onMounted, getCurrentInstance } from 'vue'
import { HeaderBar, MenuComponent, AddScoreDialog } from '@/components'
import { api } from '@/plugins'
import { endpoints } from '@/utils'

const HomeWorkScore = defineComponent({
  components: {
    HeaderBar, MenuComponent, AddScoreDialog
  },
  setup() {
    const { $toast, $route } = getCurrentInstance().proxy
    const classroomID = $route.params.classroomId
    const homeWorkResults = ref([])
    const homeWorks = ref([])
    const homeWorkFiles = ref([])
    const homeWorkFileResults = ref([])
    const students = ref([])
    const total = ref(0)
    const isAddScoreDialog = ref(false)
    const curHomeWorkFile = ref({})

    const calculator = () => {
      total.value = homeWorks.value.filter(e => e.have_to_do).length

      students.value = students.value.map(student => {
        return {
          ...student,
          score: homeWorkResults.value.filter(homeWorkResult => {
            return homeWorkResult.student === student.id && homeWorkResult.is_correct
          }).length,
          homeWorkFileResults: homeWorkFileResults.value.filter(homeWorkFileResult => {
            return homeWorkFileResult.student === student.id
          }).map(homeWorkFileResult => {
            return {
              ...homeWorkFileResult,
              homeWorkFile: homeWorkFiles.value.find(homeWorkFile => homeWorkFile.id === homeWorkFileResult.home_work_file)
            }
          })
        }
      })
    }

    const getData = async () => {
      try {
        const data = await Promise.all([
          api.get(`${endpoints.HOME_WORK_RESULT}?classroom=${classroomID}`),
          api.get(`${endpoints.HOME_WORK}?classroom=${classroomID}`),
          api.get(`${endpoints.STUDENT}?classroom=${classroomID}`),
          api.get(`${endpoints.HOME_WORK_FILE}?classroom=${classroomID}`),
          api.get(`${endpoints.HOME_WORK_FILE_RESULT}?classroom=${classroomID}`)
        ])

        const [{ data: hwrData }, { data: hwData }, { data: stuData }, { data: hwfData }, { data: hwfrData }] = data

        homeWorkResults.value = hwrData
        homeWorks.value = hwData
        students.value = stuData
        homeWorkFiles.value = hwfData
        homeWorkFileResults.value = hwfrData
      } catch (e) {
        $toast.error('Get data failed')
      }
      calculator()
    }

    const watchFile = (url) => {
      window.open(url)
    }

    const onAddScore = (result) => {
      curHomeWorkFile.value = result
      console.log(curHomeWorkFile.value)
      isAddScoreDialog.value = true
    }

    onMounted(async () => {
      await getData()
    })

    return {
      students,
      homeWorkResults,
      homeWorks,
      total,
      homeWorkFiles,
      homeWorkFileResults,
      watchFile,
      onAddScore,
      isAddScoreDialog,
      curHomeWorkFile,
      getData
    }
  }
})

export default HomeWorkScore
</script>

<style lang="sass" scoped>
.watch
  cursor: pointer
  text-decoration: underline
  color: #0e68af
</style>