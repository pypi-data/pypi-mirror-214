<template>
  <div :class="[$style['mission-leg-wrapper']]">
    <div :class="[$style['mission-leg-wrapper__content']]">
      <USelectWrapper
          v-model="missionFormModel.legs[legIndex].departure_location"
          :loading="isLoadingAirportLocations"
          required
          :is-validation-dirty="isValidationDirty"
          :errors="errors?.departure_location"
          :options="airportLocations"
          :reduce="(item) => item.id"
          label="full_repr"
          label-text="Departure Airport:"
      />
      <div class="flex flex-col">
        <ULabel required label-text="Departure Date:"/>
        <UCalendar
            :min-date="computedMinimumDepartureDate"
            :errors="errors?.departure_datetime"
            :is-validation-dirty="isValidationDirty"
            required
            v-model="missionFormModel.legs[legIndex].departure_datetime"
        />
      </div>
      <USelectWrapper
          v-model="missionFormModel.legs[legIndex].arrival_location"
          :errors="errors?.arrival_location"
          :loading="isLoadingAirportLocations"
          :is-validation-dirty="isValidationDirty"
          required
          :options="airportLocations"
          :reduce="(item) => item.id"
          @update:model-value="onChangeArrivalLocation"
          label="full_repr"
          label-text="Destination Airport:"
      />

      <div class="flex flex-col">
        <ULabel required label-text="Arrival Date:"/>
        <UCalendar
            :is-validation-dirty="isValidationDirty"
            :min-date="missionFormModel.legs[legIndex].departure_datetime ?? null"
            v-model="missionFormModel.legs[legIndex].arrival_datetime"
            :errors="errors?.arrival_datetime"
        />
      </div>
      <UInputWrapper
          :errors="errors?.callsign_override"
          :is-validation-dirty="isValidationDirty"
          v-model="missionFormModel.legs[legIndex].callsign_override"
          label-text="Callsign (if different):"
      />
      <UInputWrapper
          v-model="missionFormModel.legs[legIndex].pob_crew"
          required
          type="number"
          :is-validation-dirty="isValidationDirty"
          label-text="Crew:"
          :errors="errors?.pob_crew"
      />
    </div>
  </div>
  <div class="flex mb-[18px]">
    <div class="flex px-[1.5rem] mt-[6px] gap-[1.5rem] w-full">
      <div class="flex w-1/2 flex-col">
        <div>
          <UCheckboxWrapper v-model="passengersCheckbox" label-text="Passengers?" @update:model-value="passengersCheckbox = $event"/>
            <UInputWrapper
                type="number"
                :is-validation-dirty="isValidationDirty"
                :errors="errors?.pob_pax"
                :disabled="!passengersCheckbox"
                v-model="passengersCheckboxComputed"
            />
        </div>
      </div>
      <div class="flex w-1/2 flex-col">
          <div>
            <UCheckboxWrapper v-model="cargoCheckbox" label-text="Cargo?"/>
            <UInputWrapper
                    type="number"
                    :is-validation-dirty="isValidationDirty"
                    :errors="errors?.cob_lbs"
                    :disabled="!cargoCheckbox"
                    v-model="cargoCheckboxComputed"
            />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {computed, PropType, ref} from 'vue'
import USelectWrapper from '@/components/ui/wrappers/USelectWrapper.vue'
import UCheckboxWrapper from '@/components/ui/wrappers/UCheckboxWrapper.vue'
import UInputWrapper from '@/components/ui/wrappers/UInputWrapper.vue'
import {useMissionFormStore} from '@/stores/useMissionFormStore'
import {storeToRefs} from 'pinia'
import {useMissionReferenceStore} from '@/stores/useMissionReferenceStore'
import UCalendar from '@/components/ui/form/UCalendar.vue'
import {ErrorObject} from '@vuelidate/core'
import ULabel from '@/components/ui/form/ULabel.vue'

const props = defineProps({
  legIndex: {
    type: Number,
    default: 0
  },
  isValidationDirty: {
    type: Boolean,
    default: false
  },
  errors: {
    type: Object as PropType<Record<string, ErrorObject[]>>,
    default: () => {
    }
  }
})

const missionFormStore = useMissionFormStore()
const {formModel: missionFormModel} = storeToRefs(missionFormStore)

const missionsReferenceStore = useMissionReferenceStore()
const {isLoadingAirportLocations, airportLocations} = storeToRefs(missionsReferenceStore)

const computedMinimumDepartureDate = computed(() => {
  return props.legIndex === 0
      ? null
      : missionFormModel.value?.legs?.[props.legIndex - 1].arrival_datetime
})

const passengersCheckbox = ref(false)

const passengersCheckboxComputed = computed({
  get: () => missionFormModel.value?.legs?.[props.legIndex].pob_pax,
  set: (value: number) => {
    const leg = missionFormModel.value.legs[props.legIndex]
    if (+value < 0) leg.pob_pax = 0
      leg.pob_pax = value
  }
})
const cargoCheckbox = ref(false)

const cargoCheckboxComputed = computed({
  get: () => missionFormModel.value?.legs?.[props.legIndex].cob_lbs,
  set: (value: number) => {
    const leg = missionFormModel.value.legs[props.legIndex]
    if (+value < 0) leg.cob_lbs = 0
      leg.cob_lbs = value
  }
})

const onChangeArrivalLocation = (airportId: number) => {
  const nextLeg = missionFormModel.value?.legs?.[props.legIndex + 1]
  if (nextLeg) {
    nextLeg.departure_location = airportId
  }
}
</script>

<style lang="scss" module>
.mission-leg-wrapper {
  @apply relative flex flex-col bg-white min-w-0 rounded-[0.5rem];

  &__content {
    @apply grid px-6 gap-x-[1.5rem] gap-y-[2.5px] mt-4  grid-cols-1 sm:grid-cols-2 font-medium text-[1.25rem] text-grey-900;
  }
}
</style>
