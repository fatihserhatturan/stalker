<template>
  <div class="border-b border-gray-700/50">
    <button
      @click="$emit('toggle')"
      class="w-full px-6 py-4 bg-gray-800/40 hover:bg-gray-800/60 border-b border-gray-700/30 transition-all duration-300 group"
    >
      <div class="flex items-center justify-between">
        <VisualToggleContent :has-dynamic-data="hasDynamicData" />
        <VisualToggleControls
          :is-expanded="isExpanded"
          :has-dynamic-data="hasDynamicData"
        />
      </div>
    </button>

    <div
      :class="[
        'overflow-hidden transition-all duration-500 ease-in-out',
        isExpanded ? 'max-h-[600px] opacity-100' : 'max-h-0 opacity-0'
      ]"
    >
      <div class="p-6 bg-gray-800/20">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import VisualToggleContent from './VisualToggleContent.vue'
import VisualToggleControls from './VisualToggleControls.vue'

defineProps({
  isExpanded: Boolean,
  hasDynamicData: Boolean
})

defineEmits(['toggle'])
</script>
