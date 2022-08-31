<template lang="pug">
  dialog-container(
    :label="'Đăng kí tự học'"
    :mode="isAdd ? 'create' : 'update'"
    :height="'40%'"
    @on-close="$emit('on-close')"
    @on-create="create"
    v-model="value"
  )
    v-dialog(
      ref="dialog"
      persistent
      :return-value.sync="dates"
      v-model="modal"
    )
      template(v-slot:activator="{ on, attrs }")
        v-text-field.pa-0.pr-1(
          :label="'Ngày'"
          readonly
          hide-details
          append-outer-icon="mdi-calendar"
          v-bind="attrs"
          v-on="on"
          :value="data.dates"
          @click:append-outer="modal = true"
        )
      v-date-picker.title-color(multiple full-width scrollable color="rough_black" header-color="rough_black" v-model="data.dates")
        v-spacer
        v-btn(text color="light_red" @click="modal = false")
          span Cancel
        v-btn(text color="rough_black" @click="$refs.dialog.save(data.dates)")
          span Ok
    v-autocomplete(
      v-if="data.type_member === 'teacher'"
      item-text="name"
      item-value="id"
      :items="students"
      v-model="data.student"
    )

</template>

<script>
import { defineComponent, ref, getCurrentInstance, onMounted } from 'vue'
import { api } from '@/plugins'
import { endpoints } from '@/utils'
import DialogContainer from '../DialogContainer/index'

const RegisterSelfLearningDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      requires: true
    },
    data: {
      type: Object,
      requires: true
    },
    isAdd: {
      type: Boolean,
      default: true
    }
  },
  components: { DialogContainer },
  setup(props, { emit }) {
    const { $toast, $route } = getCurrentInstance().proxy
    const modal = ref(false)
    const dates = ref([])
    const students = ref([])
    const classroomID = $route.params.classroomId

    const create = async () => {
      try {
        await api.post(`${endpoints.SELF_LEARNING}`, props.data)
        // selfLearnings.value = toCamelCase(data)
        emit('on-close')
        emit('reload')
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    const getData = async () => {
      try {
        const { data } = await api.get(`${endpoints.STUDENT}?classroom=${classroomID}`)
        students.value = data
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    onMounted(getData)

    return {
      create,
      modal,
      dates,
      students
    }
  }
})

export default RegisterSelfLearningDialog
</script>

<style scoped lang="sass">
.title-color
  background-color: #FBB232
  span
    color: white
::v-deep .v-date-picker-table .v-btn.v-btn--active
  background-color: #FBB232 !important
</style>