<template lang="pug">
  v-bottom-sheet(
    v-model="value"
    persistent
  )
    div.ma-0.pa-0
      v-row.ma-0.py-0.px-1(align='center' justify='center')
        v-btn.mb-1.rounded-lg(
          block
          height="50"
          elevation="0"
          color="white"
          @click="$emit('on-edit')"
        )
          span Sửa
      v-row.ma-0.py-0.px-1(align='center' justify='center')
        v-btn.mb-1.rounded-lg(
          block
          height="50"
          elevation="0"
          color="white"
          @click="$emit('on-delete')"
        )
          span Xóa
      v-row.ma-0.py-0.px-1(align='center' justify='center')
        v-btn.mb-1.rounded-lg(
          block
          height="50"
          elevation="0"
          color="white"
          @click="$emit('on-close')"
        )
          span Thoát
</template>

<script>
import { defineComponent } from 'vue'

const BottomSheet = defineComponent({
  props: {
    value: { type: Boolean }
  },
  setup() {
    return {}
  }
})

export default BottomSheet
</script>