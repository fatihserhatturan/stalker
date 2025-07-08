<template>
  <div class="text-center py-4">
    <div class="inline-flex items-center px-4 py-2 bg-red-600/20 text-red-400 rounded-lg text-sm">
      <ExclamationTriangleIcon class="w-4 h-4 mr-2" />
      Backend'e bağlantı kurulamıyor. Lütfen sunucunun çalıştığından emin olun.
    </div>
  </div>
</template>

<script setup>
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'
</script>
