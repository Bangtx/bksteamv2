<template lang="pug">
  .bg-gray-50.min-h-screen
    header-bar
    .flex.flex-col(class="md:flex-row")
      menu-component(:is-admin="false")
      .w-full.border-l
        #main.main-content.flex-1.py-20(class='md:pb-5')
          .px-4.text-gray-700(class='md:px-8')
            h1.flex.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
              svg.h-6.w-6.mr-1(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
                path(stroke-linecap='round' stroke-linejoin='round' d='M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6')
              div Trang chủ
            .items-center.mt-4.gap-36(class='md:flex')
              h1.py-2
                | Tên lớp:
                span {{ classroom.name }}

            div(v-for="(unit, index) in units" :key="index")
              v-list-item(@click="currentUnit=unit, openUnitDialog('edit')")
                span {{ index + 1 }}: {{ unit.title }}
              v-divider

            button.mt-4.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(
              v-if="member.type_member === 'teacher'"
              class='hover:bg-orange-300 focus:outline-none'
              @click="openUnitDialog('add')"
            )
              span.text-base Thêm Unit
            h1.py-2.flex.gap-2.items-center
              div Danh sách sinh viên
            // Danh sách sinh viên
            .w-full.overflow-hidden.rounded-lg.shadow-xs.mt-4(class='lg:px-10')
              .w-full.overflow-auto.rounded-lg(style='max-height: 600px;')
                table.w-full.whitespace-nowrap.rounded-lg.border
                  thead
                    tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                      th.px-4.py-3.text-center.border STT
                      th.px-4.py-3.border Tiêu đề
                      th.px-4.py-3.border File
                      th.px-4.py-3.border Ghi chú
                  tbody.bg-white(v-for="(slide, index) in slides" :key="slide.id")
                    tr.text-gray-700
                      td.px-4.py-3.border.text-center {{ index }}
                      td.px-4.py-3.border {{ slide.title }}
                      td.px-4.py-3.text-sm.border(@click="openFile(slide.url)") xem
                      td.px-4.py-3.text-sm.border {{ slide.remark }}

            button.mt-4.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(
              v-if="member.type_member === 'teacher'"
              class='hover:bg-orange-300 focus:outline-none'
              @click="openSlideDialog()"
            )
              span.text-base Thêm Bài giảng

    unit-dialog(
      :value="isOpenUnitDialog"
      :classroom="classroom"
      :unit="currentUnit"
      :is-add="isAddUnit"
      @re-load="reload()"
      @on-close="isOpenUnitDialog = false"
    )

    add-content-date(
      :value="isOpenSlideDialog"
      :slide="slideProps"
      @on-close="isOpenSlideDialog = false"
      @reload="reload"
    )
</template>

<script>
import { defineComponent, onMounted, ref, getCurrentInstance } from 'vue'
import { UnitDialog, AddContentDate, HeaderBar, MenuComponent, BottomSheet } from '@/components'
import { endpoints } from '@/utils'
import { api } from '@/plugins'

const ClassHome = defineComponent({
  components: {
    UnitDialog,
    AddContentDate,
    HeaderBar,
    MenuComponent,
    BottomSheet
  },
  setup() {
    const { $toast, $route } = getCurrentInstance().proxy
    const isOpenUnitDialog = ref(false)
    const currentUnit = ref({})
    const showBottomSheet = ref(false)
    const member = JSON.parse(localStorage.getItem('token'))
    const isOpenSlideDialog = ref(false)
    const classroomID = $route.params.classroomId
    const isAddUnit = ref(false)

    const classroom = ref({})
    const units = ref([])
    const slides = ref([])

    const slideProps = ref({
      title: null,
      classroom: null,
      url: null,
      remark: null
    })

    const openUnitDialog = (mode) => {
      if (member.type_member === 'teacher') {
        isAddUnit.value = mode === 'add'
        isOpenUnitDialog.value = true
      }
    }

    const openSlideDialog = () => {
      isOpenSlideDialog.value = true
    }

    const reload = () => {
      getData()
    }

    const openBottomSheet = (unit) => {
      currentUnit.value = unit
      showBottomSheet.value = true
    }

    const openFile = (url) => {
      window.open(url)
    }

    const getData = async () => {
      try {
        const data = await Promise.all([
          api.get(`${endpoints.CLASSROOM}${classroomID}`),
          api.get(`${endpoints.UNIT}?classroom=${classroomID}`),
          api.get(`${endpoints.SLIDE}?classroom=${classroomID}`)
        ])
        const [{ data: ClassData }, { data: UnitData }, { data: SlideData }] = data

        classroom.value = ClassData
        units.value = UnitData
        slides.value = SlideData
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    onMounted(async () => {
      await getData()
    })

    return {
      openUnitDialog,
      isOpenUnitDialog,
      reload,
      openBottomSheet,
      showBottomSheet,
      member,
      openSlideDialog,
      isOpenSlideDialog,
      slideProps,
      openFile,
      classroom,
      slides,
      units,
      currentUnit,
      isAddUnit
    }
  }
})

export default ClassHome
</script>
