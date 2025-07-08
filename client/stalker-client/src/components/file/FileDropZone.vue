<template>
  <div
    @drop="handleDrop"
    @dragover.prevent
    @dragenter="handleDragEnter"
    @dragleave="handleDragLeave"
    class="border-2 border-dashed rounded-lg p-6 text-center transition-all duration-200 cursor-pointer"
    :class="dropZoneClasses"
  >
    <input
      ref="fileInput"
      type="file"
      :accept="accept"
      @change="handleFileSelect"
      class="hidden"
    />

    <div class="space-y-2">
      <component :is="icon" class="w-8 h-8 text-gray-400 mx-auto" />
      <p class="text-sm text-gray-300">
        <button
          @click="fileInput?.click()"
          :class="buttonClasses"
        >
          {{ message }}
        </button>
      </p>
      <p class="text-xs text-gray-500">{{ help }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ArrowUpTrayIcon, DocumentIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  accept: {
    type: String,
    default: '*'
  },
  isDropping: Boolean,
  message: {
    type: String,
    default: 'Dosya seç veya buraya sürükle'
  },
  help: {
    type: String,
    default: 'Desteklenen formatlar'
  },
  color: {
    type: String,
    default: 'purple',
    validator: (value) => ['purple', 'orange'].includes(value)
  }
})

const emit = defineEmits(['files-dropped', 'file-selected'])

const fileInput = ref(null)
const isDragging = ref(false)

const icon = computed(() => {
  return props.color === 'orange' ? DocumentIcon : ArrowUpTrayIcon
})

const dropZoneClasses = computed(() => {
  const baseClasses = 'border-gray-600'
  const hoverClasses = props.color === 'orange'
    ? 'hover:border-orange-500'
    : 'hover:border-purple-500'
  const activeClasses = props.color === 'orange'
    ? 'border-orange-500 bg-orange-500/10'
    : 'border-purple-500 bg-purple-500/10'

  return [
    baseClasses,
    hoverClasses,
    isDragging.value ? activeClasses : ''
  ].filter(Boolean).join(' ')
})

const buttonClasses = computed(() => {
  return props.color === 'orange'
    ? 'text-orange-400 hover:text-orange-300 hover:border-b hover:border-orange-300 transition-all duration-200'
    : 'text-purple-400 hover:text-purple-300 hover:border-b hover:border-purple-300 transition-all duration-200'
})

const handleDrop = (event) => {
  event.preventDefault()
  isDragging.value = false

  const files = Array.from(event.dataTransfer.files)
  emit('files-dropped', files)
}

const handleDragEnter = (event) => {
  event.preventDefault()
  isDragging.value = true
}

const handleDragLeave = (event) => {
  event.preventDefault()
  if (!event.currentTarget.contains(event.relatedTarget)) {
    isDragging.value = false
  }
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    emit('file-selected', file)
  }
  event.target.value = ''
}
</script>
