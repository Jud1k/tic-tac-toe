<script lang="ts" setup>
import { ref, watch } from 'vue'
import { useAuth } from '@/composables/auth'
import { getErrorMessage } from '@/utils'

const props = defineProps({
  method: {
    type: String,
    default: 'login',
  },
})

const authStore = useAuth()
const error = ref<string | null>(null)

const form = ref({
  username: '',
  password: '',
})

const emit = defineEmits<{ success: [] }>()

async function handleSubmit() {
  try {
    error.value = null
    if (props.method === 'login') {
      await authStore.login(form.value.username, form.value.password)
    } else {
      await authStore.signup(form.value.username, form.value.password)
      await authStore.login(form.value.username, form.value.password)
    }
    emit('success')
    form.value.username = ''
    form.value.password = ''
    console.log(`${props.method} form submitted:`, form.value)
  } catch (err: unknown) {
    error.value = getErrorMessage(err)
    console.error(err)
  }
}

watch(
  () => props.method,
  () => {
    error.value = null
    form.value.username = ''
    form.value.password = ''
    console.log(props.method)
  },
)
</script>

<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div>
      <h1 class="text-red-600 p-2 rounded-md" v-if="error">
        {{ error ? error : '' }}
      </h1>
      <label class="block text-sm font-medium mb-1 text-gray-200"> Username </label>
      <input
        v-model="form.username"
        @input="error = null"
        type="text"
        class="w-full px-3 py-2 border rounded-md bg-gray-700 text-white"
        required
      />
    </div>
    <div>
      <label class="block text-sm font-medium mb-1 text-gray-200"> Password </label>
      <input
        v-model="form.password"
        @input="error = null"
        type="password"
        class="w-full px-3 py-2 border rounded-md bg-gray-700 text-white"
        required
      />
    </div>
    <button
      type="submit"
      class="cursor-pointer w-full mt-4 py-2 px-4 rounded-md font-medium bg-blue-600 hover:bg-blue-700 text-white transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
      :disabled="authStore.isLoading"
    >
      {{ props.method === 'login' ? 'Log In' : 'Sign Up' }}
    </button>
  </form>
</template>
