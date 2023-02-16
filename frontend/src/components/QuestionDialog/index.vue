<template lang="pug">
  dialog-container(
    :label="'Question'"
    :mode="questionData.id ? 'update' : 'create'"
    :width="1000"
    @on-close="$emit('on-close')"
    @on-update="update"
    @on-create="create"
    @on-remove="remove"
    v-model="value"
  )
    .pa-2
      v-row
        v-col(cols="12")
        v-col(cols="12" sm="6")
          v-dialog(
            ref="startDialog"
            persistent
            width="90vw"
            max-width="500px"
            :return-value.sync="questionData.date"
            v-model="dateModal"
          )
            template(v-slot:activator="{ on, attrs }")
              v-text-field(
                outlined
                dense
                readonly
                hide-details
                v-bind="attrs"
                v-on="on"
                append-icon="mdi-calendar-range"
                label="Từ ngày"
                :value="questionData.date"
                @click:append-outer="dateModal = true"
              )
            v-date-picker.title-color(
              color="rough_black"
              header-color="rough_black"
              v-model="questionData.date"
              full-width
            )
              v-spacer
              v-btn.white--text(dark text color="light_red" @click="dateModal = false")
                span cancel
              v-btn.white--text(dark text color="rough_black" @click="$refs.startDialog.save(questionData.date), dateModal = false")
                span ok
        v-col(cols="12" sm="6")
          v-autocomplete(
            clearable
            item-text="title" item-value="id"
            :items="units"
            :label="'Unit'"
            v-model="questionData.unit"
            hide-details
            dense
            outlined
          )
        v-col(cols="12" sm="6")
          v-checkbox(label="Trắc nghiệm" v-model="questionData.multi_choice")
        v-col(cols="12" sm="6")
          v-text-field(label="Audio" v-model="questionData.audio" hide-details dense outlined)
          i.watch(v-if="questionData.audio?.length > 0" @click="watchAudio()") xem ngay
        v-col.pa-0(cols="12")
          span Nội Dung
          vue-editor(v-model="questionData.question" )
          v-radio-group(v-if="questionData.multi_choice" row v-model="questionData.answer" )
            v-radio(:value="questionData.option_1" )
            v-text-field(v-model="questionData.option_1" )
            v-radio(:value="questionData.option_2" )
            v-text-field(v-model="questionData.option_2" )
            v-radio(:value="questionData.option_3" )
            v-text-field(v-model="questionData.option_3" )
        v-col.pa-0(cols="12")
          v-text-field(
            v-if="!questionData.multi_choice"
            label="Answer"
            v-model="questionData.answer"
            hide-details
            dense
            outlined
          )
        v-col.pa-0(cols="12")
          v-checkbox(label="Bắt buộc" v-model="questionData.have_to_do")
          //vuetify-audio(v-if="questionData.audio?.length > 0" :file="questionData.audio")
</template>

<script>
import { defineComponent, ref, watch, getCurrentInstance } from 'vue'
import VuetifyAudio from 'vuetify-audio/src/vuetifyaudio.vue'
import { api } from '@/plugins'
import { endpoints } from '@/utils'
import DialogContainer from '../DialogContainer/index'
import { QUESTION_INIT } from './index'
import { VueEditor } from 'vue2-editor'

const QuestionDialog = defineComponent({
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
    question: {
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
    const questionData = ref({})
    const dateModal = ref(false)
    const classroomID = $route.params.classroomId

    const update = async () => {
      try {
        await api.put(`${endpoints.HOME_WORK}`, questionData.value)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const create = async () => {
      try {
        await api.post(`${endpoints.HOME_WORK}`, questionData.value)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const remove = async () => {
      try {
        await api.delete(`${endpoints.HOME_WORK}${questionData.value.id}`)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const watchAudio = () => {
      window.open(questionData.value.audio)
    }

    const init = async () => {
      if (props.value) {
        if (props.isAdd) questionData.value = JSON.parse(JSON.stringify(QUESTION_INIT))
        else questionData.value = JSON.parse(JSON.stringify(props.question))
        questionData.value.classroom = classroomID
      }
    }

    watch(
      () => props.value,
      () => init()
    )

    return {
      update,
      create,
      remove,
      questionData,
      watchAudio,
      dateModal
    }
  }
})

export default QuestionDialog
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
