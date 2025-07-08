<template>
  <div
    :class="[
      'flex items-start space-x-4',
      message.author === 'user' ? 'flex-row-reverse space-x-reverse' : ''
    ]"
  >
    <MessageAvatar :author="message.author" />

    <MessageBubble
      :message="message"
      :is-user="message.author === 'user'"
    />
  </div>
</template>

<script setup>
import MessageAvatar from './MessageAvatar.vue'
import MessageBubble from './MessageBubble.vue'

defineProps({
  message: {
    type: Object,
    required: true
  }
})
</script>
