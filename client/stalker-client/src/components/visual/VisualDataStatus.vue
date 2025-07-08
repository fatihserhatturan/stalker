<template>
  <div class="mt-4 p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
    <div class="flex items-center space-x-2">
      <ExclamationTriangleIcon class="w-4 h-4 text-yellow-400" />
      <span class="text-xs text-yellow-400">
        Şu anda örnek verilerle gösterim yapılıyor. Dinamik veriler için analiz dokümanı oluşturun.
      </span>
    </div>
  </div>
</template>

<script setup>
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'
</script>
