import { useEffect, useState } from "react"

function MainLayout({ children }) {
  const [dark, setDark] = useState(
    localStorage.theme === "dark"
  )

  useEffect(() => {
    if (dark) {
      document.documentElement.classList.add("dark", "bg-gray-900")
      localStorage.theme = "dark"
    } else {
      document.documentElement.classList.remove("dark", "bg-gray-900")
      localStorage.theme = "light"
    }
  }, [dark])

  return (
    <>
      {/* Sidebar */}
      <aside className="bg-gray-500 py-6 pl-6 fixed h-screen w-64">
        <h1 className="text-2xl font-bold text-slate-300 mb-6">
          Resume Parser
        </h1>

        <nav className="space-y-4">
          <a
            href="/dashboard"
            className="block py-2 px-4 rounded-lg font-semibold"
          >
            Dashboard
          </a>

          <button
            onClick={() => setDark(!dark)}
            className="py-2 px-4 rounded-lg bg-gray-300"
          >
            {dark ? "Light Mode" : "Dark Mode"}
          </button>
        </nav>
      </aside>

      {/* Main content */}
      <main className="ml-64 p-6 min-h-screen">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-slate-700 text-slate-200 py-6 mt-12">
        <p className="text-center text-sm">
          Resume Parsing Web Application
        </p>
      </footer>
    </>
  )
}

export default MainLayout
