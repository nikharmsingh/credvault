# 🚀 CredVault - Quick Start Guide

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Gmail account (for email notifications - optional)

---

## ⚡ Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Generate Security Keys

```bash
python setup.py
```

This will generate:
- `SECRET_KEY` - For Flask sessions
- `ENCRYPTION_KEY` - For password encryption

**⚠️ IMPORTANT:** Save these keys securely! Losing the ENCRYPTION_KEY means losing all stored passwords.

### Step 3: Create .env File

Create a file named `.env` in the project root and paste the keys from Step 2:

```env
SECRET_KEY=your-generated-secret-key-here
ENCRYPTION_KEY=your-generated-encryption-key-here

# Email Configuration (Optional - for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### Step 4: Run the Application

```bash
python app.py
```

### Step 5: Open in Browser

Visit: **http://localhost:5000**

---

## 🎯 First Time Usage

### 1. Register an Account
- Click "Register here"
- Enter your email and password (min 6 characters)
- Click "Create Account"

### 2. Login
- Enter your credentials
- Click "Login"

### 3. Add Your First Service
- Click "➕ Add Service" in the navbar
- Enter service name (e.g., "Netflix")
- Enter username/email
- Enter password
- Click "Add Service"

### 4. Access Your Credentials
- Go to Dashboard
- Click "🔑 Access" on any service
- Click "Reveal (decrypt)" to see the password

---

## 🎨 Features Overview

### 🔐 Core Features
- **Add Services** - Store encrypted credentials
- **Edit Services** - Update name, username, or password
- **Delete Services** - Remove services and all shares
- **Access Credentials** - View and decrypt passwords
- **Access Logs** - Track who accessed what

### 👥 Sharing Features
- **Share with Users** - Share credentials via email
- **Pending Invites** - Invite unregistered users
- **My Shares** - See who has access to your services
- **Revoke Access** - Remove access anytime
- **Email Notifications** - Automatic notifications

### 🎨 UI Features
- **Modern Design** - Beautiful gradient interface
- **Responsive** - Works on mobile, tablet, desktop
- **Animations** - Smooth transitions and effects
- **Navigation** - Easy-to-use navbar
- **Flash Messages** - Helpful feedback with emojis

---

## 📧 Email Setup (Optional)

### For Gmail:

1. **Enable 2-Factor Authentication**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "CredVault"
   - Copy the 16-character password

3. **Add to .env**
   ```env
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-char-app-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

---

## 🔧 Common Tasks

### Add a Service
```
Dashboard → ➕ Add Service → Fill form → Add Service
```

### Edit a Service
```
Dashboard → Find service → ✏️ Edit → Update → Save Changes
```

### Delete a Service
```
Dashboard → Find service → 🗑️ Delete → Confirm
```

### Share a Service
```
Dashboard → Find service → Enter email → 📤 Share
```

### View Your Shares
```
Dashboard → 📤 My Shares (top right)
```

### Revoke Access
```
My Shares → Find share → 🚫 Revoke Access → Confirm
```

---

## 🛡️ Security Best Practices

### ✅ DO:
- ✅ Keep your `.env` file secure
- ✅ Backup your `ENCRYPTION_KEY`
- ✅ Use strong passwords (12+ characters)
- ✅ Regularly review access logs
- ✅ Revoke access when no longer needed
- ✅ Use HTTPS in production

### ❌ DON'T:
- ❌ Commit `.env` to version control
- ❌ Share your `ENCRYPTION_KEY`
- ❌ Use the same password everywhere
- ❌ Leave unused shares active
- ❌ Run in production with `debug=True`

---

## 📱 Mobile Usage

The app is fully responsive! Access it from:
- 📱 iPhone/Android browsers
- 📱 iPad/Tablet browsers
- 💻 Desktop browsers

All features work on mobile devices.

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "No such table" error
```bash
# Delete the database and restart
rm instance/vault.db
python app.py
```

### Email not sending
- Check your Gmail app password
- Verify 2FA is enabled
- Check `.env` configuration
- App works without email (optional feature)

### "Invalid encryption key" error
- Your `ENCRYPTION_KEY` changed
- Restore from backup or reset database
- **Warning:** Changing key loses all passwords

---

## 📊 Project Structure

```
credvault/
├── app.py              # Main application
├── models.py           # Database models
├── config.py           # Configuration
├── crypto_utils.py     # Encryption utilities
├── setup.py            # Key generation script
├── requirements.txt    # Dependencies
├── .env               # Your secrets (create this!)
├── .gitignore         # Git ignore rules
├── README.md          # Full documentation
├── IMPROVEMENTS.md    # What's new
├── QUICK_START.md     # This file
├── templates/         # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── add_service.html
│   ├── edit_service.html
│   ├── access_logs.html
│   ├── my_shares.html
│   ├── users.html
│   └── invites.html
├── static/
│   └── style.css      # Beautiful CSS
└── instance/
    └── vault.db       # Database (auto-created)
```

---

## 🎓 Learning Resources

### Flask
- Official Docs: https://flask.palletsprojects.com/
- Tutorial: https://flask.palletsprojects.com/tutorial/

### Cryptography
- Fernet: https://cryptography.io/en/latest/fernet/
- Best Practices: https://cryptography.io/en/latest/hazmat/

### Bootstrap
- Docs: https://getbootstrap.com/docs/5.3/

---

## 🚀 Deployment

### Heroku (Recommended)

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-credvault-app

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ENCRYPTION_KEY=your-encryption-key

# Deploy
git push heroku main

# Open app
heroku open
```

### Other Platforms
- **Railway**: Similar to Heroku
- **Render**: Free tier available
- **PythonAnywhere**: Good for beginners
- **DigitalOcean**: More control

---

## 📞 Support

### Issues?
- Check `README.md` for detailed docs
- Check `IMPROVEMENTS.md` for what's new
- Review error messages carefully
- Check the terminal for detailed errors

### Need Help?
- Review the code comments
- Check Flask documentation
- Search for error messages online

---

## 🎉 You're Ready!

Your CredVault is now set up and ready to use!

**Next Steps:**
1. ✅ Run `python app.py`
2. ✅ Visit http://localhost:5000
3. ✅ Register an account
4. ✅ Add your first service
5. ✅ Explore all features!

**Enjoy your secure password manager! 🔐**

---

## 📝 Quick Reference

| Action | URL | Method |
|--------|-----|--------|
| Home | `/` | GET |
| Login | `/login` | GET/POST |
| Register | `/register` | GET/POST |
| Dashboard | `/dashboard` | GET |
| Add Service | `/add` | GET/POST |
| Edit Service | `/edit/<id>` | GET/POST |
| Delete Service | `/delete/<id>` | POST |
| Access Service | `/access/<id>` | GET |
| Reveal Password | `/reveal/<id>` | GET |
| Share Service | `/share/<id>` | POST |
| My Shares | `/my-shares` | GET |
| Unshare | `/unshare/<id>` | POST |
| Users List | `/users` | GET |
| Invites List | `/invites` | GET |
| Logout | `/logout` | GET |

---

**Happy Password Managing! 🎊🔐**

