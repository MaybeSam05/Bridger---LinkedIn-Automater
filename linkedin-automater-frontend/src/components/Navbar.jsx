import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const banner = "py-4 px-6 md:px-12 flex justify-between items-center";
const img = "object-contain";
const getStartedButton = "text-white font-bold px-8 py-2 text-lg rounded-full hover:opacity-75 ";
const logInButton = "text-white font-bold px-8 py-2 text-lg rounded-full hover:opacity-75";

const Navbar = () => {
  const navigate = useNavigate();  
  
  const handleGetStarted = async () => {
    try {
      // First authenticate with Gmail
      const res = await axios.post("http://127.0.0.1:8000/authenticate_gmail");
      console.log("Gmail authentication response:", res);
      
      if (res.data.status === "authenticated") {
        // After successful Gmail authentication, navigate to the tool page
        navigate("/tool");
      } else {
        console.error("Gmail authentication failed");
        alert("Failed to authenticate with Gmail. Please try again.");
      }
    } catch (error) {
      console.error("Authentication error:", error);
      alert("Something went wrong during authentication. Please try again.");
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
