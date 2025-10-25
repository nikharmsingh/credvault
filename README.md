# 🔐 CredVault - Secure Password Manager

A secure, encrypted password management system with sharing capabilities built with Flask.

## ✨ Features

### 🔒 Security
- **End-to-end encryption** using Fernet (symmetric encryption)
- **Password hashing** with Werkzeug's secure hash functions
- **Access logging** - Track who accessed what and when
- **Session management** - Secure user authentication

### 👥 Sharing & Collaboration
- **Share credentials** with other users via email
- **Pending invites** - Share with unregistered users
- **Email notifications** - Automatic notifications when sharing
- **Revoke access** - Remove access anytime
- **Share management** - See who has access to your services

### 📊 User Experience
- Clean, modern Bootstrap 5 interface
- Dashboard with all your services
- View services shared with you
- Manage your shares and invites
- User directory for easy sharing

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd credvault
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file:
```env
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-fernet-key-here

# Email Configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

**Generate keys:**
```python
# SECRET_KEY
import secrets
print(secrets.token_hex(32))

# ENCRYPTION_KEY
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

5. **Run the application**
```bash
python app.py
```

Visit `http://localhost:5000`

## 📖 Usage Guide

### 1. Register & Login
- Create an account with your email
- Login to access your dashboard

### 2. Add Services
- Click "Add Service"
- Enter service name, username, and password
- Password is encrypted before storage

### 3. Access Credentials
- Click "Access" to view service details
- Click "Reveal" to decrypt and view password
- All access is logged for security

### 4. Share Services
- Enter recipient's email in the share field
- Works with registered or unregistered users
- Recipient gets email notification
- They can access shared credentials immediately

### 5. Manage Shares
- Click "My Shares" to see who has access
- Revoke access anytime with one click
- View services shared with you

### 6. Pending Invites
- View pending invitations you've sent
- Cancel invites if needed
- Invites auto-convert when user registers

## 🏗️ Architecture

### Tech Stack
- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Encryption**: Cryptography (Fernet)
- **Email**: Flask-Mail
- **Frontend**: Bootstrap 5, Jinja2 templates

### Database Models
- **User** - User accounts
- **Service** - Stored credentials (encrypted)
- **Share** - Sharing relationships
- **PendingInvite** - Invitations for unregistered users
- **AccessLog** - Audit trail of credential access

### Security Features
- Passwords encrypted at rest with Fernet
- User passwords hashed with Werkzeug
- Session-based authentication
- Access control checks on all routes
- IP logging for access tracking

## 📁 Project Structure

```
credvault/
├── app.py              # Main Flask application
├── models.py           # Database models
├── config.py           # Configuration
├── crypto_utils.py     # Encryption utilities
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── templates/         # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── add_service.html
│   ├── access_logs.html
│   ├── my_shares.html
│   ├── users.html
│   └── invites.html
├── static/            # CSS and static files
│   └── style.css
└── instance/          # Database (auto-created)
    └── vault.db
```

## 🔧 Configuration

### Email Setup (Gmail)
1. Enable 2-factor authentication on your Google account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the app password in `.env` file

### Environment Variables
- `SECRET_KEY` - Flask session secret (required)
- `ENCRYPTION_KEY` - Fernet encryption key (required)
- `MAIL_*` - Email configuration (optional, for notifications)

## 🛡️ Security Best Practices

1. **Never commit `.env` file** - Contains sensitive keys
2. **Use strong SECRET_KEY** - Generate with `secrets.token_hex(32)`
3. **Backup ENCRYPTION_KEY** - Losing it means losing all passwords
4. **Use HTTPS in production** - Never send credentials over HTTP
5. **Regular backups** - Backup `instance/vault.db` regularly
6. **Monitor access logs** - Check for suspicious activity

## 🚀 Deployment

### Heroku
```bash
# Already configured with Procfile and runtime.txt
heroku create your-app-name
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ENCRYPTION_KEY=your-encryption-key
git push heroku main
```

### Docker (Coming Soon)
Docker support will be added in future updates.

## 📝 API Routes

### Authentication
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - Logout

### Dashboard
- `GET /` - Home (redirects to dashboard)
- `GET /dashboard` - Main dashboard

### Services
- `GET/POST /add` - Add new service
- `POST /share/<service_id>` - Share service
- `GET /access/<service_id>` - View service details
- `GET /reveal/<service_id>` - Decrypt and show password

### Share Management
- `GET /my-shares` - View all your shares
- `POST /unshare/<share_id>` - Revoke access

### Users & Invites
- `GET /users` - List all users
- `GET /invites` - View pending invites
- `POST /invites/cancel/<invite_id>` - Cancel invite

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Flask framework
- Cryptography library
- Bootstrap for UI
- All contributors

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

**⚠️ Important Security Note**: This is a personal password manager. For production use with multiple users, consider additional security measures like:
- Rate limiting
- Two-factor authentication
- Password strength requirements
- Session timeout
- CSRF protection
- Security headers

