import React, { useState, useEffect } from "react";
import axios from "axios";

const ComposeEmail = ({ address, subject, body }) => {
  const [editedAddress, setEditedAddress] = useState(address || "");
  const [editedSubject, setEditedSubject] = useState(subject || "");
  const [editedBody, setEditedBody] = useState(body || "");
  const [isSending, setIsSending] = useState(false);
  const [sendStatus, setSendStatus] = useState(null); // 'success' or 'error'

  // Update state when props change
  useEffect(() => {
    setEditedAddress(address || "");
    setEditedSubject(subject || "");
    setEditedBody(body || "");
  }, [address, subject, body]);

  const handleSendEmail = async () => {
    setIsSending(true);
    setSendStatus(null);
    
    try {
      await axios.post("http://127.0.0.1:8000/send_email", {
        address: editedAddress,
        subject: editedSubject,
        body: editedBody
      });
      
      setSendStatus('success');
      // Clear the fields after successful send
      setEditedAddress("");
      setEditedSubject("");
      setEditedBody("");
    } catch (error) {
      console.error("Failed to send email:", error);
      setSendStatus('error');
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow border">
      <h2 className="text-xl font-semibold mb-6">Compose Email</h2>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">To:</label>
        <input
          type="email"
          value={editedAddress}
          onChange={(e) => setEditedAddress(e.target.value)}
          className="w-full border border-gray-300 rounded-md px-4 py-2"
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Subject:</label>
        <input
          type="text"
          value={editedSubject}
          onChange={(e) => setEditedSubject(e.target.value)}
          className="w-full border border-gray-300 rounded-md px-4 py-2"
        />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium mb-1">Message:</label>
        <textarea
          rows="6"
          value={editedBody}
          onChange={(e) => setEditedBody(e.target.value)}
          className="w-full border border-gray-300 rounded-md px-4 py-2 resize-none"
        />
      </div>

      {sendStatus === 'success' && (
        <div className="mb-4 text-green-600">✅ Email sent successfully!</div>
      )}
      
      {sendStatus === 'error' && (
        <div className="mb-4 text-red-600">❌ Failed to send email. Please try again.</div>
      )}

      <button 
        onClick={handleSendEmail}
        disabled={isSending}
        className={`bg-[#0F689C] text-white px-4 py-2 rounded-md flex items-center gap-2 hover:bg-blue-700 transition ${isSending ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
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
        {isSending ? 'Sending...' : 'Send Email'}
      </button>
    </div>
  );
};

export default ComposeEmail;
