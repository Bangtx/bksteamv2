<template lang="pug">
  v-dialog(:value="value" max-width="600" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span Điểm danh {{ date }}
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close
      v-card-text
        v-row
          v-col(cols="12" sm="6" v-for="student in students" )
            span {{student.name}}
            v-autocomplete(
              :items="absentTypes"
              item-value="name"
              item-text="name"
              hide-details
              v-model="data[String(student.id)]"
            )

        //v-text-field(readonly :value="data.date")
      v-card-actions
        v-btn.relative-btn(
          :large="!$vuetify.breakpoint.xsOnly"
          block
          @click="onSave()"
        )
          span Lưu
</template>

<script>
import { defineComponent, watch, ref, getCurrentInstance, computed } from 'vue'
import { api } from '@/plugins'
import { endpoints } from '@/utils'
import moment from "moment/moment";

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
    },
    students: {
      default: () => []
    },
    classroom: {
      type: Object,
      required: true
    },
    teacher: {
      type: Object,
      required: true
    },
    date: {
      type: String,
      required: true
    },
    dates: {
      type: Array,
      required: true
    }
  },
  setup(props, { emit }) {
    const { $toast } = getCurrentInstance().proxy
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

    const getBody = () => {
      const result = {}
      Object.keys(props.data).forEach((key) => {
        if (props.data[key] === 'Đúng giờ') result[key] = 1
        if (props.data[key] === 'Nghỉ có phép') result[key] = 2
        if (props.data[key] === 'Nghỉ không phép') result[key] = 3
        if (props.data[key] === 'Muộn có phép') result[key] = 4
        if (props.data[key] === 'Muộn không phép') result[key] = 5
      })
      return {date: props.date, payload: result, classroom: props.classroom.id, teacher: props.teacher.id}
    }

    const onSave = async () => {
      if (props.dates.indexOf(props.date) !== -1) {
        $toast.info('Hom nay da diem danh')
        return
      }
      try {
        if (!props.isSelfLearning) await api.post(`${endpoints.ROLLCALL}`, getBody())
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
      itemSelected,
      absentTypes
    }
  }
})

export default EditRollCallDialog
</script>
