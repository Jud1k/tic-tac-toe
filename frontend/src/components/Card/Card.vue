<template>
  <div
    data-slot="card"
    :class="cn('flex flex-col gap-6 rounded-xl border border-custom-transparent', className)"
  >
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { cn } from '../utils'

defineProps<{
  className?: string
}>()
</script>
