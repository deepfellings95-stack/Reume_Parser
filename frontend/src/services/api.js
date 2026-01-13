import axios from "axios"

const api = axios.create({
  baseURL: "/api",
  withCredentials: true   // 🔥 THIS IS THE KEY
})

export default api
