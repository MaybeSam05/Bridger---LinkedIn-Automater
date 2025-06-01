import React, { useState } from "react";
import axios from "axios";

const UserProfile = () => {
  const [profileUrl, setProfileUrl] = useState("");
  const [done, setDone] = useState(false);
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(false);

  const runScript = async () => {
    setLoading(true);
    setDone(false);
    setError(false);

    try {
      const response = await axios.post("http://127.0.0.1:8000/setup", {
        link: profileUrl
      });

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

  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow border">
      <h2 className="text-xl font-semibold mb-4">Set Up Your LinkedIn Profile</h2>

      <div className="flex flex-col sm:flex-row gap-4">
        <input
          type="text"
          value={profileUrl}
          onChange={(e) => setProfileUrl(e.target.value)}
          placeholder="Enter your LinkedIn profile URL"
          className="flex-1 border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
          onClick={runScript}
          disabled={loading}
          className={`bg-[#0F689C] text-white px-6 py-2 rounded-md font-medium transition ${
            loading ? "opacity-50 cursor-not-allowed" : "hover:bg-[#004182]"
          }`}
        >
          {loading ? "Running..." : "Run Script"}
        </button>
      </div>

      <p className="text-xl mt-6">
        {loading
          ? "⏳ Running script..."
          : error
          ? "⚠️ Error!"
          : done
          ? "✅ Task complete!"
          : "❌ Task not done yet."}
      </p>
    </div>
  );
};

export default UserProfile;
