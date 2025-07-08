<template>
  <Transition
    name="notification"
    enter-active-class="transition ease-out duration-300"
    enter-from-class="opacity-0 transform scale-90 translate-y-2"
    enter-to-class="opacity-100 transform scale-100 translate-y-0"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100 transform scale-100 translate-y-0"
    leave-to-class="opacity-0 transform scale-90 translate-y-2"
  >
    <div
      v-if="notification.show"
      :class="[
        'fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50',
        notificationClasses
      ]"
    >
      {{ notification.message }}
    </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  notification: {
    type: Object,
    required: true
  }
})

const notificationClasses = computed(() => {
  return props.notification.type === 'success'
    ? 'bg-green-600 text-white'
    : 'bg-red-600 text-white'
})
</script>
