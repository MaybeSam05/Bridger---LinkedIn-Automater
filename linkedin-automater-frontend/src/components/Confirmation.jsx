import React from "react";
import { Link } from "react-router-dom";

const EmailSentConfirmation = () => {
  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow border text-center">
      <div className="flex justify-center mb-4">
        <svg
          className="w-16 h-16 text-green-500"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M9 12l2 2l4 -4"
          />
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2S2 6.477 2 12s4.477 10 10 10z"
          />
        </svg>
      </div>
      <h2 className="text-2xl font-semibold mb-2">Email Sent Successfully!</h2>
      <p className="text-gray-600 mb-6">
        Your message has been delivered. Check your outbox for confirmation.
      </p>
      <Link to="/tool">
        <button className="bg-[#0F689C] text-white px-4 py-2 rounded-md hover:bg-gray-800 transition">
          <span className="text-lg">+</span> New Connect
        </button>
        </Link>
    </div>
  );
};

export default EmailSentConfirmation;
