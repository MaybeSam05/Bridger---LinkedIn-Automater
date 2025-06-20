import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API_BASE_URL } from "../config";

const banner = "py-4 px-6 md:px-12 flex justify-between items-center";
const img = "object-contain";
const getStartedButton = "text-white font-bold px-8 py-2 text-lg rounded-full hover:opacity-75 ";
const logInButton = "text-white font-bold px-8 py-2 text-lg rounded-full hover:opacity-75";

const Navbar = () => {
  const navigate = useNavigate();  
  
  useEffect(() => {
    // Listen for OAuth messages from popup
    const handleMessage = (event) => {
      if (event.data.type === 'oauth-success') {
        console.log('OAuth successful:', event.data);
        // Store JWT token
        if (event.data.token) {
          localStorage.setItem('token', event.data.token);
        }
        // Navigate to tool page
        navigate("/tool");
      } else if (event.data.type === 'oauth-error') {
        console.error('OAuth error:', event.data.error);
        alert(`Authentication failed: ${event.data.error}`);
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, [navigate]);

  const handleGetStarted = async () => {
    try {
      // Get OAuth URL from backend
      const response = await axios.get(`${API_BASE_URL}/oauth/url`);
      const oauthUrl = response.data.oauth_url;
      
      // Open popup window
      const width = 500;
      const height = 600;
      const left = window.innerWidth / 2 - width / 2;
      const top = window.innerHeight / 2 - height / 2;

      const popup = window.open(
        oauthUrl,
        'GoogleSignIn',
        `width=${width},height=${height},top=${top},left=${left}`
      );

      // Optional: Check if popup was blocked
      if (!popup) {
        alert("Popup was blocked. Please allow popups for this site and try again.");
      }
    } catch (error) {
      console.error("Error getting OAuth URL:", error);
      alert("Something went wrong. Please try again.");
    }
  };

  return (
    <header className={banner}>
      <div className="flex items-center">
        <Link to="/">
          <img
            src="/finaldesignBG.png"
            alt="Bridger Logo"
            className={img}
            style={{ height: "70px", width: "auto" }}
          />
        </Link>
      </div>

      {/* Buttons on the right */}
      <div className="flex items-center gap-4">
        <Link to="/confirm"> 
          <button className={logInButton} style={{ backgroundColor: '#A3A3A3' }}>
            Learn More
          </button>
        </Link>
        <button 
          className={getStartedButton} 
          style={{ backgroundColor: '#0F689C' }} 
          onClick={handleGetStarted}
        >
          Get Started
        </button>
      </div>
    </header>
  );
};

export default Navbar;
