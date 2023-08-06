<template>
  <UFormWrapper :is-loading="isLoading" addDefaultClasses>
    <template #header>
      <h2 class="text-[1.25rem] font-medium text-grey-1000">Mission Details</h2>
    </template>
    <template #content>
      <UInputWrapper
          v-model="formModel.mission_number"
          required
          :is-validation-dirty="validationInfo?.$dirty"
          :errors="validationInfo?.mission_number.$errors"
          label-text="Mission Number"
      />
      <USelectWrapper
          v-model="formModel.type"
          required
          :is-validation-dirty="validationInfo?.$dirty"
          label-text="Mission Type"
          :errors="validationInfo?.type.$errors"
          label="name"
          :reduce="(item) => item.id"
          :options="requestTypes"
          :loading="isLoadingRequestTypes"
      />
      <USelectWrapper
          v-model="formModel.organisation"
          required
          label-text="Organisation"
          :errors="validationInfo?.organisation.$errors"
          :is-validation-dirty="validationInfo?.$dirty"
          label="full_repr"
          :reduce="(item) => item.id"
          :options="organisations"
          :loading="isLoadingOrganisations"
      />
      <UInputWrapper v-model="formModel.callsign" label-text="Callsign"/>
      <UInputWrapper v-if="0" label-text="Unit"/>
      <USelectWrapper
          v-model="formModel.requesting_person"
          :loading="isLoadingOrganisationPeople"
          :errors="validationInfo?.requesting_person.$errors"
          :options="organisationPeople"
          :reduce="(item) => item.id"
          required
          :is-validation-dirty="validationInfo?.$dirty"
          label="job_title"
          label-text="Primary Mission Contact"
      />
      <USelectWrapper
          v-model="formModel.aircraft_type"
          :loading="isLoadingAircraftTypes"
          required
          :is-validation-dirty="validationInfo?.$dirty"
          :errors="validationInfo?.aircraft_type.$errors"
          :options="aircraftTypes"
          :reduce="(item) => item?.id"
          :get-option-label="(item) => item?.type?.model"
          label="type.model"
          label-text="Aircraft Type"
      />
      <USelectWrapper
          v-model="formModel.aircraft"
          :is-validation-dirty="validationInfo?.$dirty"
          :loading="isLoadingAircraftTypes"
          :errors="validationInfo?.aircraft.$errors"
          :options="aircraftTypes"
          :reduce="(item) => item?.id"
          required
          :get-option-label="(item) => item?.registration"
          label="type.model"
          label-text="Tail Number"
      />
      <UInputWrapper v-model="formModel.apacs_number" label-text="APACS Number"/>
      <UInputWrapper
          v-model="formModel.apacs_url"
          :is-validation-dirty="validationInfo?.$dirty"
          :errors="validationInfo?.apacs_url.$errors"
          label-text="APACS URL"
      />
    </template>
  </UFormWrapper>
</template>

<script lang="ts" setup>
import {onBeforeMount, PropType, watch} from 'vue'
import UFormWrapper from '@/components/ui/wrappers/UFormWrapper.vue'
import UInputWrapper from '@/components/ui/wrappers/UInputWrapper.vue'
import USelectWrapper from '@/components/ui/wrappers/USelectWrapper.vue'
import {useFetch} from '@/composables/useFetch'
import {ITypeReference} from '@/types/general.types'
import {IPerson} from '@/types/mission/mission-reference.types'
import {IAircraft} from '@/types/mission/aircraft.types'
import MissionReferences from '@/services/mission/mission-references'
import {useMissionFormStore} from '@/stores/useMissionFormStore'
import {storeToRefs} from 'pinia'
import {BaseValidation} from '@vuelidate/core'

defineProps({
  validationInfo: {
    type: Object as PropType<BaseValidation>,
    default: () => {
    }
  },
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  }
})

const missionFormStore = useMissionFormStore()

const {formModel} = storeToRefs(missionFormStore)

const {
  loading: isLoadingRequestTypes,
  data: requestTypes,
  callFetch: fetchRequestTypes
} = useFetch<ITypeReference>(async () => {
  return await MissionReferences.fetchHandlingRequestTypes()
})
const {
  loading: isLoadingOrganisationPeople,
  data: organisationPeople,
  callFetch: fetchOrganisationPeople
} = useFetch<IPerson[]>(async (id: number) => {
  return await MissionReferences.fetchOrganisationPeople(id as number)
})
const {
  loading: isLoadingAircraftTypes,
  data: aircraftTypes,
  callFetch: fetchAircraftTypes
} = useFetch<IAircraft[]>(async (id: number) => {
  return await MissionReferences.fetchAircraftTypes(id as number)
})
const {
  loading: isLoadingOrganisations,
  data: organisations,
  callFetch: fetchOrganisations
} = useFetch<IAircraft[]>(async () => {
  return await MissionReferences.fetchOrganisations()
})

watch(
    () => formModel.value?.organisation,
    async (organisationId: number, oldId) => {
      if (oldId) {
        formModel.value.aircraft = null
        formModel.value.aircraft_type = null
        formModel.value.requesting_person = null
      }
      if (organisationId) {
        return await Promise.allSettled([
          fetchOrganisationPeople(organisationId as any),
          fetchAircraftTypes(organisationId as any)
        ])
      }
    },
    {immediate: true}
)

onBeforeMount(async () => {
  await Promise.allSettled([fetchRequestTypes(), fetchOrganisations()])
})
</script>
