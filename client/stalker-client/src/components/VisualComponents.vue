<template>
  <div class="bg-gray-800/60 rounded-xl p-6 border border-gray-700/50">
    <VisualHeader
      :has-dynamic-data="!!visualData"
      :visual-count="visualTypes.length"
    />

    <VisualTypeSelector
      :visual-types="visualTypes"
      :selected-visual="selectedVisual"
      @visual-selected="selectedVisual = $event"
    />

    <div class="bg-gray-900/50 rounded-lg p-4 min-h-[400px]">
      <VisualContent
        :selected-visual="selectedVisual"
        :visual-data="visualData"
        :chart-refs="chartRefs"
        @charts-ready="handleChartsReady"
      />
    </div>

    <VisualDataStatus v-if="!visualData" />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import {
  UserGroupIcon,
  CogIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  CpuChipIcon,
  CurrencyDollarIcon
} from '@heroicons/vue/24/outline'
import VisualHeader from './visual/VisualHeader.vue'
import VisualTypeSelector from './visual/VisualTypeSelector.vue'
import VisualContent from './visual/VisualContent.vue'
import VisualDataStatus from './visual/VisualDataStatus.vue'

defineProps({
  visualData: {
    type: Object,
    default: () => null
  }
})

const selectedVisual = ref('orgChart')

const visualTypes = [
  { id: 'orgChart', name: 'Organizasyon', icon: UserGroupIcon },
  { id: 'workflow', name: 'İş Akışı', icon: CogIcon },
  { id: 'timeline', name: 'Zaman Çizelgesi', icon: ClockIcon },
  { id: 'riskAnalysis', name: 'Risk Analizi', icon: ExclamationTriangleIcon },
  { id: 'resources', name: 'Kaynaklar', icon: CpuChipIcon },
  { id: 'cost', name: 'Maliyet', icon: CurrencyDollarIcon }
]

const chartRefs = reactive({
  timelineChart: null,
  riskChart: null,
  resourceChart: null,
  costChart: null,
  orgChartContainer: null,
  workflowContainer: null
})

const handleChartsReady = (refs) => {
  Object.assign(chartRefs, refs)
}
</script>
