import React from 'react';
import Header from '../components/Header';
import UserProfile from '../components/userProfile';
import ConnectionProfile from '../components/ConnectionProfile';
import ComposeEmail from '../components/ComposeEmail';

function Tool() {
    return (
        <div className="font-sans">
      <Header/>
      <div className="font-sans bg-gray-50 min-h-screen p-6">
      <div className="max-w-4xl mx-auto space-y-8">
        <UserProfile />
        <ConnectionProfile />
        <ComposeEmail />
      </div>
    </div>
    </div>
    );
};

export default Tool;