# LinkedIn Automater - Docker Deployment Guide

This guide explains how to deploy the LinkedIn Automater application using Docker and Docker Compose.

## Prerequisites

- Docker and Docker Compose installed
- PostgreSQL database (included in docker-compose)
- Required API keys and credentials

## Required Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# OpenAI API Key for email generation
OPENAI_API_KEY=your_openai_api_key_here

# LinkedIn credentials for automation
LINKEDIN_USERNAME=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password

# Optional: Override default database credentials
POSTGRES_DB=bridger_db
POSTGRES_USER=bridger_user
POSTGRES_PASSWORD=bridger_password
```

## Required Files

Before running the application, ensure you have:

1. **`credentials.json`** - Google OAuth credentials file for Gmail integration
2. **`token.json`** - Will be created automatically after first Gmail authentication

## Quick Start

1. **Clone and setup:**

   ```bash
   git clone <repository-url>
   cd LinkedInAutomater
   ```

2. **Create environment file:**

   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

3. **Add your Google credentials:**

   - Place your `credentials.json` file in the root directory
   - This file should contain your Google OAuth 2.0 credentials

4. **Build and run:**

   ```bash
   docker-compose up --build
   ```

5. **Access the application:**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Manual Docker Build

If you prefer to build manually:

```bash
# Build the image
docker build -t linkedin-automater .

# Run with environment variables
docker run -d \
  --name linkedin-automater \
  -p 8000:8000 \
  -e SQLALCHEMY_DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e OPENAI_API_KEY="your_key" \
  -e USERNAME="your_linkedin_email" \
  -e PASSWORD="your_linkedin_password" \
  -v $(pwd)/credentials.json:/app/credentials.json:ro \
  -v $(pwd)/token.json:/app/token.json \
  linkedin-automater
```

## Database Setup

The application uses PostgreSQL with the following configuration:

- **Database**: `bridger_db`
- **Schema**: `bridger`
- **User**: `bridger_user`
- **Password**: `bridger_password`

Tables are created automatically when the application starts.

## API Endpoints

- `GET /` - Health check
- `POST /authenticate_gmail` - Authenticate with Gmail
- `POST /setup` - Set up user profile
- `POST /find_connection` - Find and analyze LinkedIn connections
- `POST /send_email` - Send generated emails
- `GET /email_history` - Get email history
- `GET /check_linkedin_status` - Check profile setup status

## Troubleshooting

### Common Issues

1. **Chrome/Playwright issues:**

   ```bash
   # Rebuild with no cache
   docker-compose build --no-cache
   ```

2. **Database connection issues:**

   ```bash
   # Check database logs
   docker-compose logs db

   # Restart database
   docker-compose restart db
   ```

3. **Permission issues:**

   ```bash
   # Fix file permissions
   chmod 644 credentials.json
   chmod 666 token.json
   ```

4. **Memory issues:**
   - Increase Docker memory limit to at least 4GB
   - The application uses OCR and browser automation which can be memory-intensive

### Logs

View application logs:

```bash
docker-compose logs -f app
```

View database logs:

```bash
docker-compose logs -f db
```

## Production Deployment

For production deployment:

1. **Use environment-specific docker-compose files:**

   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Set up proper secrets management:**

   - Use Docker secrets or external secret management
   - Never commit credentials to version control

3. **Configure reverse proxy:**

   - Use nginx or similar for SSL termination
   - Set up proper CORS configuration

4. **Database backup:**
   ```bash
   # Backup database
   docker-compose exec db pg_dump -U bridger_user bridger_db > backup.sql
   ```

## Security Considerations

1. **Environment variables:** Never hardcode secrets
2. **File permissions:** Ensure credentials files have proper permissions
3. **Network security:** Use internal networks for database communication
4. **Updates:** Regularly update base images and dependencies

## Performance Optimization

1. **Resource limits:** Set appropriate CPU and memory limits
2. **Caching:** Consider Redis for session management
3. **Database indexing:** Monitor and optimize database queries
4. **Image optimization:** Use multi-stage builds for smaller images

## Support

For issues and questions:

- Check the application logs
- Review the API documentation at `/docs`
- Ensure all environment variables are set correctly
