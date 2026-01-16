import React from 'react'; // Fixed typo
import { useState } from 'react'

const UserData = ({formData, setFormData, onNext, onBack}) => {
	const [userData, setUserData] = useState({})
	
	const handleSubmit = async (e) => {
		e.preventDefault();
		
		let cleanUpData = {
			city : userData.city,
			state : userData.state,
			zipcode : userData.zipcode,
			other_location: userData.other_location
		}
		
		if (formData.accountType === "personal") {
			cleanUpData = {...cleanUpData,
				age: userData.age,
				need: userData.need,
				members: userData.members,
				education: userData.education
			};
		}
		
		else if (formData.accountType === "student"){
			cleanUpData = {...cleanUpData,
				universityName : userData.universityName,
				course: userData.course,
				student_id: userData.student_id,
				university_link: userData.university_link,
				need: userData.need
			};
		}
		
		else if ( formData.accountType === "corporate"){
			cleanUpData = {...cleanUpData,
				company_type: userData.company_type,
				company_strength: userData.company_strength,
				company_web_link: userData.company_web_link,
				company_name: userData.company_name,
				job_title: userData.job_title
			}	;
		}
		setFormData({...formData, ...cleanUpData})
	try{	
		const res = await fetch('http://localhost:5000/api/auth/send_otp', {
			method:"POST",
			headers: {"Content-Type":"application/json"},
			body: JSON.stringify({email: formData.email})
		})
		
		if (!res.ok){
			let r = await res.json()
			alert(r.message)
			return ;
		}
		
		else if (res.ok){
			const result = await res.json();
			console.log(result.message)
			onNext()			
		}
		else {
			alert('Something went wrong, will you fill up your form again, else this is server side error')
			return;
		}
	}
	
	catch (err) {
        console.error("Error fetching data:", err.message);
		return ;
	}
	};
	
    return (
	<div>
		<form onSubmit={handleSubmit} method="POST">
			<div className="grid gap-4 md:grid-cols-2">
				<input type="text" required name="city" placeholder="city" className=" bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setUserData({...userData, city: e.target.value})} 	required />
				<input type="text" required name="state" placeholder="Satae" className="  bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body"				onChange={(e) => setUserData({...userData, state: e.target.value})} 	required />
				<input type="number" required name="zipcode" placeholder="Zip Code please" className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" 				onChange={(e) => setUserData({...userData, zipcode: e.target.value})} 	required />
				<input type="text" required name="other_location" placeholder="Address line" className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" 				onChange={(e) => setUserData({...userData, other_location: e.target.value})} 	required />
			</div>	
			{ formData.accountType === "personal" && (
				<div>
				<input type="number" required name="age" placeholder="Age" className="mb-6  bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" 				onChange={(e) => setUserData({...userData, age: e.target.value})} 	required />
				<input type="text" required name="need" placeholder="reason to use our site" className="mb-6  bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" 				onChange={(e) => setUserData({...userData, need: e.target.value})} 	required />
				<input type="text" required name="members" placeholder="How many people in your home" className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body"				onChange={(e) => setUserData({...userData, members: e.target.value})} 	required />
				<input type="text" required name="education" placeholder="qualification" className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body"				onChange={(e) => setUserData({...userData, education: e.target.value})} 	required />
				</div>
			)}
			
			{ formData.accountType === "student" && (		
<div>			
				<input type="text" required name="universityName" placeholder="University Name" className="mb-6  bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body"				onChange={(e) => setUserData({...userData, universityName: e.target.value})} 	required />
				<input type="text" required name="course" placeholder="Course" className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body"				onChange={(e) => setUserData({...userData, course: e.target.value})} 	required />
				<input type="text" required name="student_id" placeholder="Student Id if Available" className="mb-6  bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" 				onChange={(e) => setUserData({...userData, student_id: e.target.value})} 	required />
				<input type="text" required name="university_link" placeholder="University Link" className="mb-6  bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" 				onChange={(e) => setUserData({...userData, university_link: e.target.value})} 	required />
				<input type="text" required name="need" placeholder="What purpose you are using our tool" className="mb-6  bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body"				onChange={(e) => setUserData({...userData, need: e.target.value})} 	required />
				</div>
			)}
			{ formData.accountType === "corporate" && (
			<div>
				<input type="text" required name="company_type" placeholder="Company Type" className="mb-6  bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body"				onChange={(e) => setUserData({...userData, company_type: e.target.value})} 	required />
				<input type="text" required name="company_strength" placeholder="Company Strength" className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" 				onChange={(e) => setUserData({...userData, strength: e.target.value})} 	required />
				<input type="text" required name="company_web_link" placeholder="Link to your company mail" className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" 				onChange={(e) => setUserData({...userData, company_link: e.target.value})} 	required />
				<input type="text" required name="company_name" placeholder="company name" className="mb-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" 				onChange={(e) => setUserData({...userData, company_name: e.target.value})} 	required />
				<input type="text" required name="job_title" placeholder="Job title" className="mb-6  bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" 				onChange={(e) => setUserData({...userData, job_title: e.target.value})} 	required />
			
			</div>
			)}
			<div className="grid gap-4 md:grid-cols-2">
			<p className=" text-green-800">Click only one time</p>
		<button type="submit" >Next</button>
			
			
			
			</div>
		</form>
			<button type="button" onClick={onBack}>Go Back</button>
		
		</div>
    );
};

export default UserData;