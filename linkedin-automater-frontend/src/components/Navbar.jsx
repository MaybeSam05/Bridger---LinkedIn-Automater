import React from 'react';
//import { Link } from 'react-router-dom';

const banner = "py-4 px-6 md:px-12 flex justify-between items-center";
const img = "object-contain";
const getStartedButton = "text-white font-bold px-8 py-2 text-lg rounded-full hover:opacity-75 ";
const logInButton = "text-white font-bold px-8 py-2 text-lg rounded-full hover:opacity-75";

const Navbar = () => {
  return (
    <header className = { banner }>
      
      {/* Logo on the left */}
      <div className="flex items-center">

          <img
            src="/finaldesignBG.png"
            alt="Bridger Logo"
            className= { img } style={{ height: "70px", width: "auto" }}
          />
        
      </div>

      {/* Buttons on the right */}
      <div className="flex items-center gap-4">
        <button className= { logInButton } style = {{ backgroundColor: '#A3A3A3'}} >
          Log in
        </button>
        <button className= { getStartedButton } style={{ backgroundColor: '#0F689C' }}>
          Get Started Today!
        </button>
      </div>

    </header>
  );
};

export default Navbar;
