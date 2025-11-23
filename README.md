# ClassCritic Setup Instructions

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Start Development Server
```bash
python manage.py runserver
```

### 5. Access the Application
- **Home Page**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

## Email Configuration

The application uses a `.env` file for email configuration. This keeps your credentials secure and separate from the code.

### Option 1: Console Backend (Development/Testing)

By default, OTPs are printed in the console. No configuration needed!

The `.env` file is already set to:
```
EMAIL_BACKEND=console
```

### Option 2: Gmail SMTP (Production)

To send real emails via Gmail:

#### Step 1: Generate Gmail App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Enable **2-Factor Authentication** (Security → 2-Step Verification)
3. Generate an **App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Other" (enter "ClassCritic")
   - Click "Generate"
   - Copy the 16-character password

#### Step 2: Update .env File

Edit the `.env` file in the project root:

```env
# Change EMAIL_BACKEND from 'console' to 'smtp'
EMAIL_BACKEND=smtp

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password

# Default sender email
DEFAULT_FROM_EMAIL=noreply@classcritic.com
```

#### Step 3: Restart Server

```bash
python manage.py runserver
```

Now OTPs will be sent to real email addresses!

### Security Notes

- ⚠️ **Never commit `.env` to Git** (already in `.gitignore`)
- ✅ Use App Passwords, not your regular Gmail password
- ✅ Keep `.env.example` as a template (without real credentials)

## Important Notes

### Email Restriction
- **Only @std.ewubd.edu emails are accepted** for student registration
- This is enforced at multiple levels:
  - Model validation
  - Form validation
  - Custom validator function

### OTP System
- OTPs are 6 digits
- Valid for 5 minutes
- Sent via email (console in development)

### Review Requirements
- Minimum 100 words in description
- Points must be between 0-10
- Tags are optional (predefined list)
- Anonymous option available

## Admin Setup

After creating a superuser, log into the admin panel and add:

1. **Departments** (e.g., Computer Science, Mathematics)
2. **Courses** (e.g., CSE101, MATH201)
3. **Faculty** (assign to departments and courses)
4. **Questions** (optional review questions)

## Features

✅ Student registration with @std.ewubd.edu email validation  
✅ OTP-based authentication  
✅ Anonymous and normal reviews  
✅ Search by faculty, course, department, tags  
✅ Average rating calculations  
✅ Modern dark theme UI with glassmorphism  
✅ Responsive design  
✅ Real-time word counter for reviews  
✅ Tag filtering  

## Testing the Application

1. **Register a student** with email ending in @std.ewubd.edu
2. **Check console** for OTP
3. **Verify OTP** to login
4. **Submit a review** (test both normal and anonymous)
5. **Search and filter** reviews
6. **View faculty details** with ratings

Enjoy using ClassCritic! 🎓
