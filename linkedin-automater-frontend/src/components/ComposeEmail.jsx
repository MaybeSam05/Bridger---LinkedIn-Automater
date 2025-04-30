import React from "react";

const ComposeEmail = () => {
  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow border">
      <h2 className="text-xl font-semibold mb-6">Compose Email</h2>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">To:</label>
        <input
          type="email"
          placeholder="Recipient email"
          className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Subject:</label>
        <input
          type="text"
          placeholder="Email subject"
          className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium mb-1">Message:</label>
        <textarea
          placeholder="Write your message here..."
          rows="6"
          className="w-full border border-gray-300 rounded-md px-4 py-2 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>
      </div>

      <div className="flex justify-between items-center">

        <button className="bg-[#0F689C]  text-white px-4 py-2 rounded-md flex items-center gap-2 hover:bg-blue-700 transition">
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M22 2L11 13"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M22 2L15 22L11 13L2 9L22 2Z"
            />
          </svg>
          Send Email
        </button>
      </div>
    </div>
  );
};

export default ComposeEmail;
