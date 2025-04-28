import React from 'react';

function Login() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-blue-600 mb-6">Welcome to LinkedIn Automater</h1>
        <button className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg shadow-md transition">
          Connect with Google
        </button>
      </div>
    </div>
  );
}

export default Login;
