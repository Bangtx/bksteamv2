<template lang="pug">
  v-dialog(:value="value" max-width="500" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span Điểm danh
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close
      v-card-text
        v-text-field(readonly :value="data.date")
        v-autocomplete(
          label="Diem danh"
          :items="absentTypes"
          item-value="id"
          item-text="name"
          v-model="data.absent_type"
        )
      v-card-actions
        v-btn.relative-btn(
          :large="!$vuetify.breakpoint.xsOnly"
          block
          @click="onSave()"
        )
          span Lưu
</template>

<script>
import { defineComponent, watch, ref, getCurrentInstance } from 'vue'
import { api } from '@/plugins'
import { endpoints } from '@/utils'

const EditRollCallDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    data: {
      type: Object,
      required: true
    },
    isSelfLearning: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  setup(props, { emit }) {
    const { $toast } = getCurrentInstance().proxy
    const items = ref([])
    const itemSelected = ref(0)

    const absentTypes = [
      {id: 1, name: 'Đúng giờ'},
      {id: 2, name: 'Nghỉ có phép'},
      {id: 3, name: 'Nghỉ không phép'},
      {id: 4, name: 'Muộn có phép'},
      {id: 5, name: 'Muộn không phép'}
    ]

    const getBodySelfLearning = () => {
      return {
        classroom: props.data.classroom,
        student: props.data.student,
        absent_type: props.data.absent_type,
        dates: [props.data.date],
        id: props.data.id
      }
    }

    const onSave = async () => {
      try {
        if (!props.isSelfLearning) await api.put(`${endpoints.ROLLCALL}`, props.data)
        else await api.put(`${endpoints.SELF_LEARNING}${props.data.id}`, getBodySelfLearning())
        emit('reload')
        emit('on-close')
        $toast.success('Save data successful')
      } catch {
        $toast.error('Delete data failed')
      }
    }

    return {
      onSave,
      items,
      itemSelected,
      absentTypes
    }
  }
})

export default EditRollCallDialog
</script>
