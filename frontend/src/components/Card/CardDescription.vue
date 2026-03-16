<template>
  <p
    data-slot="card-description"
    :class="cn('', className)"
  >
    <slot></slot>
  </p>
</template>

<script setup lang="ts">
import { cn } from '../utils'

defineProps<{
  className?: string
}>()
</script>