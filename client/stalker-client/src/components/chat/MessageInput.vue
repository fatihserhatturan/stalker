<template>
  <div class="px-6 py-4">
    <div class="max-w-4xl mx-auto">
      <FileUpload
        v-if="showFileUpload"
        :selected-file="selectedFile"
        :is-uploading="isUploading"
        @close="$emit('toggle-file-upload')"
        @file-selected="$emit('file-selected', $event)"
        @file-removed="$emit('file-removed')"
        @upload-file="$emit('upload-file')"
      />

      <form @submit.prevent="handleSubmit" class="relative">
        <div class="relative flex items-end">
          <textarea
            v-model="messageText"
            ref="textareaRef"
            placeholder="Proje fikrinizi detaylıca anlatın..."
            :disabled="isLoading || !isConnected"
            rows="2"
            class="w-full pl-4 pr-20 py-3 bg-gray-800 border border-gray-700 rounded-xl text-sm placeholder-gray-400 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 disabled:bg-gray-900 disabled:text-gray-500 shadow-lg resize-none overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent"
            :style="textareaStyle"
            @input="adjustHeight"
            @keydown.enter.prevent="handleEnterKey"
          />

          <button
            type="button"
            @click="$emit('toggle-file-upload')"
            :disabled="isLoading || !isConnected"
            class="absolute right-12 bottom-3 p-2 text-gray-400 hover:text-purple-400 hover:border hover:border-purple-400 rounded transition-all duration-200 disabled:text-gray-600 disabled:cursor-not-allowed"
            title="Dosya Yükle"
          >
            <PaperClipIcon class="w-4 h-4" />
          </button>

          <button
            type="submit"
            :disabled="isLoading || !messageText.trim() || !isConnected"
            class="absolute right-2 bottom-3 p-2 bg-gradient-to-r from-blue-600 to-purple-700 text-white rounded-lg hover:border-blue-400 transition-all duration-200 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed border border-transparent"
          >
            <PaperAirplaneIcon class="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { PaperClipIcon, PaperAirplaneIcon } from '@heroicons/vue/24/outline'
import FileUpload from '../file/FileUpload.vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  isLoading: Boolean,
  isConnected: Boolean,
  showFileUpload: Boolean,
  selectedFile: Object,
  isUploading: Boolean
})

const emit = defineEmits([
  'update:modelValue',
  'submit',
  'toggle-file-upload',
  'file-selected',
  'file-removed',
  'upload-file'
])

const textareaRef = ref(null)

const messageText = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const textareaStyle = computed(() => ({
  maxHeight: '120px',
  minHeight: '48px'
}))

const adjustHeight = () => {
  const textarea = textareaRef.value
  if (textarea) {
    textarea.style.height = '48px'
    const scrollHeight = textarea.scrollHeight
    const minHeight = 48
    const maxHeight = 120
    const newHeight = Math.min(Math.max(scrollHeight, minHeight), maxHeight)
    textarea.style.height = newHeight + 'px'
  }
}

const handleEnterKey = (event) => {
  if (event.shiftKey) {
    return
  } else {
    event.preventDefault()
    handleSubmit()
  }
}

const handleSubmit = () => {
  if (messageText.value.trim() && !props.isLoading && props.isConnected) {
    emit('submit', messageText.value.trim())
  }
}

const focusInput = () => {
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.focus()
      adjustHeight()
    }
  })
}

watch(messageText, () => {
  nextTick(() => {
    adjustHeight()
  })
})

defineExpose({
  focusInput
})
</script>

<style scoped>
.scrollbar-thin::-webkit-scrollbar {
  width: 4px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background-color: rgb(75 85 99);
  border-radius: 2px;
}
</style>
