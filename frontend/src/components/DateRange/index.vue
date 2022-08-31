<template lang="pug">
  v-row.ma-0.pa-0.px-0(justify="space-around")
    v-col.pr-0.pl-2.pb-2
      v-dialog(
        ref="startDialog"
        persistent
        width="90vw"
        max-width="500px"
        :return-value.sync="startDate"
        v-model="dateStartModal"
      )
        template(v-slot:activator="{ on, attrs }")
          v-text-field(
            readonly
            hide-details
            v-bind="attrs"
            v-on="on"
            append-icon="mdi-calendar-range"
            label="Từ ngày"
            :value="startDate"
            @click:append-outer="dateStartModal = true"
          )
        v-date-picker.title-color(
          color="rough_black"
          header-color="rough_black"
          v-model="startDate"
          @input="updateDateStart"
          full-width
        )
          v-spacer
          v-btn.white--text(dark text color="light_red" @click="dateStartModal = false")
            span cancel
          v-btn.white--text(dark text color="rough_black" @click="$refs.startDialog.save(startDate), goToDate(), dateStartModal = false")
            span ok
    v-col.px-0(cols="1" align-self="end" align-content="center")
      div(style="text-align:center")
        span &#10132;
    v-col.pl-0.pr-1.pb-2
      v-dialog(
        ref="endDialog"
        persistent
        width="90vw"
        max-width="500px"
        :return-value.sync="endDate"
        v-model="dateEndModal"
      )
        template(v-slot:activator="{ on, attrs }")
          v-text-field(
            readonly
            hide-details
            v-bind="attrs"
            v-on="on"
            append-icon="mdi-calendar-range"
            label="Đến ngày"
            :value="endDate"
            @click:append-outer="dateEndModal = true"
          )
        v-date-picker.title-color(
          color="rough_black"
          header-color="rough_black"
          v-model="endDate"
          :min="startDate"
          full-width
        )
          v-spacer
          v-btn.white--text(dark text color="light_red" @click="dateEndModal = false")
            span cancel
          v-btn.white--text(dark text color="rough_black" @click="$refs.endDialog.save(endDate), goToDate()")
            span ok
</template>

<script>
import { defineComponent, ref, watch } from 'vue'

const DateRange = defineComponent({
  props: {
    dateStart: {
      type: String,
      required: true
    },
    dateEnd: {
      type: String,
      required: true
    },
    goToDate: {
      type: Function,
      required: false
    }
  },
  setup(props, { emit }) {
    const dateStartModal = ref(false)
    const dateEndModal = ref(false)
    const startDate = ref(props.dateStart)
    const endDate = ref(props.dateEnd)

    if (props.dateStart === props.dateEnd) {
      startDate.value = props.dateStart
      endDate.value = props.dateStart
    } else {
      startDate.value = props.dateStart
      endDate.value = props.dateEnd
    }

    const updateDateStart = () => {
      if (props.dateStart > props.dateEnd) {
        endDate.value = startDate.value
      }
    }

    watch(
      () => props.dateStart,
      () => {
        startDate.value = props.dateStart
      }
    )

    watch(
      () => props.dateEnd,
      () => {
        endDate.value = props.dateEnd
      }
    )

    watch(
      () => startDate.value,
      () => {
        emit('on-change-date', startDate.value, endDate.value)
      }
    )

    watch(
      () => endDate.value,
      () => {
        emit('on-change-date', startDate.value, endDate.value)
      }
    )

    return {
      dateStartModal,
      dateEndModal,
      updateDateStart,
      startDate,
      endDate
    }
  }
})
export default DateRange
</script>
<style lang="sass" scoped>
::v-deep .v-date-picker-title__date
  font-size: 28px
.title-color
  background-color: #FBB232 !important
::v-deep .v-date-picker-table .v-btn.v-btn--active
  background-color: #FBB232 !important
</style>
