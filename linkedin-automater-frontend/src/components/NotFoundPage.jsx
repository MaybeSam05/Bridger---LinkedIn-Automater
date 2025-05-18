import React from "react";
import { Link } from "react-router-dom";

const NotFoundPage = () => {
  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow border text-center mt-20">
      <div className="flex justify-center mb-4">
        <svg
          className="w-16 h-16 text-red-500"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.054 0 1.918-.816 1.994-1.851l.878-10.536A2 2 0 0019.807 4H4.193a2 2 0 00-1.993 2.613l.878 10.536A2 2 0 004.07 19z"
          />
        </svg>
      </div>
      <h2 className="text-2xl font-semibold mb-2">404 - Page Not Found</h2>
      <p className="text-gray-600 mb-6">
        The page you’re looking for doesn’t exist or has been moved.
      </p>
      <Link to="/">
        <button className="bg-[#0F689C] text-white px-4 py-2 rounded-md hover:bg-gray-800 transition">
          <span className="text-lg">←</span> Go Home
        </button>
      </Link>
    </div>
  );
};

export default NotFoundPage;
