<template lang="pug">
  dialog-container(
    :label="'Unit'"
    :mode="isAdd ? 'create' : 'update'"
    :height="'40%'"
    @on-close="$emit('on-close')"
    @on-update="update"
    @on-create="create"
    @on-remove="remove"
    v-model="value"
  )
    v-text-field(
      v-model="unitData.title"
      :label="'Unit'"
    )

</template>

<script>
import { defineComponent, getCurrentInstance, watch, ref } from 'vue'
import { api } from '@/plugins'
import { endpoints } from '@/utils'
import DialogContainer from "@/components/DialogContainer";

const UnitDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    classroom: {
      type: Object,
      required: true
    },
    unit: {
      type: Object,
      required: true
    },
    isAdd: {
      type: Boolean,
      default: true
    }
  },
  components: { DialogContainer },
  setup(props, { emit }) {
    const { $toast } = getCurrentInstance().proxy
    const unitData = ref({})

    const getBody = () => {
      return {
        classroom: props.classroom.id,
        title: unitData.value.title
      }
    }

    const update = async () => {
      const body = getBody()
      try {
        await api.put(`${endpoints.UNIT}${unitData.value.id}`, body)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const create = async () => {
      const body = getBody()
      try {
        await api.post(`${endpoints.UNIT}`, body)
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const remove = async () => {
      try {
        await api.delete(`${endpoints.UNIT}${unitData.value.id}`)
        emit('re-load')
        emit('on-close')
      } catch (e) {
        $toast.error('Delete data failed')
      }
    }

    const init = () => {
      if (props.value) {
        if (props.isAdd) {
          unitData.value = { id: null, title: null }
        }
        else unitData.value = JSON.parse(JSON.stringify(props.unit))
      }
    }

    watch(
      () => props.value,
      () => init()
    )

    return {
      create,
      update,
      remove,
      unitData
    }
  }
})

export default UnitDialog
</script>
