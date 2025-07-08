<template>
  <div class="relative" ref="dropdownRef">
    <button
      @click="showMenu = !showMenu"
      class="flex items-center space-x-1 px-3 py-2 bg-gray-700 border border-gray-600 hover:border-gray-400 text-white rounded-lg transition-colors text-sm"
    >
      <ArrowDownTrayIcon class="w-4 h-4" />
      <span>İndir</span>
      <ChevronDownIcon class="w-3 h-3" />
    </button>

    <div v-show="showMenu" class="absolute right-0 mt-2 w-48 bg-gray-800 border border-gray-700 rounded-lg shadow-xl z-50">
      <div class="py-1">
        <DownloadMenuItem
          @click="handlePdfDownload"
          :disabled="isGeneratingPdf"
          :loading="isGeneratingPdf"
          icon="DocumentIcon"
          text="PDF (.pdf)"
          loading-text="PDF oluşturuluyor..."
        />

        <DownloadMenuItem
          @click="handleWordDownload"
          :disabled="isGeneratingWord"
          :loading="isGeneratingWord"
          icon="DocumentTextIcon"
          text="Word (.docx)"
          loading-text="Word oluşturuluyor..."
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ArrowDownTrayIcon, ChevronDownIcon } from '@heroicons/vue/24/outline'
import DownloadMenuItem from './DownloadMenuItem.vue'

defineProps({
  isGeneratingPdf: Boolean,
  isGeneratingWord: Boolean
})

const emit = defineEmits(['download-pdf', 'download-word'])

const showMenu = ref(false)
const dropdownRef = ref(null)

const handlePdfDownload = () => {
  emit('download-pdf')
  showMenu.value = false
}

const handleWordDownload = () => {
  emit('download-word')
  showMenu.value = false
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    showMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
