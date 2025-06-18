import React from "react";
import { Link } from "react-router-dom";

const LearnMore = () => {
  return (
    <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow border">
      <div className="flex items-center mb-8">
        <svg
          className="w-12 h-12 text-[#0F689C] mr-4"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <h1 className="text-3xl font-bold text-gray-800">About Bridger</h1>
      </div>

      <div className="space-y-6">
        <section>
          <h2 className="text-2xl font-semibold mb-3 text-[#0F689C]">What is Bridger?</h2>
          <p className="text-gray-700 leading-relaxed">
            Bridger is an intelligent networking tool that helps you build meaningful professional connections. 
            Using AI technology, it analyzes LinkedIn profiles and generates personalized connection requests 
            that highlight genuine common ground between professionals.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3 text-[#0F689C]">How It Works</h2>
          <div className="space-y-4">
            <div className="flex items-start">
              <span className="bg-[#0F689C] text-white rounded-full w-8 h-8 flex items-center justify-center mr-3 mt-1">1</span>
              <p className="text-gray-700">Log in with your Gmail accounts</p>
            </div>
            <div className="flex items-start">
              <span className="bg-[#0F689C] text-white rounded-full w-8 h-8 flex items-center justify-center mr-3 mt-1">2</span>
              <p className="text-gray-700">Paste your LinkedIn profile URL</p>
            </div>
            <div className="flex items-start">
              <span className="bg-[#0F689C] text-white rounded-full w-8 h-8 flex items-center justify-center mr-3 mt-1">3</span>
              <p className="text-gray-700">Paste the LinkedIn profile URL of someone you'd like to connect with</p>
            </div>
            <div className="flex items-start">
              <span className="bg-[#0F689C] text-white rounded-full w-8 h-8 flex items-center justify-center mr-3 mt-1">4</span>
              <p className="text-gray-700">Bridger analyzes both profiles and identifies meaningful connections</p>
            </div>
            <div className="flex items-start">
              <span className="bg-[#0F689C] text-white rounded-full w-8 h-8 flex items-center justify-center mr-3 mt-1">5</span>
              <p className="text-gray-700">Review and send the personalized connection email</p>
            </div>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3 text-[#0F689C]">Key Features</h2>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <li className="flex items-center space-x-2">
              <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
              </svg>
              <span>AI-Powered Profile Analysis</span>
            </li>
            <li className="flex items-center space-x-2">
              <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
              </svg>
              <span>Personalized Email Generation</span>
            </li>
            <li className="flex items-center space-x-2">
              <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
              </svg>
              <span>Secure OAuth Integration</span>
            </li>
            <li className="flex items-center space-x-2">
              <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
              </svg>
              <span>Real-time Processing</span>
            </li>
          </ul>
        </section>

        <section className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-2xl font-semibold mb-3 text-[#0F689C]">Ready to Start?</h2>
          <p className="text-gray-700 mb-4">
            Begin building meaningful professional connections with Bridger today.
          </p>
          <Link to="/">
            <button className="bg-[#0F689C] text-white px-6 py-3 rounded-md hover:bg-blue-700 transition flex items-center space-x-2">
              <span>Start Connecting</span>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </button>
          </Link>
        </section>
      </div>
    </div>
  );
};

export default LearnMore;
