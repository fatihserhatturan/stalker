<template>
  <div class="flex items-center justify-between mb-6">
    <div class="flex items-center space-x-3">
      <div class="p-2 bg-gradient-to-r from-purple-600 to-pink-700 rounded-lg">
        <ChartBarIcon class="w-5 h-5 text-white" />
      </div>
      <div>
        <h3 class="text-lg font-semibold text-white">Görsel Analiz Araçları</h3>
        <p class="text-xs text-gray-400 mt-1">
          {{ description }}
        </p>
      </div>
    </div>
    <div v-if="hasDynamicData" class="px-3 py-1 bg-emerald-600/20 text-emerald-400 rounded-full text-xs font-medium">
      Dinamik Veri
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ChartBarIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  hasDynamicData: Boolean,
  visualCount: Number
})

const description = computed(() => {
  return props.hasDynamicData
    ? 'Konuşma verilerinize dayalı dinamik analizler'
    : 'Örnek analizler ve şemalar'
})
</script>
