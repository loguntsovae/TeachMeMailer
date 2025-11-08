# Gmail SMTP Configuration Guide

This guide explains how to configure Gmail SMTP for the Mail Gateway Service.

## Prerequisites

1. **Gmail Account**: You need a Gmail account (loguntsovae.teachmeskills@gmail.com)
2. **2-Factor Authentication**: Must be enabled on your Gmail account
3. **App Password**: Required for SMTP authentication

## Step 1: Enable 2-Factor Authentication

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable "2-Step Verification" if not already enabled
3. Follow the setup instructions

## Step 2: Generate Gmail App Password

1. Visit [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Sign in to your account
3. Select "Mail" as the app type
4. Select "Other (custom name)" and enter "Mail Gateway Service"
5. Click "Generate"
6. Copy the 16-character app password (format: xxxx xxxx xxxx xxxx)

## Step 3: Configure Environment Variables

Update your `.env` file with the Gmail App Password:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=loguntsovae.teachmeskills@gmail.com
SMTP_PASSWORD=your-16-character-app-password
SMTP_STARTTLS=1
FROM_EMAIL=loguntsovae.teachmeskills@gmail.com
```

**Important**: Replace `your-16-character-app-password` with the actual app password from Step 2.

## Step 4: Test Configuration

Run the test script to verify your configuration:

```bash
uv run python -m app.scripts.test_mail
```

This will:
1. Display your SMTP configuration
2. Check if the app password is set correctly
3. Send a test email to verify connectivity
4. Show status code 250 OK if successful

## Environment Variable Alternative

For production or CI/CD, you can set the Gmail App Password as an environment variable:

```bash
export GMAIL_APP_PASSWORD="your-16-character-app-password"
```

Then use in `.env`:
```bash
SMTP_PASSWORD=${GMAIL_APP_PASSWORD}
```

## Security Notes

- **Never commit** your Gmail App Password to version control
- **Use App Passwords only** - never your regular Gmail password
- **Rotate App Passwords** periodically for security
- **Revoke unused** App Passwords from your Google Account

## Troubleshooting

### Common Issues

1. **"Invalid credentials" error**:
   - Verify 2FA is enabled
   - Generate a new App Password
   - Ensure no extra spaces in the password

2. **"Connection timeout" error**:
   - Check firewall settings
   - Verify port 587 is open
   - Ensure STARTTLS is enabled

3. **"Authentication required" error**:
   - Verify SMTP_USER matches your Gmail address
   - Confirm App Password is correctly set

### Verification Commands

Check configuration without sending email:
```bash
uv run python -c "from app.core.config import get_settings; s=get_settings(); print(f'Host: {s.smtp_host}:{s.smtp_port}'); print(f'User: {s.smtp_user}'); print(f'Password set: {bool(s.smtp_password)}')"
```

### Success Indicators

- Test email sent successfully
- Log shows "250 OK" SMTP response
- Recipient receives the email
- Gmail "Sent" folder shows the message

## Production Deployment

For production deployments:

1. Set `GMAIL_APP_PASSWORD` as a secure environment variable
2. Never include the App Password in Docker images
3. Use secret management systems (AWS Secrets Manager, etc.)
4. Monitor email delivery logs for "250 OK" status codes

## Configuration Summary

Current Gmail SMTP settings:
- **Server**: smtp.gmail.com
- **Port**: 587 (STARTTLS)
- **Security**: TLS/STARTTLS
- **Authentication**: Username/App Password
- **From Address**: loguntsovae.teachmeskills@gmail.com