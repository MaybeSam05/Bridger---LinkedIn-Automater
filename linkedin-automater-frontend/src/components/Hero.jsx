import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { API_BASE_URL } from "../config";

const conversations = "text-4xl md:text-5xl font-bold text-slate-700 mb-4";
const outreach = "text-slate-600 ";
const easy = "text-4xl md:text-5xl font-bold mb-6";

const Hero = () => {
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
    <section className="bg-gradient-to-b from-gray-300 to-white py-16 md:py-24">
      <div className="container mx-auto px-6 md:px-12 flex flex-col lg:flex-row items-center justify-between">
        
        {/* Left Side Text */}
        <div className="lg:w-1/2 lg:mr-12 mb-12 lg:mb-0">
          <h1 className={conversations} style={{ color: "#2C3E50" }}>
            More conversations,<br />
            <span className={outreach} style={{ color: "#2C3E50" }}>less outreach.</span>
          </h1><br />
          <h2 className={easy} style={{ color: "#0F689C" }}>
            Bridger makes it easy.
          </h2>
          
          {/* Get Started Button */}
          <button
            onClick={handleGetStarted}
            className="bg-[#0F689C] text-white px-8 py-3 rounded-md font-medium text-lg hover:bg-[#004182] transition-colors duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
          >
            Get Started Today
          </button>
        </div>

        {/* Right Side Image */}
        <div className="lg:w-1/2">
          <div className="relative">
            <img
              src="/editedGIF.gif"
              alt="Laptop Mockup"
              className="w-full h-auto object-contain rounded-lg"
            />
          </div>
        </div>

      </div>
    </section>
  );
};

export default Hero;
