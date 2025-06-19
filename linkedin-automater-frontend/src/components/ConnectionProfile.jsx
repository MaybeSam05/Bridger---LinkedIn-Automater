import React, { useState } from "react";
import axios from "axios";

const MAX_CONTEXT_LENGTH = 150;

const ConnectionProfile = ({ setEmailData }) => {
  const [clientURL, setClientUrl] = useState("");
  const [context, setContext] = useState("");
  const [done, setDone] = useState(false);
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);

  const handleContextChange = (e) => {
    const input = e.target.value;
    if (input.length <= MAX_CONTEXT_LENGTH) {
      setContext(input);
    }
  };

  const handleRunClick = () => {
    if (!clientURL.trim()) {
      setError(true);
      return;
    }
    setShowConfirmation(true);
  };

  const runScript = async () => {
    setLoading(true);
    setDone(false);
    setError(false);
    setShowConfirmation(false);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post("https://linkedin-automater-production.up.railway.app/find_connection", {
        link: clientURL,
        additional_context: context
      }, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.data.status === "valid") {
        setEmailData({
          address: response.data.address,
          subject: response.data.subject,
          body: response.data.body,
        });
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
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow border relative">
      {loading && (
        <div className="absolute inset-0 bg-white/80 flex items-center justify-center z-10">
          <div className="flex flex-col items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#0F689C]"></div>
            <p className="text-lg font-medium text-gray-700 mt-4">Analyzing profiles and generating email...</p>
            <p className="text-sm text-gray-500 mt-2">This may take a few moments</p>
          </div>
        </div>
      )}

      <h2 className="text-xl font-semibold mb-4">Find a Connection</h2>
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative group">
            <input
              type="text"
              value={clientURL}
              onChange={(e) => setClientUrl(e.target.value)}
              placeholder="Enter Connection's LinkedIn Profile URL"
              className={`w-full border ${error && !clientURL.trim() ? 'border-red-500' : 'border-gray-300'} rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500`}
            />
            <div className="invisible group-hover:visible absolute -top-10 left-0 bg-gray-800 text-white text-sm px-2 py-1 rounded whitespace-nowrap">
              Paste the full LinkedIn profile URL of the person you want to connect with
            </div>
          </div>
          <button
            onClick={handleRunClick}
            disabled={loading}
            className={`bg-[#0F689C] text-white px-6 py-2 rounded-md font-medium transition ${
              loading ? "opacity-50 cursor-not-allowed" : "hover:bg-[#004182]"
            }`}
          >
            {loading ? "Running..." : "Submit"}
          </button>
        </div>

        <div className="mt-4">
          <label htmlFor="context" className="block text-sm font-medium text-gray-700 mb-2 relative group">
            Additional Context (Optional)
            <div className="invisible group-hover:visible absolute -top-10 left-0 bg-gray-800 text-white text-sm px-2 py-1 rounded whitespace-nowrap z-10">
              Add any relevant information about how you know this person or why you want to connect
            </div>
          </label>
          <div className="relative">
            <textarea
              id="context"
              value={context}
              onChange={handleContextChange}
              placeholder="Add any additional context you'd like to include in the email (e.g., where you met them, mutual connections, shared interests)"
              className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 h-24 resize-none"
              maxLength={MAX_CONTEXT_LENGTH}
            />
            <div className="absolute bottom-2 right-2 text-sm text-gray-500">
              {context.length}/{MAX_CONTEXT_LENGTH}
            </div>
          </div>
        </div>
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

      {showConfirmation && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg max-w-md">
            <h3 className="text-lg font-semibold mb-4">Confirm Action</h3>
            <p className="text-gray-600 mb-6">
              Are you sure you want to analyze this profile and generate an email? This process will:
              <ul className="list-disc ml-6 mt-2">
                <li>Scan the LinkedIn profile</li>
                <li>Generate a personalized email</li>
                <li>Prepare a connection request</li>
              </ul>
            </p>
            <div className="flex justify-end gap-4">
              <button
                onClick={() => setShowConfirmation(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Cancel
              </button>
              <button
                onClick={runScript}
                className="bg-[#0F689C] text-white px-4 py-2 rounded hover:bg-[#004182]"
              >
                Proceed
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ConnectionProfile;
