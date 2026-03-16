import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as authApi from '@/api/auth'

export const useAuth = defineStore('auth', () => {
  const isLoggedIn = ref<boolean>(localStorage.getItem('accessToken') !== null)
  const isLoading = ref<boolean>(false)
  const userId = ref<string|null>(null)

  const signup = async (username: string, password: string) => {
    isLoading.value = true
    try {
      await authApi.signup(username, password)
    } finally {
      isLoading.value = false
    }
  }

  const login = async (username: string, password: string) => {
    isLoading.value = true
    try {

      const response = await authApi.login(username, password)
      localStorage.setItem('accessToken', response.accessToken)
      isLoggedIn.value = true
      userId.value = response.userId
    } finally {
      isLoading.value = false
    }
  }

  const fetchMe = async () => {
    isLoading.value = true
    try {
      const response = await authApi.getMe()
      userId.value = response.id
      isLoggedIn.value = true
    } finally {
      isLoading.value = false
    }
  }

  const logout = async() => {
    isLoading.value = true
    try {
      await authApi.logout()
      localStorage.removeItem('accessToken')
      isLoggedIn.value = false
      userId.value = null
    } finally {
      isLoading.value = false
    }
  }
 

  return {
    isLoggedIn,
    isLoading,
    userId,
    signup,
    login,
    fetchMe,
    logout,
  }
})
