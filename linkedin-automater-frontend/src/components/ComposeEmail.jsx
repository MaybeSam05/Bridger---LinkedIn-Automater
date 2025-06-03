import React, { useState, useEffect } from "react";
import axios from "axios";

const ComposeEmail = ({ address, subject, body }) => {
  const [editedAddress, setEditedAddress] = useState(address || "");
  const [editedSubject, setEditedSubject] = useState(subject || "");
  const [editedBody, setEditedBody] = useState(body || "");
  const [isSending, setIsSending] = useState(false);
  const [sendStatus, setSendStatus] = useState(null);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    setEditedAddress(address || "");
    setEditedSubject(subject || "");
    setEditedBody(body || "");
  }, [address, subject, body]);

  const validateForm = () => {
    const errors = {};
    if (!editedAddress.trim()) errors.address = "Email address is required";
    if (!editedSubject.trim()) errors.subject = "Subject is required";
    if (!editedBody.trim()) errors.body = "Message body is required";
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSendClick = () => {
    if (validateForm()) {
      setShowConfirmation(true);
    }
  };

  const handleSendEmail = async () => {
    setIsSending(true);
    setSendStatus(null);
    setShowConfirmation(false);
    
    try {
      await axios.post("http://127.0.0.1:8000/send_email", {
        address: editedAddress,
        subject: editedSubject,
        body: editedBody
      });
      
      setSendStatus('success');
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
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow border relative">
      {isSending && (
        <div className="absolute inset-0 bg-white/80 flex items-center justify-center z-10">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#0F689C] mb-4"></div>
            <p className="text-lg font-medium text-gray-700">Sending your email...</p>
            <p className="text-sm text-gray-500 mt-2">Please wait</p>
          </div>
        </div>
      )}

      <h2 className="text-xl font-semibold mb-6">Compose Email</h2>

      <div className="mb-4 relative group">
        <label className="block text-sm font-medium mb-1">
          To:
          <div className="invisible group-hover:visible absolute -top-10 left-0 bg-gray-800 text-white text-sm px-2 py-1 rounded whitespace-nowrap z-10">
            The email address of your connection
          </div>
        </label>
        <input
          type="email"
          value={editedAddress}
          onChange={(e) => setEditedAddress(e.target.value)}
          className={`w-full border ${formErrors.address ? 'border-red-500' : 'border-gray-300'} rounded-md px-4 py-2`}
        />
        {formErrors.address && (
          <p className="text-red-500 text-sm mt-1">{formErrors.address}</p>
        )}
      </div>

      <div className="mb-4 relative group">
        <label className="block text-sm font-medium mb-1">
          Subject:
          <div className="invisible group-hover:visible absolute -top-10 left-0 bg-gray-800 text-white text-sm px-2 py-1 rounded whitespace-nowrap z-10">
            A clear and professional subject line
          </div>
        </label>
        <input
          type="text"
          value={editedSubject}
          onChange={(e) => setEditedSubject(e.target.value)}
          className={`w-full border ${formErrors.subject ? 'border-red-500' : 'border-gray-300'} rounded-md px-4 py-2`}
        />
        {formErrors.subject && (
          <p className="text-red-500 text-sm mt-1">{formErrors.subject}</p>
        )}
      </div>

      <div className="mb-6 relative group">
        <label className="block text-sm font-medium mb-1">
          Message:
          <div className="invisible group-hover:visible absolute -top-10 left-0 bg-gray-800 text-white text-sm px-2 py-1 rounded whitespace-nowrap z-10">
            Your personalized connection message
          </div>
        </label>
        <textarea
          rows="6"
          value={editedBody}
          onChange={(e) => setEditedBody(e.target.value)}
          className={`w-full border ${formErrors.body ? 'border-red-500' : 'border-gray-300'} rounded-md px-4 py-2 resize-none`}
        />
        {formErrors.body && (
          <p className="text-red-500 text-sm mt-1">{formErrors.body}</p>
        )}
      </div>

      {sendStatus === 'success' && (
        <div className="mb-4 p-3 bg-green-50 text-green-600 rounded-md flex items-center">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
          </svg>
          Email sent successfully!
        </div>
      )}
      
      {sendStatus === 'error' && (
        <div className="mb-4 p-3 bg-red-50 text-red-600 rounded-md flex items-center">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          Failed to send email. Please try again.
        </div>
      )}

      <button 
        onClick={handleSendClick}
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

      {showConfirmation && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg max-w-md">
            <h3 className="text-lg font-semibold mb-4">Confirm Send Email</h3>
            <p className="text-gray-600 mb-6">
              Are you sure you want to send this connection request email? Please verify:
              <ul className="list-disc ml-6 mt-2">
                <li>The email address is correct</li>
                <li>The subject line is professional</li>
                <li>The message is personalized and error-free</li>
              </ul>
            </p>
            <div className="flex justify-end gap-4">
              <button
                onClick={() => setShowConfirmation(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Review Again
              </button>
              <button
                onClick={handleSendEmail}
                className="bg-[#0F689C] text-white px-4 py-2 rounded hover:bg-[#004182]"
              >
                Send Email
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ComposeEmail;
