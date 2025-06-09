import React from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const conversations = "text-4xl md:text-5xl font-bold text-slate-700 mb-4";
const outreach = "text-slate-600 ";
const easy = "text-4xl md:text-5xl font-bold mb-6";

const Hero = () => {
  const navigate = useNavigate();

  const handleGetStarted = async () => {
    try {
      // First authenticate with Gmail
      const gmailResponse = await axios.post("https://bridger.onrender.com/authenticate_gmail");
      
      if (gmailResponse.data.status === "authenticated") {
        // After Gmail auth, navigate to the tool page
        navigate("/tool");
      }
    } catch (error) {
      console.error("Authentication error:", error);
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
              src="/laptopzoomBG.png"
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
