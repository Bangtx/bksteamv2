<template lang="pug">
  dialog-container(
    :label="'Học sinh'"
    :mode="isAdd ? 'create' : 'update'"
    :height="'40%'"
    @on-close="$emit('on-close')"
    @on-update="update"
    @on-create="create"
    @on-remove="remove"
    v-model="value"
  )
    v-text-field.p-0(:label="'Tên'" v-model="studentData.name")
    v-text-field.p-0(:label="'Giới tinh'" v-model="studentData.gender")
    v-text-field.p-0(:label="'mail'" v-model="studentData.mail")
    v-text-field.p-0(:label="'Số đt'" v-model="studentData.phone")
    v-autocomplete(
      multiple
      item-value="id"
      item-text="name"
      :items="classrooms"
      v-model="studentData.classrooms"
    )

</template>

<script>
import { defineComponent, ref, watch, getCurrentInstance, onMounted } from 'vue'
import { api } from '@/plugins'
import { endpoints } from '@/utils'
import { DialogContainer } from '@/components'

const StudentDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    isAdd: {
      type: Boolean,
      default: false
    },
    student: {
      type: Object,
      required: true
    }
  },
  components: {
    DialogContainer
  },
  setup(props, { emit }) {
    const { $toast } = getCurrentInstance().proxy
    const studentData = ref({})
    const classrooms = ref([])

    const create = async () => {
      try {
        await api.post(`${endpoints.STUDENT}`, studentData.value)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const update = async () => {
      try {
        await api.put(`${endpoints.STUDENT}${studentData.value.id}`, studentData.value)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const remove = async () => {
      try {
        await api.delete(`${endpoints.STUDENT}${studentData.value.id}`)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const init = () => {
      if (props.value) {
        if (props.isAdd) studentData.value = { name: null, gender: null, mail: null, phone: null, password: 'password' }
        else studentData.value = JSON.parse(JSON.stringify(props.student))
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
      studentData,
      create,
      update,
      remove,
      classrooms
    }
  }
})

export default StudentDialog
</script>

<style lang="sass">
.v-picker__title
  background-color: beige !important
  color: #343f4b !important
.v-date-picker-table .v-btn.v-btn--active
  background-color: beige !important
  color: #343f4b !important
</style>
