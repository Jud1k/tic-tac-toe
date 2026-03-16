import api from '@/api/axiosConfig'
import { type AuthResponse } from '@/api/axiosConfig'

type User={
  id: string
  username: string
}

export const signup = async (username: string, password: string): Promise<string> => {
  const response = await api.post<string>('/signup', { username, password })
  return response.data
}

export const login = async (username: string, password: string): Promise<AuthResponse> => {
  const params = new URLSearchParams()
  params.append('username', username)
  params.append('password', password)
  const response = await api.post<AuthResponse>('/login/access-token', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return response.data
}

export const getMe = async (): Promise<User> => {
  const response = await api.get<User>('/me')
  return response.data
}

export const logout = async (): Promise<void> => {
  await api.post('/logout')
}