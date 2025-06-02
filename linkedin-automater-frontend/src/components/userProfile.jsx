import React, { useState, useEffect } from "react";
import axios from "axios";

const UserProfile = () => {
  const [profileURL, setProfileURL] = useState("");
  const [done, setDone] = useState(false);
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(false);
  const [userId, setUserId] = useState(null);
  const [sessionId, setSessionId] = useState(null);

  // Check for existing session on component mount
  useEffect(() => {
    const savedUserId = localStorage.getItem('userId');
    const savedSessionId = localStorage.getItem('sessionId');
    if (savedUserId && savedSessionId) {
      setUserId(savedUserId);
      setSessionId(savedSessionId);
      setDone(true);
    }
  }, []);

  const runScript = async () => {
    setLoading(true);
    setDone(false);
    setError(false);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/setup",
        { link: profileURL },
        { withCredentials: true } // Important: This enables cookie handling
      );

      if (response.data.status === "valid") {
        // Save user and session IDs
        localStorage.setItem('userId', response.data.user_id);
        localStorage.setItem('sessionId', response.data.session_id);
        setUserId(response.data.user_id);
        setSessionId(response.data.session_id);
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

  if (done && userId && sessionId) {
    return (
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow border">
        <h2 className="text-xl font-semibold mb-4">Your Profile</h2>
        <div className="bg-green-50 border border-green-200 rounded-md p-4">
          <p className="text-green-700">✅ Profile setup complete!</p>
          <p className="text-sm text-green-600 mt-1">You can now search for connections.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow border">
      <h2 className="text-xl font-semibold mb-4">Setup Your Profile</h2>
      <div className="flex flex-col sm:flex-row gap-4">
        <input
          type="text"
          value={profileURL}
          onChange={(e) => setProfileURL(e.target.value)}
          placeholder="Enter Your LinkedIn Profile URL"
          className="flex-1 border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={runScript}
          disabled={loading}
          className={`bg-[#0F689C] text-white px-6 py-2 rounded-md font-medium transition ${
            loading ? "opacity-50 cursor-not-allowed" : "hover:bg-[#004182]"
          }`}
        >
          {loading ? "Setting up..." : "Get Started"}
        </button>
      </div>
      {error && (
        <p className="text-red-500 mt-2">⚠️ Error setting up profile. Please try again.</p>
      )}
      <p className="text-xl mt-6">
        {loading
          ? "⏳ Setting up your profile..."
          : error
          ? "⚠️ Error!"
          : done
          ? "✅ Profile setup complete!"
          : "❌ Profile not set up yet."}
      </p>
    </div>
  );
};

export default UserProfile;
