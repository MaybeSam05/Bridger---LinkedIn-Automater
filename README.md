# 🚀 LinkedIn Automater

An intelligent automation tool that helps you connect with LinkedIn professionals by generating personalized connection emails using AI. Built with Python, React, and GPT-4.

## ✨ Features

- 🔐 **Secure Authentication**: Uses OAuth2 for secure Gmail integration
- 🤖 **AI-Powered Emails**: Generates personalized connection requests using GPT-4
- 📸 **Profile Analysis**: Automatically captures and analyzes LinkedIn profiles
- 🎯 **Smart Matching**: Identifies genuine connection points between profiles
- 🌐 **Modern Web Interface**: Clean, responsive React frontend
- 🔄 **Real-time Processing**: Live updates on email generation and sending
- 📱 **Mobile Responsive**: Works seamlessly on all devices

## 🛠️ Tech Stack

### Backend

- FastAPI (Python web framework)
- Selenium (Web automation)
- EasyOCR (Optical Character Recognition)
- OpenAI GPT-4 (AI text generation)
- Gmail API (Email sending)

### Frontend

- React.js
- Tailwind CSS
- Axios (API calls)

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- Chrome Browser
- Gmail Account
- OpenAI API Key
- LinkedIn Account

## 🚀 Quick Start

### Backend Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/LinkedInAutomater.git
cd LinkedInAutomater
```

2. Create and activate virtual environment:

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
- Other configuration variables

5. Set up Gmail OAuth:

- Go to Google Cloud Console
- Create a new project
- Enable Gmail API
- Create OAuth 2.0 credentials
- Download credentials and save as `credentials.json` in project root

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd linkedin-automater-frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start development server:

```bash
npm start
```

## 🎮 Usage

1. Start the backend server:

```bash
uvicorn app:api --reload
```

2. Start the frontend (in a new terminal):

```bash
cd linkedin-automater-frontend
npm start
```

3. Open your browser to `http://localhost:3000`

4. First-time setup:

   - Log in to your LinkedIn account when prompted
   - Authenticate with Gmail
   - Your credentials will be saved for future use

5. To connect with someone:
   - Paste their LinkedIn profile URL
   - The tool will analyze both profiles
   - Review and send the generated email

## 🔒 Security

- No passwords are stored
- Uses secure OAuth2 for Gmail
- Cookies are stored locally
- API keys are environment variables
- All sensitive data is encrypted

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Google for Gmail API
- LinkedIn for inspiration
- All contributors and users

## ⚠️ Disclaimer

This tool is for educational purposes only. Please use responsibly and in accordance with LinkedIn's terms of service.
