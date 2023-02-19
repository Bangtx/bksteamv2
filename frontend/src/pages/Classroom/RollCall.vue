<template lang="pug">
  .bg-gray-50.min-h-screen
    header-bar
    .flex.flex-col(class="md:flex-row")
      menu-component(:is-admin="false")
      .w-full.border-l
        #main.main-content.flex-1.py-20(class="md:pb-5")
          .px-4.text-gray-700(class="md:px-8")
            .flex.gap-2.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
              svg.w-6.h-6(aria-hidden="true" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" stroke="currentColor")
                path(d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01")
              div Điểm danh
            .items-center.mt-4.gap-36(class="md:flex")
              h1.py-2
                span Tên lớp: {{ classroom.name }}
              h1.py-2
                span Sĩ số: {{ students.length }}

              v-btn(
                v-if="member.type_member === 'teacher'"
                @click="handleClickRollCall()"
              ) {{ 'Điểm danh'}}

            .rounded-lg.overflow-auto.shadow-xs.mt-4(class="lg:px-10")
              .w-full.overflow-auto.rounded-lg(style="max-height: 600px; max-width: 1550px;")
                v-data-table(
                  v-if="member.type_member === 'teacher'"
                  :headers="HeadersTable"
                  :items="bodyTable"
                  item-key="name"
                  class="elevation-1"
                )
                  template(v-slot:item.actions='{ item }')
                    v-icon.mr-2(small='' @click='editItem(item)')
                      | mdi-pencil
                    v-icon(small='' @click='deleteItem(item)')
                      | mdi-delete

              .w-full.overflow-auto.rounded-lg(style="max-height: 600px; max-width: 1550px;")
                table.w-full.whitespace-nowrap.rounded-lg.border(
                  v-if="member.type_member === 'student'"
                )
                  thead
                    tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                      th.px-1.py-1.border STT
                      th.px-1.py-1.border Ngày
                      th.px-1.py-1.border Tên
                      th.px-1.py-1.border Điểm danh
                  tbody.bg-white
                    tr.text-gray-700(v-for="(roll, index) in rollCalls" :key="roll.id")
                      td.px-2.py-1.border.text-center {{ index + 1 }}
                      td.px-2.py-1.border {{ roll.date }}
                      td.px-2.py-1.border {{ member.name }}
                      td.px-2.py-1.border {{ toAbsentTypeName(roll.roll_call[0]) }}

            //v-btn(v-if="addCols" style="margin-left: 77%" @click="onClickSubmit") submit

    v-dialog.title-color(
        ref="dialog"
        persistent
        max-width="400"
        :return-value.sync="date"
        v-model="modal"
      )
        v-date-picker(full-width scrollable color="rough_black" header-color="rough_black" v-model="date")
          v-spacer
          v-btn(text color="light_red" @click="modal = false")
            span Cancel
          v-btn(text color="rough_black" @click="$refs.dialog.save(date), savaDate()")
            span Ok

    edit-roll-call-dialog(
      :value="isShowEdit"
      :data="rollCallProps"
      :absent-types="absentTypes"
      :students="students"
      :classroom="classroom"
      :teacher="teacher"
      :date="date"
      @on-close="isShowEdit = false"
      @reload="getData"
    )

</template>

<script>
import { defineComponent, ref, onMounted, getCurrentInstance, computed } from 'vue'
import { api } from '@/plugins'
import { endpoints } from '@/utils'
import moment from 'moment'
import { EditRollCallDialog, HeaderBar, MenuComponent } from '@/components'

const RollCall = defineComponent({
  components: {
    EditRollCallDialog,
    HeaderBar,
    MenuComponent
  },
  setup() {
    const { $toast, $route } = getCurrentInstance().proxy
    const absentTypes = [
      {id: 1, name: 'Đúng giờ'},
      {id: 2, name: 'Nghỉ có phép'},
      {id: 3, name: 'Nghỉ không phép'},
      {id: 4, name: 'Muộn có phép'},
      {id: 5, name: 'Muộn không phép'}
    ]
    const rollCalls = ref([])
    const alreadyRollCall = ref(false)
    const modal = ref(false)
    const date = ref(moment(new Date()).format('YYYY-MM-DD'))
    const currentIndexDate = ref(0)
    const dateAddScore = ref(moment(new Date()).format('YYYY-MM-DD'))
    const isShowEdit = ref(false)
    const rollCallProps = ref({
      teacher: null,
      date: null,
      absent_type: null,
      classroom: null
    })
    const classroomID = $route.params.classroomId
    const classroom = ref({})
    const students = ref([])
    const teacher = ref({})

    const HeadersTable = computed(() => {
      return [{text: 'date', value: 'date'}].concat(
        students.value.map(student => {
          return {text: student.name, value: String(student.id)}
        })
      ).concat({text: 'actions', value: 'actions'})
    })

    const bodyTable = computed(() => {
      return rollCalls.value.map(rollCall => {
        const result = {}
        students.value.map(student => student.id).forEach(id => {
          result[id] = absentTypes.find(abs => {
            return abs.id === rollCall.roll_call.find(e => e.student.id === id)?.absent_type
          })?.name
        })
        return {
          ...result,
          date: rollCall.date
        }
      })
    })

    const member = JSON.parse(localStorage.getItem('token'))

    const getData = async () => {
      try {
        const data = await Promise.all([
          api.get(`${endpoints.CLASSROOM}${classroomID}`),
          api.get(`${endpoints.STUDENT}?classroom=${classroomID}`),
          api.get(`${endpoints.TEACHER}?classroom=${classroomID}`),
          api.get(`${endpoints.ROLLCALL}?classroom=${classroomID}`)
        ])

        const [{ data: ClassData }, { data: StuData }, { data: TeaData }, { data: rollCallData }] = data

        classroom.value = ClassData
        students.value = StuData
        teacher.value = TeaData[0]
        rollCalls.value = rollCallData
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    const getDataStudent = async () => {
      try {
        const data = await Promise.all([
          api.get(`${endpoints.CLASSROOM}${classroomID}`),
          api.get(`${endpoints.ROLLCALL}?classroom=${classroomID}&student=${member.id}`)
        ])
        const [{ data: ClassData }, { data: rollCallData }] = data

        classroom.value = ClassData
        rollCalls.value = rollCallData
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    const editItem = (row) => {
      rollCallProps.value = row
      date.value = row.date
      isShowEdit.value = true
    }

    const reload = async () => {
      await getData()
    }

    const saveRollCallAPI = async (query) => {
      try {
        await api.post(`${endpoints.ROLLCALL}create_roll_calls`, query)
        await reload()
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const onClickSubmit = () => {
      const query = students.value.map((e) => {
        return {
          date: dateAddScore.value,
          classroom: Number(classroomID),
          teacher: teacher.value.id,
          student: e.id,
          absent_type: e.absent_type || null
        }
      })
      if (rollCalls.value.filter(rc => rc.date === dateAddScore.value).length > 0) {
        $toast.info('Đã điểm danh')
        return
      }

      saveRollCallAPI(query)
    }

    const savaDate = () => {
      dateAddScore.value = date.value
    }

    const editDate = (dateData, indexDate=null) => {
      date.value = dateData
      if (indexDate) currentIndexDate.value = indexDate
      modal.value = true
    }

    const handleClickRollCall = () => {
      if (rollCalls.value.find(e => e.date === moment(new Date()).format('YYYY-MM-DD'))) {
        return
      }

      rollCallProps.value = {}
      Object.keys(students.value).forEach(key => {
        rollCallProps.value[key] = null
      })
      date.value = moment(new Date()).format('YYYY-MM-DD')
      isShowEdit.value = true
    }

    const toAbsentTypeName = (absentType) => {
      let ab = null
      if (absentType) {
        ab = absentTypes.find(e => e.id === absentType.absent_type)
        if (ab) return ab.name
      }
      return null
    }

    onMounted(async () => {
      if (member.type_member === 'student') {
        await getDataStudent()
      } else {
        await getData()
        alreadyRollCall.value =
          rollCalls.value.map((e) => e.date).indexOf(moment(new Date()).format('YYYY-MM-DD')) > -1
      }
    })
    return {
      absentTypes,
      rollCalls,
      onClickSubmit,
      alreadyRollCall,
      handleClickRollCall,
      member,
      modal,
      date,
      savaDate,
      dateAddScore,
      editDate,
      isShowEdit,
      rollCallProps,
      getData,
      classroom,
      teacher,
      students,
      toAbsentTypeName,
      HeadersTable,
      bodyTable,
      editItem
    }
  }
})

export default RollCall
</script>

<style scoped lang="sass">
select
  color: deeppink
  cursor: pointer
  border-color: #0E5A84
.text-click-able
  text-decoration: underline
  color: blue
  cursor: pointer
.v-text-field
  padding: 0 !important
  margin: 0 !important
.v-text-field__details
  display: none
</style>
