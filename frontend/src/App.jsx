import { useState, useEffect } from 'react'
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import Home from './pages/home.jsx'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import SignupModal from './components/signup/signup.jsx'
import LoginModal from './components/login/login.jsx'


function App() {
	const [isSignupOpen, setIsSignupOpen] = useState(false)
	const [isLoginOpen, setIsLoginOpen] = useState(false)
	
  return (
	<BrowserRouter>
		<Routes>
			<Route path="/" element={<Home  setIsSignupOpen={setIsSignupOpen} setIsLoginOpen={setIsLoginOpen} />}/>
		</Routes>
		<SignupModal
			isOpen={isSignupOpen}
			onClose={() => setIsSignupOpen(false)}
			onSuccess={
				() => {
					setIsSignupOpen(false)
					setIsLoginOpen(true)
				}
			}
			/>
		
		<LoginModal 
			isOpen={isLoginOpen}
			onClose={() => setIsLoginOpen(false)}
		/>
	</BrowserRouter>

  )
}

export default App
