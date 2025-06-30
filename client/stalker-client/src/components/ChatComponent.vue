<template>
  <div class="flex flex-col h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <!-- Header -->
    <div class="relative bg-gray-900/80 backdrop-blur-md border-b border-gray-700/50 shadow-lg">
      <div class="max-w-4xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-gradient-to-r from-blue-600 to-purple-700 rounded-xl shadow-lg">
              <CpuChipIcon class="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 class="text-xl font-semibold text-white">AI Business Analyst</h1>
              <p class="text-sm text-gray-300">Proje analiz asistanınız</p>
            </div>
          </div>
          <Menu as="div" class="relative">
            <MenuButton class="p-2 text-gray-400 hover:text-gray-200 hover:bg-gray-800 rounded-lg transition-colors">
              <EllipsisVerticalIcon class="w-5 h-5" />
            </MenuButton>
            <transition
              enter-active-class="transition duration-100 ease-out"
              enter-from-class="transform scale-95 opacity-0"
              enter-to-class="transform scale-100 opacity-100"
              leave-active-class="transition duration-75 ease-in"
              leave-from-class="transform scale-100 opacity-100"
              leave-to-class="transform scale-95 opacity-0"
            >
              <MenuItems class="absolute right-0 mt-2 w-48 bg-gray-800 rounded-xl shadow-xl ring-1 ring-gray-700 ring-opacity-50 focus:outline-none z-10">
                <div class="p-1">
                  <MenuItem v-slot="{ active }">
                    <button :class="[active ? 'bg-gray-700' : '', 'group flex rounded-lg items-center w-full px-3 py-2 text-sm text-gray-200']">
                      <DocumentDuplicateIcon class="w-4 h-4 mr-3 text-gray-400" />
                      Oturumu Kopyala
                    </button>
                  </MenuItem>
                  <MenuItem v-slot="{ active }">
                    <button :class="[active ? 'bg-gray-700' : '', 'group flex rounded-lg items-center w-full px-3 py-2 text-sm text-gray-200']">
                      <TrashIcon class="w-4 h-4 mr-3 text-gray-400" />
                      Sohbeti Temizle
                    </button>
                  </MenuItem>
                </div>
              </MenuItems>
            </transition>
          </Menu>
        </div>
      </div>
    </div>

    <!-- Messages Container -->
    <div class="flex-1 overflow-hidden">
      <div class="h-full max-w-4xl mx-auto">
        <div
          ref="messageList"
          class="h-full overflow-y-auto px-6 py-6 space-y-6 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent"
        >
          <div class="space-y-6">
            <div
              v-for="msg in messages"
              :key="msg.id"
              :class="['flex items-start space-x-4', msg.author === 'user' ? 'flex-row-reverse space-x-reverse' : '']"
            >
              <!-- Avatar -->
              <div class="flex-shrink-0">
                <div
                  :class="[
                    'w-10 h-10 rounded-full flex items-center justify-center shadow-lg transition-all duration-200',
                    msg.author === 'ai'
                      ? 'bg-gradient-to-r from-blue-600 to-purple-700 text-white'
                      : 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white'
                  ]"
                >
                  <UserIcon v-if="msg.author === 'user'" class="w-5 h-5" />
                  <CpuChipIcon v-else class="w-5 h-5" />
                </div>
              </div>

              <!-- Message Bubble -->
              <div
                :class="[
                  'relative max-w-2xl rounded-2xl px-4 py-3 shadow-lg transition-all duration-200 hover:shadow-xl',
                  msg.author === 'ai'
                    ? 'bg-gray-800 border border-gray-700/50 text-gray-100'
                    : 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white'
                ]"
              >
                <p :class="['text-sm leading-relaxed', msg.author === 'ai' ? 'text-gray-100' : 'text-white']">
                  {{ msg.text }}
                </p>
                <div
                  :class="[
                    'absolute top-4 w-2 h-2 transform rotate-45',
                    msg.author === 'ai'
                      ? '-left-1 bg-gray-800 border-l border-b border-gray-700/50'
                      : '-right-1 bg-gradient-to-r from-emerald-600 to-teal-700'
                  ]"
                ></div>
              </div>
            </div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="isLoading" class="flex items-start space-x-4">
            <div class="flex-shrink-0">
              <div class="w-10 h-10 rounded-full bg-gradient-to-r from-blue-600 to-purple-700 flex items-center justify-center shadow-lg">
                <CpuChipIcon class="w-5 h-5 text-white" />
              </div>
            </div>
            <div class="relative bg-gray-800 border border-gray-700/50 rounded-2xl px-4 py-3 shadow-lg">
              <div class="flex items-center space-x-2">
                <div class="flex space-x-1">
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0s;"></div>
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.15s;"></div>
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.3s;"></div>
                </div>
                <span class="text-xs text-gray-400 ml-2">AI düşünüyor</span>
              </div>
              <div class="absolute top-4 -left-1 w-2 h-2 bg-gray-800 border-l border-b border-gray-700/50 transform rotate-45"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="bg-gray-900/80 backdrop-blur-md border-t border-gray-700/50">
      <div class="max-w-4xl mx-auto px-6 py-4">
        <form @submit.prevent="sendMessage" class="relative">
          <div class="relative flex items-center">
            <input
              v-model="newMessage"
              type="text"
              placeholder="Proje fikrinizi buraya yazın..."
              :disabled="isLoading"
              class="w-full pl-4 pr-12 py-3 bg-gray-800 border border-gray-700 rounded-xl text-sm placeholder-gray-400 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 disabled:bg-gray-900 disabled:text-gray-500 shadow-lg"
            />
            <button
              type="submit"
              :disabled="isLoading || newMessage.trim() === ''"
              class="absolute right-2 p-2 bg-gradient-to-r from-blue-600 to-purple-700 text-white rounded-lg hover:from-blue-700 hover:to-purple-800 transition-all duration-200 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transform hover:scale-105 disabled:transform-none"
            >
              <PaperAirplaneIcon class="w-4 h-4" />
            </button>
          </div>

          <!-- Subtle session info -->
          <div class="flex items-center justify-between mt-2 text-xs text-gray-400">
            <span>Session: {{ sessionId.slice(-8) }}</span>
            <span class="flex items-center space-x-1">
              <div class="w-2 h-2 bg-green-400 rounded-full"></div>
              <span>Bağlantı aktif</span>
            </span>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import {
  CpuChipIcon,
  UserIcon,
  PaperAirplaneIcon,
  EllipsisVerticalIcon,
  DocumentDuplicateIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'

// --- State Management ---
const messages = ref([
  {
    id: 1,
    text: 'Merhaba! Ben projenizin ön analizini yapmak için buradayım. Proje fikrinizi detaylıca anlatırsanız, kapsamlı bir analiz hazırlayabilirim.',
    author: 'ai'
  }
])
const newMessage = ref('')
const isLoading = ref(false)
const sessionId = ref(`session_${Date.now()}`)
const messageList = ref(null)

// --- Functions ---
const scrollToBottom = async () => {
  await nextTick()
  const list = messageList.value
  if (list) {
    list.scrollTop = list.scrollHeight
  }
}

const sendMessage = async () => {
  const userMessageText = newMessage.value.trim()
  if (!userMessageText || isLoading.value) return

  messages.value.push({
    id: Date.now(),
    text: userMessageText,
    author: 'user'
  })
  const currentMessage = newMessage.value
  newMessage.value = ''
  scrollToBottom()
  isLoading.value = true

  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId.value,
        message: currentMessage
      })
    })

    if (!response.ok) throw new Error('API isteği başarısız oldu.')

    const data = await response.json()

    messages.value.push({
      id: Date.now() + 1,
      text: data.answer,
      author: 'ai'
    })
  } catch (error) {
    console.error("Hata:", error)
    messages.value.push({
      id: Date.now() + 1,
      text: 'Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.',
      author: 'ai'
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
/* Custom scrollbar */
.scrollbar-thin::-webkit-scrollbar {
  width: 6px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background-color: rgb(75 85 99);
  border-radius: 3px;
}

.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background-color: rgb(107 114 128);
}

/* Message animations */
.message-enter-active {
  transition: all 0.3s ease-out;
}

.message-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.message-enter-to {
  opacity: 1;
  transform: translateY(0);
}
</style>
