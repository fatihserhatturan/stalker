<template>
  <div class="flex items-center space-x-3">
    <div class="p-2 bg-gradient-to-r from-purple-600 to-pink-700 rounded-lg group-hover:scale-110 transition-transform duration-200">
      <ChartBarIcon class="w-5 h-5 text-white" />
    </div>
    <div class="text-left">
      <h3 class="text-white font-medium">Görsel Öğeler ve Analizler</h3>
      <p class="text-gray-400 text-sm">{{ description }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ChartBarIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  hasDynamicData: Boolean
})

const description = computed(() => {
  return props.hasDynamicData
    ? 'Dinamik verilerle oluşturulmuş grafikler ve şemalar'
    : 'Grafikler, şemalar ve analiz görselleri'
})
</script>
