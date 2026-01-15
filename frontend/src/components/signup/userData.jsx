import React from 'react'; // Fixed typo
import { useState } from 'react'

const UserData = ({formData, setFormData, onNext, onBack}) => {
	const [userData, setUserData] = useState({})
    return (
		<form onSubmit={handleSubmit} method="POST">
			 // city = db.Column(db.String())
			// state = db.Column(db.String())
			// zip_code = db.Column(db.Integer())
			// planet = db.Column(db.String())
			<div className="grid gap-4 md:grid-cols-2">
				<input type="text" name="city" placeholder="city" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="text" name="state" placeholder="Satae" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="number" name="zipcode" placeholder="Number" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="text" name="other_location" placeholder="Address line" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
			</div>	
				//Personal data
				    // age = db.Column(db.Integer())
    // need = db.Column(db.String())
    // members = db.Column(db.String())
    // education = db.Column(db.String())
			{ formData.accountType === "personal" && (
				<div>
				<input type="number" name="age" placeholder="Age" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="text" name="need" placeholder="reason to use our site" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="text" name="members" placeholder="How many people in your home" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="text" name="education" placeholder="education" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				</div>
			)}
			
			//Student Data
			    // university_name = db.Column(db.String())
    // course = db.Column(db.String())
    // student_id = db.Column(db.String())
    // university_link = db.Column(db.String())
    // need = db.Column(db.String())
			
			{ formData.accountType === "student" && (		
<div>			
				<input type="text" name="universityName" placeholder="University Name" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="text" name="course" placeholder="Course" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="text" name="student_id" placeholder="Student Id if Available" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="text" name="university_link" placeholder="University Link" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="text" name="need" placeholder="What purpose you are using our tool" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				</div>
			)}
			
			
				<input type="email" name="email" placeholder="email" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="email" name="email" placeholder="email" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="email" name="email" placeholder="email" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="email" name="email" placeholder="email" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
				<input type="email" name="email" placeholder="email" className="mb-6 mt-6 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-lg focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" onChange={(e) => setData({...data, email: e.target.value})} 	required />
			<div>
			</div>
		</form>
    );
};

export default UserData