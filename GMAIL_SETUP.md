# Gmail SMTP Configuration Guide for ClassCritic

## Quick Setup

### 1. Enable Gmail SMTP

Edit your `.env` file and update these values:

```env
EMAIL_BACKEND=smtp
EMAIL_HOST_USER=your-actual-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
```

### 2. Get Gmail App Password

**Important**: You MUST use an App Password, not your regular Gmail password!

#### Steps:
1. **Enable 2-Factor Authentication**
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification" and follow the setup

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Sign in if prompted
   - Select app: **Mail**
   - Select device: **Other (Custom name)** → Type "ClassCritic"
   - Click **Generate**
   - You'll see a 16-character password like: `abcd efgh ijkl mnop`

3. **Copy the App Password**
   - Remove spaces: `abcdefghijklmnop`
   - Paste into `.env` file as `EMAIL_HOST_PASSWORD`

### 3. Example .env Configuration

```env
# Django Settings
SECRET_KEY=django-insecure-n5f=)hsm0sychx5f3&cv_1(03ah@yo3-5(%yvata(97npdp8%)
DEBUG=True

# Email Configuration - SMTP Mode
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=myemail@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop

# Default sender email
DEFAULT_FROM_EMAIL=noreply@classcritic.com
```

### 4. Restart the Server

After updating `.env`, restart Django:

```bash
# Stop the server (Ctrl+C)
# Then restart:
python manage.py runserver
```

## Testing Email Sending

1. Go to: http://localhost:8000/register/
2. Enter a valid `@std.ewubd.edu` email
3. Click "Send OTP"
4. Check the email inbox for the OTP

## Troubleshooting

### "Authentication failed" Error

**Solution**: Make sure you're using an App Password, not your regular Gmail password.

### "SMTP connection failed" Error

**Solution**: Check that:
- 2-Factor Authentication is enabled
- App Password is correct (no spaces)
- `EMAIL_BACKEND=smtp` (not `console`)

### Emails not arriving

**Solution**:
- Check spam/junk folder
- Verify the recipient email is correct
- Check Gmail's "Sent" folder to confirm email was sent

### Still using console backend

**Solution**: Make sure `.env` has `EMAIL_BACKEND=smtp` (not `console`)

## Switch Back to Console Mode

To test without sending real emails:

```env
EMAIL_BACKEND=console
```

OTPs will print in the terminal instead of sending emails.

## Security Best Practices

✅ **DO**:
- Use App Passwords (16 characters)
- Keep `.env` file private
- Add `.env` to `.gitignore` (already done)
- Use different passwords for different apps

❌ **DON'T**:
- Commit `.env` to Git
- Share your App Password
- Use your regular Gmail password
- Hardcode credentials in code

## Files Created

- `.env` - Your actual configuration (DO NOT commit)
- `.env.example` - Template for others (safe to commit)
- `.gitignore` - Prevents `.env` from being committed

---

**Need Help?** Check the main [README.md](README.md) for more information.
