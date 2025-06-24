# LinkedIn Automater

An intelligent LinkedIn networking automation tool that helps you build meaningful professional connections through AI-powered personalized email outreach.

## 🚀 Features

- **Smart Profile Analysis**: Automatically extracts and analyzes LinkedIn profiles using advanced web scraping
- **AI-Powered Email Generation**: Creates personalized, context-aware emails using GPT-4 for genuine connections
- **Gmail OAuth Integration**: Secure email sending through Gmail API with OAuth 2.0 authentication
- **Modern Web Interface**: Beautiful React frontend with Tailwind CSS for seamless user experience
- **Rate Limiting & Security**: Built-in protection against abuse with comprehensive rate limiting
- **Email History Tracking**: Keep track of all your outreach emails and their status
- **Real-time Processing**: Instant profile analysis and email generation
- **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux

## 🛠️ Technology Stack

### Backend

- **FastAPI**: High-performance Python web framework
- **Playwright**: Advanced web automation for LinkedIn profile extraction
- **OpenAI GPT-4**: AI-powered email generation
- **SQLAlchemy**: Database ORM with PostgreSQL
- **Gmail API**: Secure email sending
- **JWT**: Stateless authentication
- **Pydoll**: Modern browser automation

### Frontend

- **React 19**: Latest React with modern hooks and features
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API communication
- **React Router**: Client-side routing
- **Lucide React**: Beautiful icon library

### Infrastructure

- **PostgreSQL**: Reliable database storage
- **Docker**: Containerized deployment
- **Rate Limiting**: Built-in protection against abuse
- **CORS**: Cross-origin resource sharing support

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL database
- Google Cloud Platform account (for Gmail API)
- OpenAI API key
- LinkedIn account

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/LinkedInAutomater.git
cd LinkedInAutomater
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your actual values
```

### 3. Frontend Setup

```bash
cd linkedin-automater-frontend
npm install
```

### 4. Database Setup

```bash
# Create PostgreSQL database
createdb linkedin_automater

# Run database migrations
python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
```

### 5. Environment Variables

Create a `.env` file in the root directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# LinkedIn Credentials
USERNAME=your_linkedin_email
PASSWORD=your_linkedin_password

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
REDIRECT_URI=https://yourdomain.com/oauth/callback

# Database
DATABASE_URL=postgresql://username:password@localhost/linkedin_automater

# Security
SECRET_KEY=your_secret_key_for_jwt
```

### 6. Run the Application

```bash
# Terminal 1: Start the backend
python app.py

# Terminal 2: Start the frontend
cd linkedin-automater-frontend
npm start
```

Visit `http://localhost:3000` to access the application.

## 🔧 Configuration

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Add your redirect URI to authorized redirect URIs
6. Download the credentials and update your `.env` file

### OpenAI API Setup

1. Sign up at [OpenAI](https://openai.com/)
2. Generate an API key
3. Add the key to your `.env` file

## 📖 Usage

1. **Authentication**: Log in with your Gmail account using OAuth
2. **Profile Setup**: Enter your LinkedIn profile URL to set up your profile
3. **Find Connections**: Enter the LinkedIn URL of someone you want to connect with
4. **Add Context**: Provide any additional context about your connection
5. **Review & Send**: Review the AI-generated email and send it

## 🔒 Security Features

- **OAuth 2.0 Authentication**: Secure Gmail integration
- **JWT Tokens**: Stateless authentication
- **Rate Limiting**: Protection against abuse
- **CORS Protection**: Secure cross-origin requests
- **Input Validation**: Comprehensive data validation
- **Error Handling**: Graceful error management
- **Secure Headers**: Security-focused HTTP headers

## 📊 API Endpoints

| Endpoint                 | Method | Description                                     |
| ------------------------ | ------ | ----------------------------------------------- |
| `/authenticate_gmail`    | POST   | Gmail OAuth authentication                      |
| `/setup`                 | POST   | Set up user's LinkedIn profile                  |
| `/find_connection`       | POST   | Analyze connection's profile and generate email |
| `/send_email`            | POST   | Send connection request email                   |
| `/email_history`         | GET    | View sent email history                         |
| `/check_linkedin_status` | GET    | Check LinkedIn authentication status            |
| `/oauth/url`             | GET    | Get Google OAuth URL                            |
| `/oauth/callback`        | GET    | Handle OAuth callback                           |

## 🚦 Rate Limits

- **Authentication**: 5 requests per 5 minutes
- **Profile Analysis**: 10 requests per 5 minutes
- **Email Sending**: 10 requests per 5 minutes
- **Read Operations**: 30 requests per minute

## 🐳 Docker Deployment

### Development

```bash
docker-compose up --build
```

### Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 🧪 Testing

```bash
# Backend tests
python -m pytest

# Frontend tests
cd linkedin-automater-frontend
npm test
```

## 📈 Monitoring

The application includes health check endpoints:

```bash
curl http://localhost:8000/health
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 API
- **Playwright** for web automation
- **FastAPI** for the backend framework
- **React** and **Tailwind CSS** for the frontend
- **Gmail API** for email functionality

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/LinkedInAutomater/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

## ⚠️ Disclaimer

This tool is designed for legitimate networking purposes. Please ensure you comply with LinkedIn's Terms of Service and use the tool responsibly. The developers are not responsible for any misuse of this application.
