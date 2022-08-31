<template lang="pug">
  .bg-gray-50.min-h-screen
    header-bar(:isAdmin="true")
    .flex.flex-col(class="md:flex-row")
      menu-component(:is-admin="true")
      .w-full.border-l
        #main.main-content.flex-1.py-20(class='md:pb-5')
          .px-4.text-gray-700(class='md:px-8')
            .flex.gap-2.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
              svg.h-6.w-6(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
                path(stroke-linecap='round' stroke-linejoin='round' d='M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z')
              span Quản lí lớp
            .mt-4
              .items-center.justify-between(class='md:flex lg:px-10')
                .flex.border-2.border-gray-200.rounded.w-96
                  input.px-4.py-2.w-80(type='text' class='focus:outline-none' placeholder='Search...')
                  button.px-4.text-white.bg-orange-400.border-l.border-l-orange-400(class='hover:bg-orange-300')
                    span Search
                button.bg-green-600.text-white.px-4.py-2.rounded.mt-6(
                  class='hover:bg-green-500 md:mt-0'
                  @click="openClassroomDialog('add')"
                )
                  span + Thêm Lớp
              .w-full.overflow-hidden.rounded-lg.shadow-xs.mt-4(class='lg:px-10')
                .w-full.overflow-auto.rounded-lg(style='max-height: 600px;')
                  table.w-full.whitespace-nowrap.rounded-lg.border
                    thead
                      tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                        th.px-4.py-3.text-center.border STT
                        th.px-4.py-3.border Mã Lớp
                        th.px-4.py-3.border Môn
                        th.px-4.py-3.border.text-center Tùy chọn
                    tbody.bg-white
                      tr.text-gray-700(v-for="(item, index) in classrooms" :key="item.id")
                        td.px-4.py-3.border.text-center {{ index + 1 }}
                        td.px-4.py-3.border.text-center {{ item.id }}
                        td.px-4.py-3.border {{ item.name }}
                        td.px-4.py-3.text-sm.border
                          .flex.items-center.justify-center.gap-4
                            button.bg-green-600.text-white.px-4.py-2.rounded.mt-6(
                              class='hover:bg-green-500 md:mt-0'
                              @click="curClassroom=item, openClassroomDialog('edit')"
                            )
                              span Sửa

    classroom-dialog(
      :value="isOpenDialog"
      :is-add="isAdd"
      :classroom="curClassroom"
      @on-close="isOpenDialog = false"
      @re-load="reload"
    )

</template>

<script>
import { defineComponent, onMounted, ref, getCurrentInstance } from 'vue'
import { api } from '@/plugins'
import { HeaderBar, MenuComponent } from '@/components'
import { endpoints } from '@/utils'
import ClassroomDialog from './ClassRoomDialog'

const ClassroomManagement = defineComponent({
  components: { MenuComponent, HeaderBar, ClassroomDialog },
  setup() {
    const { $toast } = getCurrentInstance().proxy
    const classrooms = ref([])
    const curClassroom = ref({})
    const isAdd = ref(false)
    const isOpenDialog = ref(false)

    const getData = async () => {
      try {
        const { data } = await api.get(`${endpoints.CLASSROOM}`)
        classrooms.value = data
      } catch {
        $toast.error('Get data failed')
      }
    }

    const reload = async () => {
      await getData()
    }

    const openClassroomDialog = (mode) => {
      isAdd.value = mode === 'add'
      isOpenDialog.value = true
      console.log(curClassroom.value)
    }

    onMounted(async () => {
      await getData()
    })

    return {
      classrooms,
      reload,
      openClassroomDialog,
      isAdd,
      curClassroom,
      isOpenDialog
    }
  }
})

export default ClassroomManagement
</script>

<style lang="sass"></style>
