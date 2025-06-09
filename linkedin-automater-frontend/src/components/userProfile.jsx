import React, { useState, useEffect } from "react";
import axios from "axios";

const UserProfile = () => {
  const [done, setDone] = useState(false);
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(false);

  // Check LinkedIn authentication status on component mount
  useEffect(() => {
    const checkUserStatus = async () => {
      try {
        const response = await axios.get("https://bridger.onrender.com/check_linkedin_status");
        setDone(response.data.has_linkedin_cookies);
      } catch (err) {
        console.error("Error checking LinkedIn status:", err);
        setError(true);
      }
    };

    checkUserStatus();
  }, []);

  const runScript = async () => {
    setLoading(true);
    setDone(false);
    setError(false);

    try {
      const response = await axios.post(
        "https://bridger.onrender.com/setup",
        {},
        { withCredentials: true } // Important: This enables cookie handling
      );

      if (response.data.status === "valid") {
        setDone(true);
      } else {
        setError(true);
      }
    } catch (err) {
      console.error("Backend error:", err);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  if (done) {
    return (
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow border">
        <h2 className="text-xl font-semibold mb-4">Your Profile</h2>
        <div className="bg-green-50 border border-green-200 rounded-md p-4 mb-4">
          <p className="text-green-700">✅ Profile setup complete!</p>
          <p className="text-sm text-green-600 mt-1">You can now search for connections.</p>
        </div>
        <div className="mt-4">
          <button
            onClick={() => setDone(false)}
            className="text-[#0F689C] hover:text-blue-700 underline text-sm"
          >
            Reset Profile or Update LinkedIn Cookies
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow border">
      <h2 className="text-xl font-semibold mb-4">Setup Your Profile</h2>
      <div className="space-y-4">
        <p className="text-gray-600">
          Click the button below to log in to LinkedIn. You'll be redirected to LinkedIn's login page.
          After logging in, your profile will be automatically set up.
        </p>
        <button
          onClick={runScript}
          disabled={loading}
          className={`w-full sm:w-auto bg-[#0F689C] text-white px-6 py-2 rounded-md font-medium transition ${
            loading ? "opacity-50 cursor-not-allowed" : "hover:bg-[#004182]"
          }`}
        >
          {loading ? "Setting up..." : "Login with LinkedIn"}
        </button>
        {error && (
          <p className="text-red-500">⚠️ Error setting up profile. Please try again.</p>
        )}
        <p className="text-xl">
          {loading
            ? "⏳ Setting up your profile..."
            : error
            ? "⚠️ Error!"
            : done
            ? "✅ Profile setup complete!"
            : "❌ Profile not set up yet."}
        </p>
      </div>
    </div>
  );
};

export default UserProfile;
