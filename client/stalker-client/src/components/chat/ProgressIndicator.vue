<template>
  <div class="flex items-center space-x-2 px-3 py-2 bg-gray-800/60 rounded-lg border border-gray-700/30">
    <div
      class="w-2 h-2 rounded-full"
      :class="statusColor"
    ></div>
    <span class="text-xs text-gray-300">{{ completionRate }}%</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  completionRate: {
    type: Number,
    default: 0
  }
})

const statusColor = computed(() => {
  if (props.completionRate < 30) return 'bg-red-400'
  if (props.completionRate < 70) return 'bg-yellow-400'
  return 'bg-green-400'
})
</script>
