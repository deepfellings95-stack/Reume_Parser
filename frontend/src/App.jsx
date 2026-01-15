import { useState, useEffect } from 'react'
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import Home from './pages/home.jsx'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import SignupModal from './components/signup/signup.jsx'


function App() {
	const [isSignupOpen, setIsSignupOpen] = useState(false)
	
  return (
	<BrowserRouter>
		<Routes>
			<Route path="/" element={<Home  setIsSignupOpen={setIsSignupOpen} />}/>
		</Routes>
		<SignupModal
			isOpen={isSignupOpen}
			onClose={() => setIsSignupOpen(false)}
			/>
	</BrowserRouter>

  )
}

export default App
