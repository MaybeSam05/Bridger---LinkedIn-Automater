import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <header className="bg-white py-4 px-6 md:px-12 flex justify-between items-center shadow-sm">
      <div className="flex items-center">
        <Link to="/">
          <img
            src="/your-logo-path.png"
            alt="Bridger Logo"
            className="h-12 w-auto object-contain"
          />
        </Link>
      </div>

      <div className="flex items-center gap-4">
        <button className="bg-gray-400 text-white hover:bg-gray-500 border-0 px-8 py-2 text-lg rounded">
          Log in
        </button>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-2 text-lg rounded">
          Get Started Today!
        </button>
      </div>
    </header>
  );
};

export default Navbar;
