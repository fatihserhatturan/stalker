<template>
  <div class="px-6 py-4">
    <div class="max-w-4xl mx-auto">
      <div class="flex items-center justify-center mb-4">
        <button
          @click="$emit('generate')"
          :disabled="isGenerating || !isConnected || isLoading"
          class="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-emerald-600 to-teal-700 hover:border-emerald-400 text-white rounded-xl transition-all duration-200 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed border border-transparent"
        >
          <DocumentTextIcon class="w-5 h-5" />
          <span>{{ isGenerating ? 'Doküman Oluşturuluyor...' : 'Analiz Dokümanı Oluştur' }}</span>
        </button>
      </div>

      <div class="text-center">
        <p class="text-xs text-gray-400">
          {{ description }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { DocumentTextIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  isGenerating: Boolean,
  isConnected: Boolean,
  isLoading: Boolean,
  templateFile: Object,
  isImageGenerationEnabled: Boolean
})

defineEmits(['generate'])

const description = computed(() => {
  let text = props.templateFile
    ? `Template "${props.templateFile.name}" kullanılarak doküman oluşturulacak`
    : 'Sohbet geçmişinize dayanarak detaylı bir ön analiz dokümanı oluşturulacak'

  text += props.isImageGenerationEnabled ? ' (Görsel analiz dahil)' : ' (Sadece metin dokümanı)'

  return text
})
</script>
