import { useState, useEffect } from 'react';
import BaseLayout from './base.jsx';

function Home({setIsSignupOpen, setIsLoginOpen, isAuthenticated}) {
  // const [inputValue, setInputValue] = useState('');
  // const [result, setResult] = useState(null);

  // const handleVerify = async (e) => {
    // e.preventDefault();

    // Sending the data to Flask
    // const response = await fetch('http://127.0.0.1:5000/api/check-word', {
      // method: 'POST',
      // headers: { 'Content-Type': 'application/json' },
      // body: JSON.stringify({ word: inputValue })
    // });

    // const data = await response.json();
    // setResult(data); // Save the Flask response (success and message)
  // };

  const [message, setMessage] = useState(null)
  
  useEffect(() => {
	  fetch('/api', {
    credentials: 'include' // ⭐ REQUIRED
  })
	  .then(res => res.json())
	  .then(data => setMessage(data.message))
  }, []
  )

  return (
    <BaseLayout
      setIsSignupOpen={setIsSignupOpen}
      setIsLoginOpen={setIsLoginOpen}
	  isAuthenticated={isAuthenticated}
    >
      {/* HERO */}
      <section className="min-h-screen flex flex-col justify-center items-center text-white px-6">
        <h1 className="text-4xl md:text-6xl font-bold mb-4 text-center">
          Ace Your Resume 🚀
        </h1>

        <p className="text-lg md:text-xl max-w-2xl text-center text-red-100 mb-6">
          Upload your resume, analyze it with AI, and improve your chances of landing interviews.
        </p>
		{ !isAuthenticated ? (
		
        <div className="flex gap-4">
          <button
            onClick={() => setIsSignupOpen(true)}
            className="bg-white text-red-700 px-6 py-3 rounded-lg font-semibold hover:bg-red-100 transition"
          >
            Get Started
          </button>

          <button
            onClick={() => setIsLoginOpen(true)}
            className="border border-white px-6 py-3 rounded-lg hover:bg-white hover:text-red-700 transition"
          >
            Login
          </button>
        </div>
		) : (
		<button
			onClick={async () => { await fetch('http://localhost:5000/api/auth/logout', { method: 'POST', credentials: 'include'})}}
            className="bg-white text-red-700 px-6 py-3 rounded-lg font-semibold hover:bg-red-100 transition"
          >
            Hello : {message}
          </button>
		)}

        {message && (
          <p className="mt-6 text-sm text-red-200">
            Backend says: {message}
          </p>
        )}
      </section>

      {/* HOW IT WORKS */}
      <section className="text-center px-6">
        <h2 className="text-3xl font-bold mb-10">How It Works</h2>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div className="p-6 border rounded-lg shadow-sm">
            <h3 className="text-xl font-semibold mb-2">1. Upload Resume</h3>
            <p className="text-gray-600">
              Upload your resume in PDF or DOC format.
            </p>
          </div>

          <div className="p-6 border rounded-lg shadow-sm">
            <h3 className="text-xl font-semibold mb-2">2. Analyze</h3>
            <p className="text-gray-600">
              We analyze skills, keywords, and formatting.
            </p>
          </div>

          <div className="p-6 border rounded-lg shadow-sm">
            <h3 className="text-xl font-semibold mb-2">3. Improve</h3>
            <p className="text-gray-600">
              Get actionable feedback to improve your resume.
            </p>
          </div>
        </div>
      </section>
	  <section className="py-24  px-6">
  <h2 className="text-3xl font-bold text-center mb-12">
    Powerful Features
  </h2>

  <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
    <div className="p-6 border rounded-xl shadow-sm">
      <h3 className="text-xl font-semibold mb-2">AI Resume Analysis</h3>
      <p className="text-gray-600">
        Get instant feedback on skills, keywords, and formatting.
      </p>
    </div>

    <div className="p-6 border rounded-xl shadow-sm">
      <h3 className="text-xl font-semibold mb-2">ATS Friendly</h3>
      <p className="text-gray-600">
        Optimize your resume to pass Applicant Tracking Systems.
      </p>
    </div>

    <div className="p-6 border rounded-xl shadow-sm">
      <h3 className="text-xl font-semibold mb-2">Actionable Suggestions</h3>
      <p className="text-gray-600">
        Clear steps to improve your resume instantly.
      </p>
    </div>
  </div>
</section>
<section className="py-20 bg-red-700 text-white text-center px-6">
  <h2 className="text-3xl font-bold mb-4">
    Ready to Improve Your Resume?
  </h2>

  <p className="mb-6 text-red-100">
    Join thousands of users improving their careers.
  </p>

  {!isAuthenticated && (
    <button
      onClick={() => setIsSignupOpen(true)}
      className="bg-white text-red-700 px-8 py-3 rounded-lg font-semibold hover:bg-red-100 transition"
    >
      Get Started Free
    </button>
  )}
</section>
<section className="py-20 px-6">
  <h2 className="text-3xl font-bold text-center mb-12">
    What Users Say
  </h2>

  <div className="max-w-4xl mx-auto grid md:grid-cols-2 gap-8">
    <div className="p-6 rounded-xl shadow">
      <p className="text-gray-600">
        “This tool helped me land my first interview in weeks!”
      </p>
      <p className="mt-4 font-semibold">— Student Developer</p>
    </div>

    <div className="p-6  rounded-xl shadow">
      <p className="text-gray-600">
        “Simple, clean, and very effective resume feedback.”
      </p>
      <p className="mt-4 font-semibold">— Junior Engineer</p>
    </div>
  </div>
</section>

    </BaseLayout>
  );
}

export default Home;