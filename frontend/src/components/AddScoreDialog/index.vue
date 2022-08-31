<template lang="pug">
  v-dialog(
    persistent
    scrollable
    max-width="400px"
    content-class="'align-bottom'"
    :value="value"
  )
    v-card
      v-card-title.text-h5.title-color
        span.white--text Điểm
        v-spacer
        v-btn(icon dark @click="$emit('on-close')")
          v-icon mdi-close

      v-card-text.relative-card
        v-text-field(v-model="homeWork.score")
        v-checkbox(
          readonly
          :label="Number(homeWork.score) >= 8 ? 'Đạt' : 'Chưa đạt'"
          :value="Number(homeWork.score) >= 8"
          color="blue"
        )

      v-card-actions
        v-spacer
        v-btn.relative(
          :large="!$vuetify.breakpoint.xsOnly"
          color="green"
          @click="onSave()"
          style="background-color: #FBB232; color: white"
        ) Save
</template>

<script>
import { defineComponent, ref, getCurrentInstance } from "vue";
import {api} from "@/plugins";
import {endpoints} from "@/utils";

const AddScoreDialog = defineComponent({
  props: {
    value: { type: Boolean, default: false },
    homeWork: { type: Object, default: null }
  },
  setup(props, { emit }) {
    const score = ref(0)
    const { $toast } = getCurrentInstance().proxy
    const onSave = async () => {
      try {
        await api.put(`${endpoints.HOME_WORK_FILE_RESULT}score`, { id: props.homeWork.id, score: Number(props.homeWork.score) })
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }
    return { score, onSave }
  }
})

export default AddScoreDialog
</script>