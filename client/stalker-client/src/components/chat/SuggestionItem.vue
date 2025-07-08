<template>
  <button
    @click="$emit('click')"
    class="max-w-2xl text-left p-3 bg-gradient-to-r from-blue-600/20 to-purple-700/20 border border-blue-500/30 rounded-xl hover:border-blue-400 transition-all duration-200 group suggestion-item"
    :style="{ animationDelay: `${delay}ms` }"
  >
    <div class="flex items-start space-x-3">
      <div class="flex-shrink-0 mt-1">
        <div class="w-6 h-6 rounded-full bg-blue-600/30 flex items-center justify-center group-hover:bg-blue-600/50 transition-colors">
          <LightBulbIcon class="w-3 h-3 text-blue-300" />
        </div>
      </div>
      <p class="text-sm text-blue-100 group-hover:text-white transition-colors">
        {{ suggestion }}
      </p>
    </div>
  </button>
</template>

<script setup>
import { LightBulbIcon } from '@heroicons/vue/24/outline'

defineProps({
  suggestion: {
    type: String,
    required: true
  },
  delay: {
    type: Number,
    default: 0
  }
})

defineEmits(['click'])
</script>

<style scoped>
.suggestion-item {
  animation: slideInFromRight 0.4s ease-out both;
}

@keyframes slideInFromRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
