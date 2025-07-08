<template>
  <div class="flex-shrink-0">
    <div
      :class="[
        'w-10 h-10 rounded-full flex items-center justify-center shadow-lg transition-all duration-200 overflow-hidden',
        avatarClasses
      ]"
    >
      <UserIcon v-if="author === 'user'" class="w-5 h-5" />
      <img v-else src="@/assets/logo.png" alt="AI Logo" class="w-full h-full object-contain p-1" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { UserIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  author: {
    type: String,
    required: true,
    validator: (value) => ['user', 'ai'].includes(value)
  }
})

const avatarClasses = computed(() => {
  return props.author === 'ai'
    ? 'bg-white/10 backdrop-blur-sm'
    : 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white'
})
</script>
