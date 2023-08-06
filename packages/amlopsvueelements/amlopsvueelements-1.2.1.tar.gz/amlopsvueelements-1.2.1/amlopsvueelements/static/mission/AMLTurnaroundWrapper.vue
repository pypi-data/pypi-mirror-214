<template>
  <div :class="[$style['ops-aml-turnaround-wrapper']]">
    <div :class="[$style['ops-aml-turnaround__content']]">
      <div
          class="w-fit absolute top-[19px] right-[24px]"
          @click.stop.prevent.capture="onHandleAmlServicing"
      >
        <UCheckboxWrapper :label-text="`AML Servicing at ${arrivalAirportShortName}`"
                          :model-value="isAmlServicingEnabled"/>
      </div>
      <USelectWrapper
          :disabled="isDisabledField"
          :options="FuelRequiredTypes"
          v-model="missionFormModel.legs[legIndex].servicing.fuel_required"
          label-text="Fuel required:"
      />
      <UInputWrapper
          label-text="Quantity:"
          :disabled="isDisabledField"
          type="number"
          v-model="missionFormModel.legs[legIndex].servicing.fuel_quantity"
          label="attributes.description"
      />
      <USelectWrapper
          label-text="Unit of Measure:"
          :loading="isLoadingQuantityUnits"
          :options="quantityUnits"
          :errors="errors?.servicing"
          :is-validation-dirty="isValidationDirty"
          :get-option-label="(item) => item.code"
          :reduce="(item) => item.id"
          :disabled="isDisabledField"
          v-model="missionFormModel.legs[legIndex].servicing.fuel_unit"
          position="top"
      />
        <div class="flex items-center justify-between">
            <UCheckboxWrapper
                    v-model="missionFormModel.legs[legIndex].servicing.fuel_prist_required"
                    label-text="Prist required?"
                    :disabled="isDisabledField"
            />
            <div class="flex flex-col justify-center items-center h-full">
                <div
                    v-if="missionFormModel.legs[legIndex].servicing.services.length"
                    class="flex w-full items-center pl-4 gap-4 justify-between"
                >
                    <span>Arr</span>
                    <span>Dep</span>
                </div>
            </div>
        </div>

      <div class="flex font-medium text-[1.25rem] text-grey-1000">
        <div class="flex flex-col items-center w-full">
          <div class="flex items-start w-full justify-between relative">
            <USelectWrapper
                class="max-w-[310px] w-[76%]"
                placeholder="Select service"
                taggable
                multiple
                hide-values
                :disabled="isDisabledField"
                :loading="isLoadingServices"
                :options="computedFilteredServiceOptions"
                position="top"
                v-model="missionFormModel.legs[legIndex].servicing.services"
                :get-option-id="(item) => item.id"
                :get-option-label="
                (item) => {
                  if (item?.attributes) return item?.attributes?.name
                  return serviceOptions?.find((option) => option.id === item.service)?.attributes
                    ?.name
                }
              "
                :reduce="
                (item) => {
                  if (!item?.attributes) return item
                  return { service: item?.id, on_arrival: false, on_departure: false }
                }
              "
            />
            <div v-if="missionFormModel.legs[legIndex].servicing.services.length"
                   class="pointer-events-none absolute text-base top-2.5 text-[#a2aeb8] left-4"
              >
                  Select service
              </div>
          </div>
          <div
              v-if="missionFormModel.legs[legIndex].servicing.services"
              class="flex flex-col items-start w-full justify-between"
          >
            <div
                v-for="(service, index) in missionFormModel.legs[legIndex].servicing.services"
                :key="service.id"
                class="flex items-center w-full"
            >
              <img
                  :class="[$style['ops-aml-turnaround__content__delete-icon']]"
                  @click="onRemoveService(index)"
                  :src="getImageUrl(`assets/icons/close-circle-outline.svg`)"
                  alt="disapprove"
              />

              <ULabel
                  text-class="mb-0"
                  :required="false"
                  :label-text="findServiceNameById(service.service)"
              />
              <div class="flex justify-between gap-[0.75rem] items-center">
                <UCheckboxWrapper
                    v-model="service.on_arrival"
                    :disabled="isDisabledField"
                    class="gap-0 mr-2"
                    size="24px"
                />
                <UCheckboxWrapper
                    v-model="service.on_departure"
                    :disabled="isDisabledField"
                    class="gap-0"
                    size="24px"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import {computed, PropType, watch} from 'vue'
