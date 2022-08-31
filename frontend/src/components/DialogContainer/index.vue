<template lang="pug">
  v-dialog(
    persistent
    scrollable
    content-class="'align-bottom'"
    :value="value"
    :width="width ? width : ''"
    :max-width="width ? '': '500'"
    @input="dialog => $emit('input', dialog)"
  )
    v-card(:height="height" )
      v-card-title.text-h5.title-color
        v-btn(v-if="isBack" icon dark @click="close()")
          v-icon mdi-keyboard-backspace
        span.white--text {{label}}
        v-spacer
        v-btn(icon dark @click="close()")
          v-icon mdi-close

      v-card-text.relative-card
        slot

      v-card-actions
        v-btn.relative-btn(
          v-if="mode === 'create'"
          ref="save_btn"
          :large="!$vuetify.breakpoint.xsOnly"
          color="green"
          :loading="loading"
          @click="create()"
          style="background-color: #FBB232; color: white"
        )
          | Save
        v-btn.relative-btn-2(
          v-if="mode !== 'create'"
          ref="save_btn"
          :large="!$vuetify.breakpoint.xsOnly"
          color="green"
          :loading="loading"
          @click="remove()"
          style="background-color: red; color: white"
        )
          | Delete
        v-btn.relative-btn-2(
          v-if="mode !== 'create'"
          ref="save_btn"
          :large="!$vuetify.breakpoint.xsOnly"
          color="green"
          :loading="loading"
          @click="update()"
          style="background-color: #FBB232; color: white"
        )
          | Save

</template>

<script>
import {defineComponent} from 'vue'

const JDialogContainer = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    mode: {
      type: String,
      default: null
    },
    label: {
      type: String,
      default: ''
    },
    loading: {
      type: Boolean,
      default: false
    },
    isBack: {
      type: Boolean,
      required: false,
      default: false
    },
    isConfirm: {
      type: Boolean,
      default: false,
      required: false
    },
    height: {
      type: String,
      default: '85vh'
    },
    width: {
      type: Number,
      required: false
    }
  },
  setup(props, {emit}) {
    const close = () => {
      emit('on-close')
    }

    const remove = () => {
      emit('on-remove')
    }

    const create = () => {
      emit('on-create')
    }

    const update = () => {
      emit('on-update')
    }

    return {
      close,
      create,
      update,
      remove
    }
  }
})

export default JDialogContainer
</script>

<style lang="sass">
.title-color
  background-color: #FBB232
  span
    color: white
.relative-btn
  width: 100%
.relative-btn-2
  width: 50%
</style>

