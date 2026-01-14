import {useState, useEffect } from 'react'

const SignupModal = ({ isOpen, onClose }) => {
  const [formData, setFormData] = useState({
    username:'',
    name:'',
    email:'',
    dob:'',
    password:'',
    confirmPassword:''
  })

  if (!isOpen) return null

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match")
      return
    }

    const response = await fetch("/api/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData)
    })

    const data = await response.json()

    if (response.ok) {
      alert("Account created")
      onClose()
    } else {
      alert(data.message || "Signup failed")
    }
  }

  return (
    <div className="fixed inset-0 z-[90] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div className="bg-white dark:bg-neutral-900 w-full max-w-2xl p-8 rounded-2xl shadow-2xl overflow-y-auto max-h-[90vh]">
        <h2 className="text-2xl font-bold mb-6 text-heading text-center">Create account</h2>

        <form onSubmit={handleSubmit} className="grid gap-4 md:grid-cols-2">
					<input 
          type="text" 
          placeholder="Full Name"
          className="bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5" 
          onChange={(e) => setFormData({...formData, name: e.target.value})} 
		  required
        />
		<input type="date" name="dob" placeholder="dob" className="bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-xl focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setFormData({...formData, dob: e.target.value})} required/>
			
					<input 
					type="email" 
					name="email"
					placeholder="email"
					className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setFormData({...formData, email: e.target.value})} 
					required />
					<input type="text" name="username" placeholder="Choose Username" className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setFormData({...formData, username: e.target.value})} required />
					<input type="password" name="password" placeholder="create password" className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setFormData({...formData, password: e.target.value})} required />
					<input type="password" name="confirmPassword" placeholder="confirm password" className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})} required />
					<button type="submit" name="submit">Get OTP</button>
					<button type="button" onClick={onClose} name="cancle">Cancel</button>
				</form>
				<p><i className="fa fa-google"></i> Sign in using google</p>
			</div>
		</div>
	)
}


export default SignupModal