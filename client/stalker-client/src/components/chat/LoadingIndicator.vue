<template>
  <div class="flex items-start space-x-4">
    <div class="flex-shrink-0">
      <div :class="avatarClasses">
        <component :is="icon" class="w-5 h-5 text-white" />
      </div>
    </div>

    <div class="relative bg-gray-800 border border-gray-700/50 rounded-2xl px-4 py-3 shadow-lg">
      <div class="flex items-center space-x-2">
        <div v-if="color === 'blue'" class="flex space-x-1">
          <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0s;"></div>
          <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.15s;"></div>
          <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.3s;"></div>
        </div>
        <div v-else :class="spinnerClasses"></div>
        <span class="text-xs text-gray-400 ml-2">{{ message }}</span>
      </div>
      <div class="absolute top-4 -left-1 w-2 h-2 bg-gray-800 border-l border-b border-gray-700/50 transform rotate-45"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { DocumentTextIcon, ArrowUpTrayIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  message: {
    type: String,
    default: 'Yükleniyor...'
  },
  color: {
    type: String,
    default: 'blue',
    validator: (value) => ['blue', 'emerald', 'purple'].includes(value)
  }
})

const icon = computed(() => {
  const iconMap = {
    blue: 'img',
    emerald: DocumentTextIcon,
    purple: ArrowUpTrayIcon
  }
  return iconMap[props.color]
})

const avatarClasses = computed(() => {
  const baseClasses = 'w-10 h-10 rounded-full flex items-center justify-center shadow-lg overflow-hidden'

  const colorClasses = {
    blue: 'bg-white/10 backdrop-blur-sm',
    emerald: 'bg-gradient-to-r from-emerald-600 to-teal-700',
    purple: 'bg-gradient-to-r from-purple-600 to-pink-700'
  }

  return `${baseClasses} ${colorClasses[props.color]}`
})

const spinnerClasses = computed(() => {
  const colorMap = {
    emerald: 'border-emerald-400',
    purple: 'border-purple-400'
  }

  return `inline-block animate-spin rounded-full h-4 w-4 border-b-2 ${colorMap[props.color]}`
})
</script>

<style scoped>
@keyframes bounce {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

.animate-bounce {
  animation: bounce 1.4s infinite;
}
</style>
