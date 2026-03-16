<template>
  <h4
    data-slot="card-title"
    :class="cn('leading-none', className)"
  >
    <slot></slot>
  </h4>
</template>

<script setup lang="ts">
import { cn } from '../utils'

defineProps<{
  className?: string
}>()
</script>