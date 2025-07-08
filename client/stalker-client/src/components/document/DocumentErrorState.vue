<template>
  <div class="flex items-center justify-center h-full">
    <div class="text-center">
      <ExclamationTriangleIcon class="w-12 h-12 text-red-500 mx-auto mb-4" />
      <h3 class="text-lg font-semibold text-white mb-2">Hata Oluştu</h3>
      <p class="text-gray-400 text-sm">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

defineProps({
  error: {
    type: String,
    required: true
  }
})
</script>
