import {useState, useEffect } from 'react'
import EmailStep from './email.jsx'
import UserData from './userData.jsx'
import OtpStep from './otpStep.jsx'


const SignupModal = ({ isOpen, onClose }) => {
	const [step, setStep] = useState('EMAIL')
  const [formData, setFormData] = useState({})

  if (!isOpen) return null


  return (
    <div className="fixed inset-0 z-[90] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div className="bg-white dark:bg-neutral-900 w-full max-w-2xl p-8 rounded-2xl shadow-2xl overflow-y-auto max-h-[90vh]">
	  <div className="grid grid-cols-3 space-between">
	  <p></p>
			<h2 className="text-2xl font-bold mb-6 text-heading text-center">Create account</h2>
			<div className="bg-white dark:bg-neutral-900">
		  <button type="button" className=" hover:bg-red-700 text-white font-bold  rounded-3xl" onClick={onClose}>x</button>
		  </div>
			
		</div>
		{step === "EMAIL" && (
			<EmailStep
				formData  ={formData}
				setFormData= {setFormData}
				onNext = {() => setStep("USERDATA")}
			/>
		)}

		{step === "USERDATA" && (
			<UserData formData = {formData}
			setFormData = {setFormData}
			onNext = {() => setStep('OTP')}
			onBack = {() => setStep('USERDATA')}
			/>
		)		
		}
				{step === "OTP" && (
			<OtpStep formData = {formData}
			onNext = {() => setStep('UserData')}
			onBack = {() => setStep('OTP')}
			/>
		)}
		
		<p className="mt-6"><i className="fa fa-google"></i> Sign in using google</p>
		</div>
	</div>
	)
}


export default SignupModal