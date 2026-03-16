<script setup lang="ts">
import { onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import { CalendarIcon, TrophyIcon } from '@heroicons/vue/24/outline'
import { CardContent, CardTitle, CardHeader, Card } from '@/components/Card'
import Spinner from '@/components/Spinner.vue'
import { formatDate, getErrorMessage } from '@/utils'
import { toast } from 'vue3-toastify'
import StatisticChart from '@/components/Profile/StatisticChart.vue'
import EditableUsername from '@/components/Profile/EditableUsername.vue'
import Avatar from '@/components/Profile/Avatar.vue'
import { deleteFromCloudinary, uploadToCloudinary } from '@/cloudinary'
import { getPlayerWithRank, updatePlayer, type PlayerWithRank } from '@/api/player'
import RecentGames from '@/components/Profile/RecentGames.vue'

const isLoading = ref<boolean>(false)
const currentPlayer = ref<PlayerWithRank | null>(null)

const fetchPlayer = async () => {
  try {
    isLoading.value = true
    const player = await getPlayerWithRank()
    currentPlayer.value = player
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  await fetchPlayer()
})

const updateAvatar = async (file: File) => {
  isLoading.value = true
  let uploadedImageUrl: string | null = null
  try {
    uploadedImageUrl = await uploadToCloudinary(file)
    try {
      const updatedPlayer = await updatePlayer({ imageUrl: uploadedImageUrl })
      if (updatedPlayer.imageUrl !== uploadedImageUrl) {
        throw new Error('Failed to update avatar in database')
      }
      if (currentPlayer.value) {
        currentPlayer.value = updatedPlayer
      }
    } catch (err) {
      if (uploadedImageUrl) {
        await deleteFromCloudinary(uploadedImageUrl).catch((err) => {
          console.error(err)
        })
      }
      throw err
    }
    toast.success('Avatar updated successfully')
  } catch (err) {
    toast.error(getErrorMessage(err))
  } finally {
    isLoading.value = false
  }
}

const updateUsername = async (newUsername: string) => {
  isLoading.value = true
  try {
    const newPlayer = await updatePlayer({ username: newUsername })
    currentPlayer.value = newPlayer
    toast.success('Username updated successfully')
  } catch (err) {
    toast.error(getErrorMessage(err))
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <AppLayout>
    <div class="container px-4 py-8">
      <Card class="mb-8">
        <div class="flex flex-col md:flex-row items-center gap-6 p-6">
          <Spinner v-if="isLoading" size="sm" />
          <Avatar
            v-else-if="currentPlayer"
            :image-url="currentPlayer?.imageUrl"
            @update="updateAvatar"
          />
          <div class="flex-1 text-center md:text-left">
            <div>
              <Spinner v-if="isLoading" size="sm" />
              <EditableUsername
                v-else-if="currentPlayer"
                :username="currentPlayer.username"
                :loading="isLoading"
                @update="updateUsername"
              />
            </div>
            <div class="flex flex-wrap gap-4 justify-center md:justify-start">
              <Spinner v-if="isLoading" size="sm" />
              <div v-else class="flex gap-3">
                <div class="flex items-center gap-2">
                  <CalendarIcon class="w-4 h-4 text-gray-400" />
                  <span class="text-gray-400"
                    >Joined {{ currentPlayer ? formatDate(currentPlayer?.createdAt) : '' }}</span
                  >
                </div>
                <div class="flex items-center gap-2">
                  <TrophyIcon class="w-4 h-4 text-yellow-400" />
                  <span class="text-gray-400"
                    >Rank: {{ currentPlayer?.rank || 'Failed to load rank' }}</span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </Card>

      <div class="grid lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Recent Games</CardTitle>
            </CardHeader>
            <CardContent>
              <RecentGames />
            </CardContent>
          </Card>
        </div>

        <div class="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Game Distribution</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="flex items-center justify-center">
                <StatisticChart
                  v-if="!isLoading && currentPlayer"
                  :wins="currentPlayer.wins"
                  :draws="currentPlayer.draws"
                  :losses="currentPlayer.losses"
                />
                <Spinner v-else-if="isLoading" size="md" />
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  </AppLayout>
</template>
