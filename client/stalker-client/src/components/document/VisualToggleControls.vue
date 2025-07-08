<template>
  <div class="flex items-center space-x-2">
    <div v-if="hasDynamicData" class="px-2 py-1 bg-emerald-600/20 text-emerald-400 rounded text-xs">
      Dinamik
    </div>
    <span class="text-xs text-gray-500">
      {{ isExpanded ? 'Gizle' : 'Göster' }}
    </span>
    <div
      :class="[
        'transform transition-transform duration-300',
        isExpanded ? 'rotate-180' : 'rotate-0'
      ]"
    >
      <ChevronDownIcon class="w-4 h-4 text-gray-400" />
    </div>
  </div>
</template>

<script setup>
import { ChevronDownIcon } from '@heroicons/vue/24/outline'

defineProps({
  isExpanded: Boolean,
  hasDynamicData: Boolean
})
</script>
