import React from 'react'
import { useState } from 'react'

const LoginModal = ({isOpen, onClose}) => {
	const [data, setData] = useState({})
	if (!isOpen) return null
	
	const handleSubmit = async (e) => {
		e.preventDefault();
	try {
		const res = await fetch('http://localhost:5000/api/auth/login', {
			method: 'POST',
			credentials: 'include',
			headers:{'Content-Type':'application/json'},
			body:JSON.stringify({ email: data.email , password: data.password})
		})
		
		if (res.ok){
			const re = await res.json()
			console.log(re.message)
			onClose()
		}
		else {
			alert('Cannot Login sorry')
			return;
		}
	}
	catch (err) {
		console.log(err.message)
		return;
	}
	};
	
	return (
	<div className="fixed inset-0 z-[90] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div className="bg-white dark:bg-neutral-900 w-full max-w-2xl p-8 rounded-2xl shadow-2xl overflow-y-auto max-h-[90vh]">
	  <div className="grid grid-cols-3 space-between">
	  <p></p>
			<h2 className="text-2xl font-bold mb-6 text-heading text-center">Login Account</h2>
			<div className="bg-white dark:bg-neutral-900">
		  <button type="button" className=" hover:bg-red-700 text-white font-bold  rounded-3xl" onClick={onClose}>x</button>
		  </div>
			
		</div>
		<form onSubmit={handleSubmit}>
			<div>
				<input type="email" name="email" placeholder="email" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="password" name="password" placeholder="Password" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, password: e.target.value})} 	required />
			</div>
			<button type="submit">Login</button>
		</form>
		<p className="mt-6"><i className="fa fa-google"></i> Sign in using google</p>
		</div>
	</div>
	)
}

export default LoginModal;