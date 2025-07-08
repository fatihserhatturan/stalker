<template>
  <button
    @click="$emit('click')"
    :disabled="disabled"
    class="flex items-center space-x-2 w-full px-4 py-2 text-left text-sm text-gray-300 border border-transparent hover:border-gray-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
  >
    <component :is="iconComponent" class="w-4 h-4" />
    <span>{{ displayText }}</span>
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { DocumentIcon, DocumentTextIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  disabled: Boolean,
  loading: Boolean,
  icon: {
    type: String,
    required: true,
    validator: (value) => ['DocumentIcon', 'DocumentTextIcon'].includes(value)
  },
  text: {
    type: String,
    required: true
  },
  loadingText: {
    type: String,
    required: true
  }
})

defineEmits(['click'])

const iconComponent = computed(() => {
  const iconMap = {
    DocumentIcon,
    DocumentTextIcon
  }
  return iconMap[props.icon]
})

const displayText = computed(() => {
  return props.loading ? props.loadingText : props.text
})
</script>
