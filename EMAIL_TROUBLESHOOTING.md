# SMTP Email Troubleshooting Guide

## Problem: No emails are being sent

This guide will help you fix SMTP email issues in ClassCritic.

## Step 1: Check Your .env File

Your `.env` file should look like this:

```env
# Email Configuration
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-actual-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
DEFAULT_FROM_EMAIL=noreply@classcritic.com
```

### Common Mistakes:

❌ **EMAIL_BACKEND=console** (this prints to console, doesn't send emails)  
✅ **EMAIL_BACKEND=smtp** (this sends real emails)

❌ Using your regular Gmail password  
✅ Using a 16-character App Password

❌ Spaces in the App Password  
✅ No spaces: `abcdefghijklmnop`

## Step 2: Generate Gmail App Password

If you haven't already:

1. **Enable 2-Factor Authentication**:
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Follow the setup process

2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: **Mail**
   - Select device: **Other (Custom name)** → Type "ClassCritic"
   - Click **Generate**
   - Copy the 16-character password (remove spaces)

3. **Update .env**:
   ```env
   EMAIL_HOST_USER=youremail@gmail.com
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   ```

## Step 3: Run the Test Script

```bash
python test_email.py
```

This will:
- Show your current email configuration
- Check for common issues
- Allow you to send a test email

## Step 4: Common Error Messages & Solutions

### Error: "Authentication failed"

**Cause**: Wrong password or not using App Password

**Solution**:
1. Make sure you're using an App Password (16 characters)
2. Not your regular Gmail password
3. Generate a new App Password if needed

### Error: "SMTPServerDisconnected"

**Cause**: Wrong port or TLS settings

**Solution**:
```env
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### Error: "Connection refused"

**Cause**: Firewall or network issue

**Solution**:
1. Check your firewall settings
2. Try a different network
3. Verify Gmail SMTP is not blocked

### Error: No error but emails not arriving

**Possible Causes**:
1. EMAIL_BACKEND is still set to 'console'
2. Emails going to spam folder
3. Wrong recipient email

**Solution**:
1. Check `.env` has `EMAIL_BACKEND=smtp`
2. Check spam/junk folder
3. Verify recipient email is correct

## Step 5: Restart the Server

After changing `.env`, you MUST restart Django:

```bash
# Stop the server (Ctrl+C)
# Then restart:
python manage.py runserver
```

## Step 6: Test in the Application

1. Go to: http://localhost:8000/register/
2. Enter a valid `@std.ewubd.edu` email
3. Click "Send OTP"
4. Check your email inbox (and spam folder)

## Quick Checklist

- [ ] `.env` file exists in project root
- [ ] `EMAIL_BACKEND=smtp` (not console)
- [ ] `EMAIL_HOST_USER` is your Gmail address
- [ ] `EMAIL_HOST_PASSWORD` is App Password (16 chars, no spaces)
- [ ] 2-Factor Authentication enabled on Gmail
- [ ] App Password generated from Google Account
- [ ] Server restarted after changing `.env`
- [ ] Checked spam folder

## Still Not Working?

### Option 1: Use Console Backend for Testing

Temporarily use console backend to see OTPs in terminal:

```env
EMAIL_BACKEND=console
```

OTPs will print in the terminal where Django is running.

### Option 2: Check Django Logs

Look for error messages in the terminal where `python manage.py runserver` is running.

### Option 3: Try Different Email Provider

If Gmail isn't working, you can try other SMTP providers:

**Outlook/Hotmail:**
```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@outlook.com
EMAIL_HOST_PASSWORD=your-password
```

**Yahoo:**
```env
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@yahoo.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Need More Help?

Run the test script and share the output:

```bash
python test_email.py
```

This will show exactly what's configured and help identify the issue.

---

**Remember**: After ANY change to `.env`, you MUST restart the Django server!
