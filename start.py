#!/usr/bin/env python3
"""
Startup script for the LinkedIn Automater application
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        "SQLALCHEMY_DATABASE_URL",
        "SECRET_KEY",
        "OPENAI_API_KEY",
        "USERNAME",
        "PASSWORD"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All required environment variables are set")
    return True

def test_database():
    """Test database connection"""
    try:
        from database import engine
        from sqlalchemy import text
        
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main startup function"""
    print("🚀 Starting LinkedIn Automater...")
    
    # Check environment variables
    if not check_environment():
        sys.exit(1)
    
    # Test database connection
    if not test_database():
        sys.exit(1)
    
    # Import and start the application
    try:
        import uvicorn
        from main import app
        
        print("✅ Application ready to start")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()