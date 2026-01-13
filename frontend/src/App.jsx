import { Routes, Route, Navigate } from "react-router-dom"
import Dashboard from "./pages/Dashboard"

function App() {
  return (
    <Routes>
      <Route path="http://127.0.0.1:5000/api/dashboard" element={<Navigate to="/dashboard" />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  )
}

export default App
