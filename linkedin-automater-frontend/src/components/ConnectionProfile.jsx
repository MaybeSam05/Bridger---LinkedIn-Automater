import React from "react";


const ConnectionProfile = () => {

    return (
        <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow border">
      <h2 className="text-xl font-semibold mb-4">Find a Connection</h2>
      <div className="flex flex-col sm:flex-row gap-4">
        <input
          type="text"
          placeholder="Enter Connection's LinkedIn Profile URL"
          className="flex-1 border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          className="bg-[#0F689C] hover:bg-[#004182] text-white px-6 py-2 rounded-md font-medium transition"
        >
          Go
        </button>
      </div>
    </div>
    );
};


export default ConnectionProfile;