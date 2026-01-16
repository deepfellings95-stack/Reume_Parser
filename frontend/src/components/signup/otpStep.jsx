import React from 'react'
import {useState} from 'react'

const OtpStep = ({formData, done, onPrevious, onBack}) => {
	const [otp, setOtp] = useState('')
	
	const handleSubmit = async (e) => {
		e.preventDefault();
		
		console.log(otp)
		const res = await fetch('http://localhost:5000/api/auth/verify_otp', {
			method:'POST',
			headers:{"Content-Type":"application/json"},
			body: JSON.stringify({email: formData.email, otp: otp , userData: formData})
		})
		
		try {
		if (res.ok){
			const result = await res.json()
			console.log(result.message)
			done()
		}
		
		else{
			alert('Something went wrong, probably developers fault, or you may have clicked getotp button many times');
			return;
		}
		}
		catch (error) {
        console.error("Fetch Error:", error);
        alert('Could not connect to the server. Check if Flask is running.');
		}
	}
	return (
        <form onSubmit={handleSubmit} >
			<h3>We sent you OPT at your email address: {formData.email}</h3>
			<input type="number" name="otp" placeholder="enter your OTP" className="mb-6  bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setOtp(e.target.value)} 	required />
			<button type='submit'>Complete SignUp</button>
			<div className="grid gap-4 md:grid-cols-2">
				<button type="button" onClick={onPrevious}>Back</button>
				<button type="button" onClick={onBack}>Refill Form</button>
			</div>
		</form>
    );
};

export default OtpStep;