#!/usr/bin/env python3
"""
CredVault Setup Script
Helps you generate secure keys for your .env file
"""

import secrets
from cryptography.fernet import Fernet

def generate_keys():
    """Generate secure keys for the application"""
    print("🔐 CredVault Setup - Key Generation")
    print("=" * 50)
    print()
    
    # Generate SECRET_KEY
    secret_key = secrets.token_hex(32)
    print("✅ Generated SECRET_KEY (Flask session secret)")
    print(f"SECRET_KEY={secret_key}")
    print()
    
    # Generate ENCRYPTION_KEY
    encryption_key = Fernet.generate_key().decode()
    print("✅ Generated ENCRYPTION_KEY (Fernet encryption key)")
    print(f"ENCRYPTION_KEY={encryption_key}")
    print()
    
    print("=" * 50)
    print("📝 Next Steps:")
    print()
    print("1. Create a .env file in your project root")
    print("2. Copy the keys above into your .env file")
    print("3. Add your email configuration (optional)")
    print()
    print("Example .env file:")
    print("-" * 50)
    print(f"SECRET_KEY={secret_key}")
    print(f"ENCRYPTION_KEY={encryption_key}")
    print()
    print("# Email Configuration (optional)")
    print("MAIL_SERVER=smtp.gmail.com")
    print("MAIL_PORT=587")
    print("MAIL_USE_TLS=True")
    print("MAIL_USERNAME=your-email@gmail.com")
    print("MAIL_PASSWORD=your-app-password")
    print("MAIL_DEFAULT_SENDER=your-email@gmail.com")
    print("-" * 50)
    print()
    print("⚠️  IMPORTANT: Keep these keys secure!")
    print("   - Never commit .env to version control")
    print("   - Backup your ENCRYPTION_KEY safely")
    print("   - Losing ENCRYPTION_KEY means losing all passwords")
    print()
    print("🚀 After setup, run: python app.py")
    print()

if __name__ == "__main__":
    generate_keys()