import {getImageUrl} from '@/helpers'
import UCheckboxWrapper from '@/components/ui/wrappers/UCheckboxWrapper.vue'
import USelectWrapper from '@/components/ui/wrappers/USelectWrapper.vue'
import UInputWrapper from '@/components/ui/wrappers/UInputWrapper.vue'
import {useMissionFormStore} from '@/stores/useMissionFormStore'
import {storeToRefs} from 'pinia'
import {FuelRequiredTypes, missionLegServicingDefaults} from '@/constants/mission.constants'
import {useFetch} from '@/composables/useFetch'
import ULabel from '@/components/ui/form/ULabel.vue'
import {useMissionReferenceStore} from '@/stores/useMissionReferenceStore'
import MissionReferences from '@/services/mission/mission-references'
import {ErrorObject} from '@vuelidate/core'
import type {IService} from '@/types/mission/mission-reference.types'
import {IAirport} from '@/types/mission/airport.types'
import type {ILegService} from '@/types/mission/mission.types'

const props = defineProps({
  legSequenceId: {
    type: Number,
    default: 0
  },
  legIndex: {
    type: Number,
    default: 0
  },
  errors: {
    type: Object as PropType<Record<string, ErrorObject[]>>,
    default: () => {
    }
  },
  isValidationDirty: {
    type: Boolean,
    default: false
  }
})

const missionFormStore = useMissionFormStore()
const missionReferenceStore = useMissionReferenceStore()
const {isLoadingQuantityUnits, quantityUnits} = storeToRefs(missionReferenceStore)
const {formModel: missionFormModel} = storeToRefs(missionFormStore)
const missionsReferenceStore = useMissionReferenceStore()
const {airportLocations} = storeToRefs(missionsReferenceStore)

const {
  loading: isLoadingServices,
  data: serviceOptions,
  callFetch: fetchServices
} = useFetch<IService[], (locationId: number) => void>(async (locationId: number) => {
  const {data} = await MissionReferences.fetchServices(locationId)
  return data
})

const computedFilteredServiceOptions = computed(() =>
    serviceOptions.value?.filter((option: IService) => {
      return !(computedLegInfo.value?.servicing?.services as ILegService[])?.some(
          (service) => service?.service === option.id
      )
    })
)

const computedLegInfo = computed(() => missionFormModel.value?.legs?.[props.legIndex])

const isAmlServicingEnabled = computed<boolean>(
    () => computedLegInfo.value.arrival_location && computedLegInfo.value.arrival_aml_service
)

const onHandleAmlServicing = () => {
  isAmlServicingEnabled.value ? onCancelServicing() : onToggleAmlServicing(true)
}
const arrivalAirportShortName = computed(() => {
  return (
      (airportLocations.value &&
          airportLocations.value?.find((airport: IAirport) => {
            return airport.id === computedLegInfo.value.arrival_location ? airport : ''
          })?.tiny_repr) ||
      ''
  )
})

const isDisabledField = computed(() => {
  return !isAmlServicingEnabled.value || !computedLegInfo.value?.arrival_location
})

const onToggleAmlServicing = (flag: boolean) => {
  missionFormModel.value.legs[props.legIndex].arrival_aml_service = flag
  if (!flag) {
    missionFormModel.value.legs[props.legIndex].servicing = missionLegServicingDefaults()
  }
}
const onCancelServicing = async () => {
  const {isConfirmed} = await window.Swal({
    title: 'Confirmation',
    text: `Please confirm that you wish cancel the servicing & fueling arrangements at $icao_x for legs ${
        props.legIndex
    } & ${props.legIndex + 1}`,
    icon: 'info',
    showCancelButton: true
  })
  if (isConfirmed) {
    onToggleAmlServicing(false)
  }
}

const onRemoveService = (serviceIndex: number) => {
  missionFormModel.value.legs[props.legIndex].servicing.services.splice(serviceIndex, 1)
}

const findServiceNameById = (id: string): string => {
  const res = (serviceOptions.value as IService[])?.find((option: IService) => option.id === id)
  return res?.attributes?.name || 'Unknown'
}

watch(
    () => computedLegInfo.value?.arrival_location,
    async (locationId: number) => {
      if (!locationId)
        return (missionFormModel.value.legs[props.legIndex].servicing = missionLegServicingDefaults())
      await fetchServices(locationId as any)
    }
)
</script>
<style lang="scss" module>
.ops-aml-turnaround {
  &-wrapper {
    @apply flex rounded-[0.5rem] flex-col bg-white min-w-0;
  }

  &__content {
    @apply font-medium text-[1.25rem] h-auto  py-[1.25rem] pb-[1.375rem] text-grey-1000;
    &__delete-icon {
      @apply w-[18px] mr-2 cursor-pointer aspect-square;
      filter: invert(23%) sepia(85%) saturate(2552%) hue-rotate(330deg) brightness(87%) contrast(103%);
    }
  }
}
</style>
