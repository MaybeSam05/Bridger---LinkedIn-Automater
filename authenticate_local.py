#!/usr/bin/env python3
"""
Local Gmail authentication script
Run this locally to generate token.json for deployment
"""
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load environment variables
load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

def authenticate_gmail_local():
    """Authenticate Gmail locally and save token"""
    creds = None
    
    # Check if token file exists
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            print("✅ Loaded existing credentials from token.json")
        except Exception as e:
            print(f"⚠️  Error loading existing credentials: {e}")
            creds = None

    # Check if credentials are valid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("✅ Token refreshed silently.")
            except Exception as e:
                print(f"❌ Error refreshing token: {e}")
                creds = None
        
        # If no valid credentials, start OAuth flow
        if not creds:
            try:
                if not os.path.exists('c.json'):
                    print("❌ Gmail credentials file 'c.json' not found")
                    print("💡 Please download your Gmail API credentials and save as 'c.json'")
                    return False
                
                print("🔐 Starting Gmail OAuth flow...")
                print("📱 A browser window will open for authentication")
                flow = InstalledAppFlow.from_client_secrets_file('c.json', SCOPES)
                creds = flow.run_local_server(port=0)
                print("✅ OAuth authentication completed successfully!")
                
                # Save the credentials
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
                print("✅ Token saved to token.json")
                    
            except Exception as e:
                print(f"❌ Error during OAuth flow: {e}")
                return False

    # Test the credentials
    try:
        service = build('gmail', 'v1', credentials=creds)
        oauth2_service = build('oauth2', 'v2', credentials=creds)
        user_info = oauth2_service.userinfo().get().execute()
        user_email = user_info.get('email')
        print(f"✅ Authentication successful for: {user_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to verify credentials: {e}")
        return False

def main():
    """Main function"""
    print("🔐 Gmail Local Authentication")
    print("=" * 40)
    print("This script will authenticate with Gmail and save the token for deployment.")
    print("Make sure you have 'c.json' (Gmail API credentials) in the current directory.")
    print()
    
    if authenticate_gmail_local():
        print("\n✅ Authentication completed successfully!")
        print("📁 token.json has been created/updated")
        print("🚀 You can now deploy to Railway with this token")
    else:
        print("\n❌ Authentication failed")
        print("💡 Please check your credentials and try again")

if __name__ == "__main__":
    main() 