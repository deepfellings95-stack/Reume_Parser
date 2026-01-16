import { useState, useEffect } from 'react';
import BaseLayout from './base.jsx';

function Home({setIsSignupOpen, setIsLoginOpen}) {
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
  <BaseLayout setIsSignupOpen={setIsSignupOpen}  setIsLoginOpen={setIsLoginOpen}>
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>{message}</h1>
      
    </div>
  </BaseLayout>
	
  );
}

export default Home;