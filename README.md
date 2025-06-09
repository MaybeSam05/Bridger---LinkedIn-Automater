# LinkedIn Automater

An automated system for LinkedIn networking and email outreach.

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

- Docker and Docker Compose
- OpenAI API Key
- LinkedIn Account

## Setup

1. Clone the repository:

```bash
git clone [your-repo-url]
cd LinkedInAutomater
```

2. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your actual values
```

3. Build and run with Docker:

```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.yml up -d
```

## Environment Variables

Required environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `LINKEDIN_USERNAME`: Your LinkedIn username
- `LINKEDIN_PASSWORD`: Your LinkedIn password

## Deployment

1. Ensure all environment variables are set
2. Build the Docker image:

```bash
docker build -t linkedin-automater .
```

3. Run the container:

```bash
docker run -d \
  --env-file .env \
  -p 8000:8000 \
  linkedin-automater
```

## Health Check

The application includes a health check endpoint at `/`. You can monitor the application's status using:

```bash
curl http://localhost:8000/
```

## Security Notes

- Never commit `.env` file with real credentials
- Keep your API keys secure
- Regularly update dependencies
- Monitor application logs for any suspicious activity

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
