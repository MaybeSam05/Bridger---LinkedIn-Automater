# Bridger

A professional networking tool that helps you build meaningful connections on LinkedIn by automating personalized connection requests.

## Features

- OAuth integration with Gmail for secure email sending
- LinkedIn profile analysis using OCR technology
- AI-powered personalized email generation
- Modern React frontend with Tailwind CSS
- FastAPI backend with rate limiting and CORS security
- SQLAlchemy database integration
- Real-time profile processing
- Email history tracking

## Prerequisites

- Python 3.8+
- Node.js 14+
- Gmail API credentials
- OpenAI API key

## Installation

### Backend Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/LinkedInAutomater.git
cd LinkedInAutomater
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
```

Edit `.env` and add your:

- OpenAI API key
- Gmail API credentials
- Database configuration

5. Initialize the database:

```bash
python init_db.py
```

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd linkedin-automater-frontend
```

2. Install dependencies:

```bash
npm install
```

## Running the Application

1. Start the backend server:

```bash
uvicorn app:api --reload
```

2. Start the frontend development server:

```bash
cd linkedin-automater-frontend
npm start
```

3. Access the application at `http://localhost:3000`

## Usage

1. Log in with your Gmail account
2. Set up your LinkedIn profile
3. Enter the LinkedIn profile URL of someone you'd like to connect with
4. Add any additional context about your connection
5. Review and send the generated email

## Security Features

- Rate limiting on all endpoints
- CORS protection
- OAuth 2.0 authentication
- Secure cookie handling
- Input validation
- Error handling

## API Endpoints

- `POST /authenticate_gmail`: Gmail authentication
- `POST /setup`: LinkedIn profile setup
- `POST /find_connection`: Process connection's profile
- `POST /send_email`: Send connection request email
- `GET /email_history`: View sent emails
- `GET /check_linkedin_status`: Check LinkedIn authentication status

## Rate Limits

- Authentication endpoints: 5 requests per 5 minutes
- Profile analysis: 10 requests per 5 minutes
- Email sending: 10 requests per 5 minutes
- Read-only endpoints: 30 requests per minute

## Acknowledgments

- OpenAI for GPT API
- EasyOCR for text extraction
- FastAPI framework
- React and Tailwind CSS
- Gmail API
