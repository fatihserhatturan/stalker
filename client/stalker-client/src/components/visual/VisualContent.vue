<template>
  <div>
    <OrganizationChart
      v-if="selectedVisual === 'orgChart'"
      :data="dynamicOrgData"
      @chart-ready="setChartRef('orgChartContainer', $event)"
    />

    <WorkflowChart
      v-if="selectedVisual === 'workflow'"
      :data="dynamicWorkflowData"
      @chart-ready="setChartRef('workflowContainer', $event)"
    />

    <TimelineChart
      v-if="selectedVisual === 'timeline'"
      :data="dynamicTimelineData"
      @chart-ready="setChartRef('timelineChart', $event)"
    />

    <RiskChart
      v-if="selectedVisual === 'riskAnalysis'"
      :data="dynamicRiskData"
      @chart-ready="setChartRef('riskChart', $event)"
    />

    <ResourceChart
      v-if="selectedVisual === 'resources'"
      :data="dynamicResourceData"
      @chart-ready="setChartRef('resourceChart', $event)"
    />

    <CostChart
      v-if="selectedVisual === 'cost'"
      :data="dynamicCostData"
      @chart-ready="setChartRef('costChart', $event)"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import OrganizationChart from './charts/OrganizationChart.vue'
import WorkflowChart from './charts/WorkflowChart.vue'
import TimelineChart from './charts/TimelineChart.vue'
import RiskChart from './charts/RiskChart.vue'
import ResourceChart from './charts/ResourceChart.vue'
import CostChart from './charts/CostChart.vue'

const props = defineProps({
  selectedVisual: String,
  visualData: Object,
  chartRefs: Object
})

const emit = defineEmits(['charts-ready'])

const dynamicOrgData = computed(() => {
  return props.visualData?.orgChart || null
})

const dynamicWorkflowData = computed(() => {
  return props.visualData?.workflow || null
})

const dynamicTimelineData = computed(() => {
  return props.visualData?.timeline || null
})

const dynamicRiskData = computed(() => {
  return props.visualData?.riskAnalysis || null
})

const dynamicResourceData = computed(() => {
  return props.visualData?.resources || null
})

const dynamicCostData = computed(() => {
  return props.visualData?.cost || null
})

const setChartRef = (refName, element) => {
  const refs = { [refName]: element }
  emit('charts-ready', refs)
}
</script>
