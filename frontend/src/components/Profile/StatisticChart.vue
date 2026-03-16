<script setup lang="ts">
import { computed, watch, nextTick, shallowRef } from 'vue'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, type ChartData } from 'chart.js'
import { Pie } from 'vue-chartjs'
import { ChartPieIcon } from '@heroicons/vue/20/solid'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  wins: {
    type: Number,
    required: true,
  },
  draws: {
    type: Number,
    required: true,
  },
  losses: {
    type: Number,
    required: true,
  },
})

const chartData = computed<ChartData<'pie'>>(() => ({
  labels: ['Wins', 'Losses', 'Draws'],
  datasets: [
    {
      backgroundColor: ['#22c55e', '#ef4444', '#eab308'],
      data: [props.wins, props.losses, props.draws],
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
  },
  animation: {
    animateScale: true,
    duration: 1200,
  },
  animations: {
    radius: {
      duration: 1200,
      easing: 'easeOutQuart',
      delay(ctx: any) {
        return ctx.dataIndex * 400
      },
    },
  },
} as const
</script>

<template>
  <div class="flex-col">
    <div v-if="props.wins == 0 && props.draws == 0 && props.losses == 0" class="">
      <ChartPieIcon class=""/>
    </div>
    <div v-else class="flex items-center justify-center">
      <Pie ref="chartRef" :data="chartData" :options="chartOptions" />
    </div>

    <div class="flex justify-center gap-4 mt-4">
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 bg-green-500 rounded-full"></div>
        <span class="text-sm">Wins ({{ wins }})</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 bg-red-500 rounded-full"></div>
        <span class="text-sm">Losses ({{ losses }})</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
        <span class="text-sm">Draws ({{ draws }})</span>
      </div>
    </div>
  </div>
</template>
