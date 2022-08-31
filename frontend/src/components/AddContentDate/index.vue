<template lang="pug">
  dialog-container(
    :label="'Bài Giảng'"
    :mode="slide.id ? 'update' : 'create'"
    :height="'40%'"
    @on-close="$emit('on-close')"
    @on-update="update"
    @on-create="create"
    v-model="value"
  )
    v-text-field(
      v-model="slide.title"
      :label="'tiêu đè'"
    )
    v-text-field(
      v-model="slide.url"
      :label="'url'"
    )
    v-text-field(
      v-model="slide.remark"
      :label="'chú thích'"
    )

</template>

<script>
import { defineComponent, ref, getCurrentInstance } from 'vue'
import moment from 'moment'
import { endpoints } from '@/utils'
import { api } from '@/plugins'
import DialogContainer from "@/components/DialogContainer";

const AddContentDate = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    slide: {
      type: Object,
      required: true
    }
  },
  components: { DialogContainer },
  setup(props, { emit }) {
    const { $toast } = getCurrentInstance().proxy
    const modal = ref(false)
    const date = ref(moment(new Date()).format('YYYY-MM-DD'))

    const create = async () => {
      try {
        await api.post(endpoints.SLIDE, props.slide)
        emit('reload')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const update = async () => {
      try {
        await api.put(endpoints.SLIDE, props.slide)
        emit('reload')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    return {
      modal,
      date,
      create,
      update
    }
  }
})

export default AddContentDate
</script>

<style lang="sass"></style>
