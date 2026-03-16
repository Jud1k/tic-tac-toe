<script lang="ts" setup>
import { Card, CardTitle, CardContent, CardHeader, CardFooter } from '@/components/Card'
import { ArrowPathIcon } from '@heroicons/vue/24/solid'
import type { PlayerSymbol, GameBoard, Winner } from './types'

const props = defineProps<{
  board: GameBoard
  currentPlayer: PlayerSymbol
  winner: Winner | null
  winningLine?: number[]
  disabled?: boolean
  statusMessage:string
}>()

const emit = defineEmits({
  cellClick: (index: number) => {},
  reset: () => {},
})

</script>

<template>
  <div class="flex flex-col max-w-2xl mx-auto space-y-6">
    <h1 class="font-semibold text-2xl text-center">Game board</h1>
    <Card class="w-full">
      <CardHeader>
        <CardTitle class="text-center text-2xl font-bold">
          {{ statusMessage }}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-3 gap-3 max-w-md mx-auto aspect-square">
          <button
            class="aspect-square bg-gray-200 rounded-lg text-5xl font-bold flex items-center justify-center"
            v-for="(cell, index) in board"
            :key="index"
            :disabled="cell != null || !!props.winner || disabled"
            :class="[
              cell === 'X' ? 'text-blue-600' : 'text-red-600',
              props.winningLine?.includes(index) ? 'bg-green-400' : 'bg-gray-200',
              {
                'cursor-pointer hover:opacity-80 transition-all':
                  !cell && !props.winner && !disabled,
                'cursor-not-allowed': disabled && !props.winner,
              },
            ]"
            @click="emit('cellClick', index)"
          >
            <Transition name="pop" mode="out-in">
              <span :key="cell ? cell : 'empty'">
                {{ cell }}
              </span>
            </Transition>
          </button>
        </div>
      </CardContent>
      <CardFooter>
        <button
          class="flex items-center justify-center cursor-pointer gap-2 text-white bg-violet-400 w-full rounded-md py-3 hover:bg-violet-500 hover:opacity-80 transition-opacity"
          @click="emit('reset')"
        >
          <ArrowPathIcon class="w-6 h-6" />
          New game
        </button>
      </CardFooter>
    </Card>
  </div>
</template>

<style scoped>
.pop-enter-from,
.pop-leave-to {
  opacity: 0;
  transform: scale(0.5) rotate(-10deg);
}

.pop-enter-active,
.pop-leave-active {
  transition: all 0.08s ease-out;
}

.pop-enter-to,
.pop-leave-from {
  opacity: 1;
  transform: scale(1) rotate(0deg);
}
</style>
