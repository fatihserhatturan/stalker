<template>
  <div
    :class="[
      'relative max-w-2xl rounded-2xl px-4 py-3 shadow-lg transition-all duration-200 hover:border-blue-400',
      bubbleClasses
    ]"
  >
    <p
      :class="[
        'text-sm leading-relaxed whitespace-pre-wrap',
        textClasses
      ]"
    >
      {{ message.text }}
    </p>

    <div
      :class="[
        'absolute top-4 w-2 h-2 transform rotate-45',
        tailClasses
      ]"
    ></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  message: {
    type: Object,
    required: true
  },
  isUser: Boolean
})

const bubbleClasses = computed(() => {
  return props.isUser
    ? 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white border border-transparent hover:border-emerald-300'
    : 'bg-gray-800 border border-gray-700/50 text-gray-100'
})

const textClasses = computed(() => {
  return props.isUser ? 'text-white' : 'text-gray-100'
})

const tailClasses = computed(() => {
  return props.isUser
    ? '-right-1 bg-gradient-to-r from-emerald-600 to-teal-700'
    : '-left-1 bg-gray-800 border-l border-b border-gray-700/50'
})
</script>
