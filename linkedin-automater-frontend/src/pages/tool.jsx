import React, { useState } from 'react';
import Header from '../components/Header';
import UserProfile from '../components/userProfile';
import ConnectionProfile from '../components/ConnectionProfile';
import ComposeEmail from '../components/ComposeEmail';
import EmailHistory from '../components/EmailHistory';

function Tool() {
  const [emailData, setEmailData] = useState(null); // holds { address, subject, body }

  const StepIndicator = ({ number, title }) => (
    <div className="flex items-center gap-3 mb-4">
      <div className="bg-[#0F689C] text-white rounded-full w-8 h-8 flex items-center justify-center font-semibold">
        {number}
      </div>
      <h2 className="text-xl font-semibold text-gray-800">{title}</h2>
    </div>
  );

  return (
    <div className="font-sans">
      <Header />
      <div className="font-sans bg-gray-50 min-h-screen p-6">
        <div className="max-w-4xl mx-auto space-y-8">
          <div>
            <StepIndicator number="1" title="Set Up Your Profile" />
            <UserProfile />
          </div>
          <div>
            <StepIndicator number="2" title="Find Your Connection" />
            <ConnectionProfile setEmailData={setEmailData} />
          </div>
          {emailData && (
            <div>
              <StepIndicator number="3" title="Send Your Connection Request" />
              <ComposeEmail
                address={emailData.address}
                subject={emailData.subject}
                body={emailData.body}
              />
            </div>
          )}
          <EmailHistory />
        </div>
      </div>
    </div>
  );
}

export default Tool;