<template lang="pug">
  dialog-container(
    :label="'Question'"
    :mode="isAdd ? 'create' : 'update'"
    @on-close="$emit('on-close')"
    @on-update="update"
    @on-create="create"
    v-model="value"
  )
    v-dialog(
      ref="startDialog"
      persistent
      width="90vw"
      max-width="500px"
      :return-value.sync="questionFileData.date"
      v-model="dateModal"
    )
      template(v-slot:activator="{ on, attrs }")
        v-text-field(
          readonly
          hide-details
          v-bind="attrs"
          v-on="on"
          append-icon="mdi-calendar-range"
          label="Ngày"
          :value="questionFileData.date"
          @click:append-outer="dateModal = true"
        )
      v-date-picker.title-color(
        color="rough_black"
        header-color="rough_black"
        v-model="questionFileData.date"
        full-width
      )
        v-spacer
        v-btn.white--text(dark text color="light_red" @click="dateModal = false")
          span cancel
        v-btn.white--text(dark text color="rough_black" @click="$refs.startDialog.save(questionFileData.date), dateModal = false")
          span ok
    v-autocomplete(
      clearable
      item-text="title" item-value="id"
      :items="units"
      :label="'Unit'"
      v-model="questionFileData.unit"
    )
    v-text-field(label="Mô tả chung" v-model="questionFileData.description" )
    v-text-field(label="Link driver (cấp quyền xem)" v-model="questionFileData.file_url" )
    i.watch(v-if="questionFileData.file_url?.length > 0" @click="watchFile()") xem ngay
    v-checkbox(label="Bắt buộc" v-model="questionFileData.have_to_do")
    v-divider
    v-checkbox(label="Bài Tập Riêng" :value="!questionFileData.is_global" @click="questionFileData.is_global = !questionFileData.is_global")
    v-autocomplete(
      multiple
      item-text="name"
      item-value="id"
      :items="students"
      v-model="questionFileData.student_ids"
    )

</template>

<script>
import { defineComponent, ref, watch, getCurrentInstance, onMounted } from 'vue'
import VuetifyAudio from 'vuetify-audio/src/vuetifyaudio.vue'
import { api } from '@/plugins'
import { endpoints } from '@/utils'
import DialogContainer from '../DialogContainer/index'
import { QUESTION_INIT } from './index'
import { VueEditor } from 'vue2-editor'

const QuestionFileDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    units: {
      type: Array,
      required: true
    },
    classroom: {
      type: Object,
      required: true
    },
    questionFile: {
      type: Object,
      required: true
    },
    isAdd: {
      type: Boolean,
      default: false
    }
  },
  components: { DialogContainer, VuetifyAudio, VueEditor },
  setup(props, { emit }) {
    const { $toast, $route } = getCurrentInstance().proxy
    const questionFileData = ref({})
    const dateModal = ref(false)
    const classroomID = $route.params.classroomId
    const students = ref([])

    const getData = async () => {
      try {
        const { data } = await api.get(`${endpoints.STUDENT}?classroom=${classroomID}`)
        students.value = data
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    const update = async () => {
      try {
        await api.put(`${endpoints.HOME_WORK_FILE}`, questionFileData.value)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const create = async () => {
      console.log(questionFileData.value)
      try {
        await api.post(`${endpoints.HOME_WORK_FILE}`, questionFileData.value)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const watchFile = () => {
      window.open(questionFileData.value.file_url)
    }

    const init = async () => {
      if (props.value) {
        if (props.isAdd) questionFileData.value = JSON.parse(JSON.stringify(QUESTION_INIT))
        else questionFileData.value = JSON.parse(JSON.stringify(props.questionFile))
        questionFileData.value.classroom = classroomID
      }
    }

    watch(
      () => props.value,
      () => init()
    )

    watch(
      () => questionFileData.value,
      () => {
        console.log(questionFileData.value)
      }, {
        deep: true
      }
    )

    onMounted(getData)

    return {
      dateModal,
      update,
      create,
      questionFileData,
      watchFile,
      getData,
      students
    }
  }
})

export default QuestionFileDialog
</script>

<style lang="sass" scoped>
.container
  display: grid
  grid-gap: 25px
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr))
.container > div
  object-fit: cover
.watch
  cursor: pointer
  text-decoration: underline
  color: #0e68af
.title-color
  background-color: #FBB232 !important
::v-deep .v-date-picker-table .v-btn.v-btn--active
  background-color: #FBB232 !important
</style>
