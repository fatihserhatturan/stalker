<template>
  <div class="relative bg-gray-900/80 backdrop-blur-md border-b border-gray-700/50 shadow-lg">
    <div class="max-w-4xl mx-auto px-6 py-4 h-[80px]">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl shadow-lg overflow-hidden bg-white/10 backdrop-blur-sm">
            <img src="@/assets/logo.png" alt="AI Logo" class="w-full h-full object-contain p-1" />
          </div>
          <div>
            <h1 class="text-xl font-semibold text-white">AI Business Analyst</h1>
          </div>
        </div>

        <div class="flex items-center space-x-3">
          <button
            @click="$emit('toggle-image-generation')"
            :disabled="isLoading || !isConnected"
            :class="[
              'flex items-center space-x-1 px-3 py-2 border rounded-lg transition-colors text-sm disabled:opacity-50 disabled:cursor-not-allowed',
              isImageGenerationEnabled
                ? 'bg-purple-600 border-purple-500 text-white'
                : 'bg-gray-700 border-gray-600 hover:border-purple-400 text-white'
            ]"
            title="Görüntü Üretimi Aktif/Pasif"
          >
            <ChartBarIcon class="w-4 h-4" />
            <span>{{ isImageGenerationEnabled ? 'Görüntü Aktif' : 'Görüntü Pasif' }}</span>
          </button>

          <button
            @click="$emit('toggle-template-upload')"
            :disabled="isLoading || !isConnected"
            class="flex items-center space-x-1 px-3 py-2 bg-gray-700 border border-gray-600 hover:border-orange-400 text-white rounded-lg transition-colors text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            title="Doküman Template Yükle"
          >
            <DocumentIcon class="w-4 h-4" />
            <span>Template</span>
            <div v-if="hasTemplate" class="w-2 h-2 bg-orange-400 rounded-full"></div>
          </button>

          <ProgressIndicator
            v-if="showProgress"
            :completion-rate="completionRate"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { DocumentIcon, ChartBarIcon } from '@heroicons/vue/24/outline'
import ProgressIndicator from './ProgressIndicator.vue'

defineProps({
  isLoading: Boolean,
  isConnected: Boolean,
  isImageGenerationEnabled: Boolean,
  hasTemplate: Boolean,
  showProgress: Boolean,
  completionRate: Number,
})

defineEmits([
  'toggle-image-generation',
  'toggle-template-upload'
])
</script>
