<template lang="pug">
  dialog-container(
    :label="'Lớp'"
    :mode="isAdd ? 'create' : 'update'"
    :height="'40%'"
    @on-close="$emit('on-close')"
    @on-update="update"
    @on-create="create"
    @on-remove="remove"
    v-model="value"
  )
    v-text-field.p-0(:label="'môn'" v-model="classroomData.name")
    v-text-field.p-0(:label="'phòng'" v-model="classroomData.room")

</template>

<script>
import { defineComponent, ref, watch, getCurrentInstance } from 'vue'
import { api } from '@/plugins'
import { endpoints } from '@/utils'
import { DialogContainer } from '@/components'

const ClassroomDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    isAdd: {
      type: Boolean,
      default: false
    },
    classroom: {
      type: Object,
      required: true
    }
  },
  components: {
    DialogContainer
  },
  setup(props, { emit }) {
    const { $toast } = getCurrentInstance().proxy
    const classroomData = ref({})

    const create = async () => {
      try {
        await api.post(`${endpoints.CLASSROOM}`, classroomData.value)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const update = async () => {
      try {
        await api.put(`${endpoints.CLASSROOM}${classroomData.value.id}`, classroomData.value)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const remove = async () => {
      try {
        await api.delete(`${endpoints.CLASSROOM}${classroomData.value.id}`)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const init = () => {
      if (props.value) {
        if (props.isAdd) classroomData.value = { name: null, room: null }
        else classroomData.value = JSON.parse(JSON.stringify(props.classroom))
      }
    }

    watch(
      () => props.value,
      () => init()
    )

    return {
      classroomData,
      create,
      update,
      remove
    }
  }
})

export default ClassroomDialog
</script>

<style lang="sass">
.v-picker__title
  background-color: beige !important
  color: #343f4b !important
.v-date-picker-table .v-btn.v-btn--active
  background-color: beige !important
  color: #343f4b !important
</style>
