import { useEffect, useState } from "react"
import api from "../services/api"
import MainLayout from "../layouts/MainLayout"

function Dashboard() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get("dashboard")
      .then(res => {
		  console.log("API DATA:", res.data) //
        setPosts(res.data.posts)
		
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return <p>Loading...</p>

  return (
    <MainLayout>
      {/* existing dashboard JSX stays SAME */}
    </MainLayout>
  )
}

export default Dashboard
