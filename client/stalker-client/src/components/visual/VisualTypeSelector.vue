<template>
  <div class="flex flex-wrap gap-3 mb-6">
    <button
      v-for="visual in visualTypes"
      :key="visual.id"
      @click="$emit('visual-selected', visual.id)"
      :class="[
        'flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 border',
        selectedVisual === visual.id
          ? 'bg-purple-600 border-purple-500 text-white'
          : 'bg-gray-700 border-gray-600 text-gray-300 hover:border-purple-500 hover:text-white'
      ]"
    >
      <component :is="visual.icon" class="w-4 h-4" />
      <span class="text-sm">{{ visual.name }}</span>
    </button>
  </div>
</template>

<script setup>
defineProps({
  visualTypes: {
    type: Array,
    required: true
  },
  selectedVisual: {
    type: String,
    required: true
  }
})

defineEmits(['visual-selected'])
</script>
