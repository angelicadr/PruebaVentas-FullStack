import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
})

export async function login(username: string, password: string) {
  const r = await axios.post((import.meta as any).env.VITE_API_AUTH || 'http://localhost:8000/api/v1/auth/login', { username, password })
  const token = r.data.access
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  return token
}
