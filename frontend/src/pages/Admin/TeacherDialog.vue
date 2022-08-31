<template lang="pug">
  dialog-container(
    :label="'Giáo Viên'"
    :mode="isAdd ? 'create' : 'update'"
    :height="'40%'"
    @on-close="$emit('on-close')"
    @on-update="update"
    @on-create="create"
    @on-remove="remove"
    v-model="value"
  )
    v-text-field.p-0(:label="'Tên'" v-model="teacherData.name")
    v-text-field.p-0(:label="'Giới tinh'" v-model="teacherData.gender")
    v-text-field.p-0(:label="'mail'" v-model="teacherData.mail")
    v-text-field.p-0(:label="'Số đt'" v-model="teacherData.phone")
    v-autocomplete(
      multiple
      item-value="id"
      item-text="name"
      :items="classrooms"
      v-model="teacherData.classrooms"
    )

</template>

<script>
import { defineComponent, ref, watch, getCurrentInstance, onMounted } from 'vue'
import { api } from '@/plugins'
import { endpoints } from '@/utils'
import { DialogContainer } from '@/components'

const TeacherDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    isAdd: {
      type: Boolean,
      default: false
    },
    teacher: {
      type: Object,
      required: true
    }
  },
  components: {
    DialogContainer
  },
  setup(props, { emit }) {
    const { $toast } = getCurrentInstance().proxy
    const teacherData = ref({})
    const classrooms = ref([])

    const create = async () => {
      try {
        await api.post(`${endpoints.TEACHER}`, teacherData.value)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const update = async () => {
      try {
        await api.put(`${endpoints.TEACHER}${teacherData.value.id}`, teacherData.value)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const remove = async () => {
      try {
        await api.delete(`${endpoints.TEACHER}${teacherData.value.id}`)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const init = () => {
      if (props.value) {
        if (props.isAdd) teacherData.value = { name: null, gender: null, mail: null, phone: null, password: 'password' }
        else teacherData.value = JSON.parse(JSON.stringify(props.teacher))
      }
    }

    const getData = async () => {
      try {
        const { data } = await api.get(`${endpoints.CLASSROOM}`)
        classrooms.value = data
      } catch {
        $toast.error('Get data failed')
      }
    }

    onMounted(() => {
      getData()
    })

    watch(
      () => props.value,
      () => init()
    )

    return {
      teacherData,
      create,
      update,
      remove,
      classrooms
    }
  }
})

export default TeacherDialog
</script>

<style lang="sass">
.v-picker__title
  background-color: beige !important
  color: #343f4b !important
.v-date-picker-table .v-btn.v-btn--active
  background-color: beige !important
  color: #343f4b !important
</style>
