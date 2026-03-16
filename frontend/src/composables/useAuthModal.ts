import { useRouter } from 'vue-router'

export const useAuthModal = () => {
  const router = useRouter()

  const openAuthModal = (method: 'signup' | 'login' = 'signup') => {
    router.replace({
      query: {
        ...router.currentRoute.value.query,
        modal: 'auth',
        method: method,
      },
    })
  }

  return { openAuthModal: openAuthModal }
}
