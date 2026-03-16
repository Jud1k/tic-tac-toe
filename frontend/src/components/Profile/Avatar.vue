<script setup lang="ts">
import { computed, ref } from 'vue'
import { CameraIcon } from '@heroicons/vue/24/outline'
import { cld } from '@/cloudinary'
import { AdvancedImage } from '@cloudinary/vue'
import { fill } from '@cloudinary/url-gen/actions/resize'
import { focusOn } from '@cloudinary/url-gen/qualifiers/gravity'
import { FocusOn } from '@cloudinary/url-gen/qualifiers/focusOn'
import AvatarImage from '../AvatarImage.vue'

const emits = defineEmits<{
  (e: 'update', file: File): void
}>()

const props = defineProps<{
  imageUrl: string
}>()

const currentImageUrl = ref<string>(props.imageUrl)

const fileInput = ref<HTMLInputElement | null>(null)

const onUpdate = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) {
    return
  }
  emits('update', file)
}
</script>

<template>
  <div class="relative">
    <input type="file" class="hidden" ref="fileInput" @change="onUpdate" accept="image/*" />
    <AvatarImage
      :image-url="currentImageUrl"
      :width="200"
      :height="200"
      class="w-32 h-32 rounded-full border-4 border-gray-600"
    />
    <button
      class="absolute cursor-pointer bottom-2 right-2 bg-purple-600 rounded-full p-2 hover:bg-purple-400"
      @click="fileInput?.click()"
      type="button"
    >
      <CameraIcon class="w-5 h-5" />
    </button>
  </div>
</template>
