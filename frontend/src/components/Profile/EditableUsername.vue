<script setup lang="ts">
import { nextTick, ref } from 'vue'
import { PencilIcon } from '@heroicons/vue/24/outline'

const props = defineProps<{ username: string; loading: boolean }>()

const emits = defineEmits<{
  (e: 'update', username: string): void
}>()

const isEditing = ref<boolean>(false)
const usernameInput = ref<HTMLInputElement | null>(null)
const newUsername = ref<string>('')

const startEditing = async () => {
  newUsername.value = props.username
  isEditing.value = true
  await nextTick()
  usernameInput.value?.focus()
}

const onUpdate = () => {
  if (!newUsername || newUsername.value === props.username) {
    isEditing.value = false
    return
  }
  const trimmedName = newUsername.value.trim()
  if (trimmedName && trimmedName !== props.username) {
    emits('update', trimmedName)
  }
  isEditing.value = false
}

const onBlur = () => {
  if (!props.loading) {
    isEditing.value = false
  }
}
</script>

<template>
  <div class="flex items-center gap-3 mb-2 md:justify-start">
    <template v-if="!isEditing">
      <h1 class="text-3xl font-bold">{{ props.username }}</h1>
      <button
        @click="startEditing"
        class="text-gray-400 hover:text-white transition cursor-pointer"
      >
        <PencilIcon class="w-5 h-5" />
      </button>
    </template>

    <form v-else @submit.prevent="onUpdate" class="flex items-center gap-3">
      <input
        ref="usernameInput"
        v-model="newUsername"
        @keyup.esc="isEditing = false"
        @blur="onBlur"
        type="text"
        class="w-full px-3 py-2 border rounded-md bg-gray-700 text-white"
        :disabled="props.loading"
      />
    </form>
  </div>
</template>
