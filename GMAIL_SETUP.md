# Gmail Authentication Setup

## Overview

This application requires Gmail authentication to send emails. Due to containerized deployment environments (like Railway), the OAuth flow cannot be completed during deployment. Instead, you need to authenticate locally and include the generated token in your deployment.

## Prerequisites

1. **Gmail API Credentials**: You need a `c.json` file with your Gmail API credentials
2. **Local Python Environment**: To run the authentication script

## Step-by-Step Setup

### 1. Get Gmail API Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Choose "Desktop application" as the application type
6. Download the JSON file and rename it to `c.json`
7. Place `c.json` in your project root directory

### 2. Authenticate Locally

Run the local authentication script:

```bash
python authenticate_local.py
```

This will:

- Open a browser window for Gmail authentication
- Complete the OAuth flow
- Save the credentials to `token.json`

### 3. Deploy to Railway

1. Make sure both `c.json` and `token.json` are in your project root
2. Deploy to Railway
3. The application will use the pre-authenticated token

## File Structure

Your project should have these files:

```
LinkedInAutomater/
├── c.json              # Gmail API credentials
├── token.json          # Generated authentication token
├── main.py
├── app.py
└── ... (other files)
```

## Troubleshooting

### "No valid Gmail credentials available"

**Solution**: Run `python authenticate_local.py` locally to generate `token.json`

### "Gmail service not available"

**Solution**: Check that `token.json` exists and contains valid credentials

### Token Expired

**Solution**: Run `python authenticate_local.py` again to refresh the token

### Browser Authentication Fails

**Solution**:

1. Check your `c.json` file is correct
2. Ensure you have the Gmail API enabled
3. Try running the authentication script again

## Security Notes

- Keep your `c.json` and `token.json` files secure
- Don't commit these files to public repositories
- Use environment variables for sensitive data in production
- Regularly rotate your API credentials

## Testing

After setup, you can test the authentication:

```bash
# Test locally
curl -X POST http://localhost:8000/authenticate_gmail

# Test on Railway
curl -X POST https://your-railway-app.railway.app/authenticate_gmail
```

## Support

If you continue to have issues:

1. Check the Railway logs for specific error messages
2. Verify your Gmail API credentials are correct
3. Ensure `token.json` was generated successfully
4. Test the authentication locally before deploying
