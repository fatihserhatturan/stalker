<template>
  <div class="flex flex-col items-end space-y-2">
    <SuggestionItem
      v-for="(suggestion, index) in suggestions"
      :key="index"
      :suggestion="suggestion"
      :delay="index * 100"
      @click="$emit('suggestion-selected', suggestion)"
    />
  </div>
</template>

<script setup>
import SuggestionItem from './SuggestionItem.vue'

defineProps({
  suggestions: {
    type: Array,
    default: () => []
  }
})

defineEmits(['suggestion-selected'])
</script>
