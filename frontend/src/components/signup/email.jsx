import {useState, useEffect } from 'react'

const EmailStep = ({formData, setFormData, onNext }) => {
  const [data, setData] = useState({name:'', dob:'', email:'', username:'', password:'', confirmPassword:'', accountType:''})
  
  const handleSubmit = async (e) => {
	  e.preventDefault();
	  
	  if(data.password !== data.confirmPassword){
		  alert('Password does not match');
		  return
	  }
	  
	// const res = await fetch('http://localhost:5000/api/auth/send_otp', {
		// method:"POST",
		// headers:{'Accept': 'application/json', // Add this line
        // 'Content-Type': 'application/json'},
		// body:JSON.stringify({email: data.email})
	// })  
	
	// if (res.ok){
		// const result = await res.json();
      // console.log(result.message);
	// setFormData({...formData, ...data});
	  
      // onNext();
    // }
	// else {
		// alert("Something went wrong");
		// return ;
	// }
	
	setFormData({...formData, ...data})
	onNext()
    };
	
  return (
	<form onSubmit={handleSubmit} method="POST">
			<div className="grid gap-4 md:grid-cols-2">
					<input 
					  type="text" 
					  placeholder="Full Name"
					  className="bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5" 
					  onChange={(e) => setData({...data, name: e.target.value})} 
					  required
					/>
					<input type="date" name="dob" placeholder="dob" className="bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-xl focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, dob: e.target.value})} required/>
			</div>
					<input type="email" name="email" placeholder="email" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
					<input type="text" name="username" placeholder="Choose Username" className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, username: e.target.value})} required />
			<div className="grid gap-4 md:grid-cols-2">		
					<input type="password" name="password" placeholder="create password" className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, password: e.target.value})} required />
					<input type="password" name="confirmPassword" placeholder="confirm password" className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, confirmPassword: e.target.value})} required />
					<select name="cars" value={data.accountType} onChange={(e) => setData({...data, accountType: e.target.value})} required className="rounded-lg bg-neutral-secondary-medium border  text-heading text-sm focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" id="car-select">
					  <option value="" disabled>Select Account Type</option>
					  <option value="personal">Personal</option>
					  <option value="student">Student</option>
					  <option value="corporate">Corporate</option>
					  <option value="other">Other</option>
					</select>
					<button type="submit" className="bg-blue-500" name="submit">Get OTP</button>
			</div>
	</form>

	);
};


export default EmailStep