<template lang="pug">
  .bg-gray-50.min-h-screen
    header-bar
    .flex.flex-col(class="md:flex-row")
      menu-component(:is-admin="false")
      .w-full.border-l
        #main.main-content.flex-1.py-20(class='md:pb-5')
          .px-4.text-gray-700(class='md:px-8')
            .flex.gap-2.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
              svg.h-5.w-5(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
                path(stroke-linecap='round' stroke-linejoin='round' d='M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z')
                path(stroke-linecap='round' stroke-linejoin='round' d='M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z')
              div Điểm số
            .items-center.mt-4.gap-36(class='md:flex')
              h1.py-2
                | Tên lớp:
                span Toán cao cấp
              h1.py-2
                | Sĩ số:
                span 32
              v-btn(
                v-if="member.type_member === 'teacher'"
                @click="handleClickAddCol()"
              ) {{ addCols ? 'Hủy nhập' : 'Nhập điểm'}}
            // Danh sách sinh viên
            .rounded-lg.overflow-auto.shadow-xs.mt-4(class='lg:px-10')
              .w-full.overflow-auto.rounded-lg(
                 v-if="member.type_member === 'teacher'"
                style='max-height: 600px; max-width: 1550px;'
              )
                table.w-full.whitespace-nowrap.rounded-lg.border
                  thead
                    tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                      th.px-2.py-1.text-center.border.sticky.w-44.l-0 STT
                      th.px-2.py-1.border.w-44 Mã học viên
                      th.px-2.py-1.border.w-44 Họ tên
                      th.px-2.py-1.border.w-44(
                        v-for="(scoreData, index) in scoreDatas" :key="scoreData.date"
                        @click="editDate(scoreData.date, index)"
                      )
                        span {{ scoreData.date }}
                      th.px-2.py-1.border.text-click-able(v-if="addCols" @click="editDate(dateAddScore)")
                        span {{ dateAddScore }}
                      //th.px-2.py-1.border Trung bình
                      th.px-2.py-1.border Ghi chú
                  tbody.bg-white
                    tr.text-gray-700(v-for="(student, index) in studentDatas" :key="student.id")
                      td.px-2.py-1.border.text-center {{ index + 1 }}
                      td.px-2.py-1.border {{ student.id }}
                      td.px-2.py-1.border {{ student.name }}
                      td.px-2.py-1.border(v-for="scoreData in scoreDatas" :key="scoreData.date")
                        //span.text-click-able {{ scoreData.data }}
                        span L:{{ scoreData.data.find(e => e.student.id === student.id)?.listening || '_' }} {{ ' ' }}
                        span S:{{ scoreData.data.find(e => e.student.id === student.id)?.specking || '_' }} {{ ' ' }}
                        span R:{{ scoreData.data.find(e => e.student.id === student.id)?.reading || '_' }} {{ ' ' }}
                        span W:{{ scoreData.data.find(e => e.student.id === student.id)?.writing || '_' }} {{ ' ' }}
                      td.px-2.py-1.text-sm.border.text-center(v-if="addCols")
                        v-text-field.pa-0.ma-0(
                          label="Nghe" hide-details
                          type="number" v-model="student.score.listening"
                        )
                        v-text-field.pa-0.ma-0(
                          label="Nói" hide-details
                          type="number" v-model="student.score.specking"
                        )
                        v-text-field.pa-0.ma-0(
                          label="Đọc" hide-details
                          type="number" v-model="student.score.reading"
                        )
                        v-text-field.pa-0.ma-0(
                          label="Viết" hide-details
                          type="number" v-model="student.score.writing"
                        )

                      //td.px-2.py-1.text-sm.border.text-center
                      //  span {{ student.average ? student.average.toFixed(2) : '' }}
                      td.px-2.py-1.text-sm.border

              .w-full.overflow-auto.rounded-lg(
                 v-if="member.type_member === 'student'"
                style='max-height: 600px; max-width: 1550px;'
              )
                table.w-full.whitespace-nowrap.rounded-lg.border
                  thead
                    tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                      th.px-2.py-1.border.w-44 Mã học viên
                      th.px-2.py-1.border.w-44 Họ tên
                      th.px-2.py-1.border.w-44 Ngày
                      th.px-2.py-1.border.w-44 Điểm
                  tbody.bg-white
                    tr.text-gray-700(v-for="scoreData in scoreDatas")
                      td.px-2.py-1.border {{ member.id }}
                      td.px-2.py-1.border {{ member.name }}
                      td.px-2.py-1.border {{ scoreData.data.find(e => e.student.id === member.id).date }}
                      td.px-2.py-1.border
                        span L:{{ scoreData.data.find(e => e.student.id === member.id)?.listening || '_' }} {{ ' ' }}
                        span S:{{ scoreData.data.find(e => e.student.id === member.id)?.specking || '_' }} {{ ' ' }}
                        span R:{{ scoreData.data.find(e => e.student.id === member.id)?.reading || '_' }} {{ ' ' }}
                        span W:{{ scoreData.data.find(e => e.student.id === member.id)?.writing || '_' }} {{ ' ' }}
                      //td.px-2.py-1.border {{ scoreData.data.find(e => e.student.id === member.id).score.join(', ') }}

            v-btn(v-if="addCols" style="margin-left: 77%" @click="onSave()") Lưu

            //.rounded-lg.overflow-auto.shadow-xs.mt-4(class='lg:px-10')
            //  .w-full.overflow-auto.rounded-lg(
            //     v-if="member.type_member === 'teacher'"
            //    style='max-height: 600px; max-width: 1550px;'
            //  )
            //    table.w-full.whitespace-nowrap.rounded-lg.border
            //      thead
            //        tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
            //          th.px-2.py-1.text-center.border.sticky.w-44.l-0 STT
            //          th.px-2.py-1.border.w-44 Họ tên
            //          th.px-2.py-1.border.w-44(v-for="unit in units" :key="unit.id")
            //            span {{ unit.title }}
            //
            //      tbody.bg-white
            //        tr.text-gray-700(v-for="(scoreHomeWork, index) in scoreHomeWorks" :key="scoreHomeWork.id")
            //          td.px-2.py-1.border.text-center {{ index + 1 }}
            //          td.px-2.py-1.border {{ scoreHomeWork.name }}
            //            //span {{ scoreHomeWork }}
            //          th.px-2.py-1.border.w-44(v-for="(unit, indexUnit) in scoreHomeWork.result")
            //            span {{ unit[units[indexUnit].id] }}
            //
            //  .w-full.overflow-auto.rounded-lg(
            //     v-if="member.type_member === 'student'"
            //    style='max-height: 600px; max-width: 1550px;'
            //  )
            //    table.w-full.whitespace-nowrap.rounded-lg.border
            //      thead
            //        tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
            //          th.px-2.py-1.border.w-44 Mã học viên
            //          th.px-2.py-1.border.w-44 Họ tên
            //          th.px-2.py-1.border.w-44(v-for="unit in units" :key="unit.id")
            //            span {{ unit.title }}
            //      tbody.bg-white
            //        td.px-2.py-1.border {{ member.id }}
            //        td.px-2.py-1.border {{ member.name }}
            //        th.px-2.py-1.border.w-44(v-for="(unit, indexUnit) in scoreHomeWorks.find(e => e.id === member.id).result")
            //          span {{ unit[units[indexUnit].id] }}

    v-dialog.title-color(
      ref="dialog"
      persistent
      max-width="400"
      :return-value.sync="date"
      v-model="modal"
    )
      v-date-picker.title-color(full-width scrollable v-model="date")
        v-spacer
        v-btn(text color="light_red" @click="modal = false")
          span Cancel
        v-btn(text color="rough_black" @click="$refs.dialog.save(date), savaDate()")
          span Ok

</template>

<script>
import { defineComponent, ref, onMounted, getCurrentInstance } from 'vue'
import { api } from '@/plugins'
import { endpoints } from '@/utils'
import moment from 'moment'
import { EditRollCallDialog, HeaderBar, MenuComponent } from '@/components'

const Score = defineComponent({
  components: {
    EditRollCallDialog,
    HeaderBar,
    MenuComponent
  },
  setup() {
    const { $toast, $route } = getCurrentInstance().proxy
    const addCols = ref(false)
    const studentDatas = ref([])
    // studentDatas.value = JSON.parse(JSON.stringify(props.students))
    const member = JSON.parse(localStorage.getItem('token'))
    const dateAddScore = ref(moment(new Date()).format('YYYY-MM-DD'))
    const scoreDatas = ref([])
    const scoreHomeWorks = ref([])
    const modal = ref(false)
    const date = ref(moment(new Date()).format('YYYY-MM-DD'))
    const currentIndexDate = ref(0)
    const classroomID = $route.params.classroomId
    const students = ref([])
    const units = ref([])
    const classroom = ref({})

    const handleClickAddCol = () => {
      studentDatas.value = students.value.map((studentData) => {
        return {
          ...studentData,
          score: { specking: null, reading: null, writing: null, listening: null }
        }
      })
      addCols.value = !addCols.value
    }

    const getData = async () => {
      try {
        const data = await Promise.all([
          api.get(`${endpoints.CLASSROOM}${classroomID}`),
          api.get(`${endpoints.STUDENT}?classroom=${classroomID}`),
          api.get(`${endpoints.SCORE}?classroom=${classroomID}`)
          // api.get(`${endpoints.HOME_WORK_STUDENT}check_rate_corrects?classroom_id=${classroomID}`),
          // api.get(`${endpoints.SCHEDULE}?classroom=${classroomID}`)
        ])
        const [
          { data: classData },
          { data: stuData },
          { data: scoreData }
          // { data: homeworkData },
          // { data: unitData }
        ] = data
        classroom.value = classData
        students.value = stuData
        // units.value = unitData
        // scoreHomeWorks.value = homeworkData
        // const { data } = await api.get(`${endpoints.SCORE}?class_room=${classroomID}`)
        scoreDatas.value = scoreData

        studentDatas.value = JSON.parse(JSON.stringify(students.value))
      } catch {
        $toast.error('Get data failed')
      }
    }

    const reload = async () => {
      await getData()
    }

    const addScoreAPI = async () => {
      const params = ref([])
      studentDatas.value.forEach((studentData) => {
        params.value.push({
          date: dateAddScore.value,
          classroom: classroomID,
          student: studentData.id,
          teacher: member.id,
          specking: studentData.score.specking ? Number(studentData.score.specking) : null,
          reading: studentData.score.reading ? Number(studentData.score.reading) : null,
          writing: studentData.score.writing ? Number(studentData.score.writing) : null,
          listening: studentData.score.listening ? Number(studentData.score.listening) : null
        })
      })
      try {
        await api.post(`${endpoints.SCORE}`, params.value)
        $toast.success('Save data successful')
      } catch {
        $toast.error('Add data failed')
      }
      await reload()
    }

    const onSave = async () => {
      const validate = studentDatas.value.find((e) => Number(e.score) > 10)
      if (validate) $toast.error('Điểm chỉ được phép từ 0 -> 10')
      else await addScoreAPI()
      addCols.value = false
    }

    const editDate = (dateData, indexDate=null) => {
      date.value = dateData
      if (indexDate) currentIndexDate.value = indexDate
      modal.value = true
    }

    const savaDate = () => {
      if (addCols.value) dateAddScore.value = date.value
      else scoreDatas.value[currentIndexDate.value].date = date.value
    }

    onMounted(async () => {
      await getData()
    })

    return {
      addCols,
      studentDatas,
      handleClickAddCol,
      onSave,
      dateAddScore,
      scoreDatas,
      member,
      scoreHomeWorks,
      editDate,
      modal,
      date,
      savaDate,
      units
    }
  }
})

export default Score
</script>

<style scoped lang="sass">
.v-text-field__details
  display: none !important
.v-text-field__slot input
  margin: 2px !important
  padding: 0 !important
.text-click-able
  text-decoration: underline
  color: blue
  cursor: pointer
.title-color
  background-color: #FBB232 !important
</style>
