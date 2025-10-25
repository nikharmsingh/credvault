from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Service, Share, AccessLog, PendingInvite
from config import Config
from datetime import datetime
from crypto_utils import encrypt_password, decrypt_password
from cryptography.fernet import InvalidToken

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
mail = Mail(app)

# ---------------- HELPER FUNCTIONS ----------------

def send_invitation_email(recipient_email, service_name, inviter_email):
    """Send invitation email to unregistered user"""
    try:
        msg = Message(
            subject=f"You've been invited to access {service_name} on CredVault",
            recipients=[recipient_email],
            sender=app.config['MAIL_DEFAULT_SENDER']
        )

        # Email body
        msg.body = f"""
Hello!

{inviter_email} has invited you to access their "{service_name}" credentials on CredVault.

To accept this invitation and view the shared credentials:

1. Visit: {request.url_root}register
2. Register with this email address: {recipient_email}
3. Login and access the shared service from your dashboard

CredVault is a secure password vault that allows you to store and share credentials safely.

Best regards,
CredVault Team
        """

        msg.html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
        <h2 style="color: #007bff;">🔐 CredVault Invitation</h2>

        <p>Hello!</p>

        <p><strong>{inviter_email}</strong> has invited you to access their <strong>"{service_name}"</strong> credentials on CredVault.</p>

        <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin: 20px 0;">
            <h3 style="margin-top: 0;">To accept this invitation:</h3>
            <ol>
                <li>Visit: <a href="{request.url_root}register" style="color: #007bff;">{request.url_root}register</a></li>
                <li>Register with this email address: <strong>{recipient_email}</strong></li>
                <li>Login and access the shared service from your dashboard</li>
            </ol>
        </div>

        <p style="color: #666; font-size: 14px;">CredVault is a secure password vault that allows you to store and share credentials safely with end-to-end encryption.</p>

        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">

        <p style="color: #999; font-size: 12px;">
            This is an automated message from CredVault. If you didn't expect this invitation, you can safely ignore this email.
        </p>
    </div>
</body>
</html>
        """

        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_share_notification_email(recipient_email, service_name, inviter_email):
    """Send notification email to registered user when service is shared"""
    try:
        msg = Message(
            subject=f"{inviter_email} shared {service_name} with you on CredVault",
            recipients=[recipient_email],
            sender=app.config['MAIL_DEFAULT_SENDER']
        )

        msg.body = f"""
Hello!

{inviter_email} has shared their "{service_name}" credentials with you on CredVault.

You can now access this service by:
1. Logging into CredVault: {request.url_root}login
2. Check the "Shared With You" section on your dashboard

Best regards,
CredVault Team
        """

        msg.html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
        <h2 style="color: #28a745;">✅ New Service Shared With You</h2>

        <p>Hello!</p>

        <p><strong>{inviter_email}</strong> has shared their <strong>"{service_name}"</strong> credentials with you on CredVault.</p>

        <div style="background-color: #d4edda; padding: 15px; border-left: 4px solid #28a745; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #155724;">Access the shared service:</h3>
            <ol>
                <li>Login to CredVault: <a href="{request.url_root}login" style="color: #28a745;">{request.url_root}login</a></li>
                <li>Check the "Shared With You" section on your dashboard</li>
                <li>Click "Access" to view the credentials</li>
            </ol>
        </div>

        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">

        <p style="color: #999; font-size: 12px;">
            This is an automated message from CredVault.
        </p>
    </div>
</body>
</html>
        """

        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_welcome_email(recipient_email, shared_services_count):
    """Send welcome email to new user with pending invites"""
    try:
        msg = Message(
            subject="Welcome to CredVault! You have shared services waiting",
            recipients=[recipient_email],
            sender=app.config['MAIL_DEFAULT_SENDER']
        )

        msg.body = f"""
Welcome to CredVault!

Your account has been successfully created.

Good news! You have {shared_services_count} service(s) that have been shared with you.

Login now to access them: {request.url_root}login

Best regards,
CredVault Team
        """

        msg.html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
        <h2 style="color: #28a745;">🎉 Welcome to CredVault!</h2>

        <p>Your account has been successfully created.</p>

        <div style="background-color: #d4edda; padding: 15px; border-left: 4px solid #28a745; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #155724;">🎁 You have {shared_services_count} service(s) shared with you!</h3>
            <p>Someone has already shared credentials with you. Login now to access them.</p>
            <p style="text-align: center; margin-top: 15px;">
                <a href="{request.url_root}login" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Login to CredVault</a>
            </p>
        </div>

        <p style="color: #666; font-size: 14px;">CredVault is a secure password vault that allows you to store and share credentials safely with end-to-end encryption.</p>

        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">

        <p style="color: #999; font-size: 12px;">
            This is an automated message from CredVault.
        </p>
    </div>
</body>
</html>
        """

        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# ---------------- AUTH ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        # Validation
        if not email or not password:
            flash("Email and password are required!", "danger")
            return redirect(url_for('register'))

        if len(password) < 6:
            flash("Password must be at least 6 characters long!", "danger")
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash("❌ Email already exists! Please login instead.", "danger")
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)
        new_user = User(email=email, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        # Check for pending invites and convert them to shares
        pending_invites = PendingInvite.query.filter_by(email=email).all()
        if pending_invites:
            for invite in pending_invites:
                share = Share(
                    service_id=invite.service_id,
                    shared_to=new_user.id,
                    shared_by=invite.invited_by
                )
                db.session.add(share)
                db.session.delete(invite)
            db.session.commit()

            # Send welcome email with shared services info
            send_welcome_email(email, len(pending_invites))

            flash(f"🎉 Registered successfully! You have {len(pending_invites)} service(s) shared with you. Check your email!", "success")
        else:
            flash("✅ Registered successfully! Please login to continue.", "success")

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials.", "danger")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for('login'))

# ---------------- DASHBOARD ----------------

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    services = Service.query.filter_by(owner_id=user_id).all()
    shares = Share.query.filter_by(shared_to=user_id).all()

    # Enrich shares with service details and sharer info (services shared WITH you)
    shared_services = []
    for share in shares:
        service = Service.query.get(share.service_id)
        sharer = User.query.get(share.shared_by)
        if service and sharer:
            shared_services.append({
                'share_id': share.id,
                'service_id': service.id,
                'service_name': service.name,
                'service_username': service.username,
                'shared_by_email': sharer.email,
                'shared_at': share.timestamp
            })

    # Get services you've shared with others (services shared BY you)
    my_shares = Share.query.filter_by(shared_by=user_id).all()
    services_i_shared = []
    for share in my_shares:
        service = Service.query.get(share.service_id)
        recipient = User.query.get(share.shared_to)
        if service and recipient:
            services_i_shared.append({
                'share_id': share.id,
                'service_id': service.id,
                'service_name': service.name,
                'shared_with_email': recipient.email,
                'shared_at': share.timestamp
            })

    # Get count of pending invites sent by user
    pending_invites_count = PendingInvite.query.filter_by(invited_by=user_id).count()

    return render_template('dashboard.html',
                         services=services,
                         shared_services=shared_services,
                         services_i_shared=services_i_shared,
                         pending_invites_count=pending_invites_count)

# ---------------- ADD / SHARE / ACCESS ----------------

@app.route('/add', methods=['GET', 'POST'])
def add_service():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name'].strip()
        username = request.form['username'].strip()
        password = request.form['password']

        # Validation
        if not name or not username or not password:
            flash("All fields are required!", "danger")
            return render_template('add_service.html')

        # encrypt password before saving
        try:
            ciphertext = encrypt_password(password)
        except Exception as e:
            flash(f"Encryption error: {str(e)}", "danger")
            return render_template('add_service.html')

        service = Service(
            name=name,
            username=username,
            password_encrypted=ciphertext,
            owner_id=session['user_id']
        )
        db.session.add(service)
        db.session.commit()
        flash(f"✅ Service '{name}' added and encrypted successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template('add_service.html')

@app.route('/edit/<int:service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    """Edit an existing service"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    service = Service.query.get(service_id)
    if not service or service.owner_id != session['user_id']:
        flash('Service not found or you do not have permission', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form['name'].strip()
        username = request.form['username'].strip()
        password = request.form.get('password', '').strip()

        # Validation
        if not name or not username:
            flash("Name and username are required!", "danger")
            return render_template('edit_service.html', service=service)

        service.name = name
        service.username = username

        # Only update password if provided
        if password:
            try:
                service.password_encrypted = encrypt_password(password)
            except Exception as e:
                flash(f"Encryption error: {str(e)}", "danger")
                return render_template('edit_service.html', service=service)

        db.session.commit()
        flash(f"✅ Service '{name}' updated successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('edit_service.html', service=service)

@app.route('/delete/<int:service_id>', methods=['POST'])
def delete_service(service_id):
    """Delete a service and all its shares"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    service = Service.query.get(service_id)
    if not service or service.owner_id != session['user_id']:
        flash('Service not found or you do not have permission', 'danger')
        return redirect(url_for('dashboard'))

    service_name = service.name

    # Delete all shares for this service
    Share.query.filter_by(service_id=service_id).delete()

    # Delete all pending invites for this service
    PendingInvite.query.filter_by(service_id=service_id).delete()

    # Delete all access logs for this service
    AccessLog.query.filter_by(service_id=service_id).delete()

    # Delete the service
    db.session.delete(service)
    db.session.commit()

    flash(f"🗑️ Service '{service_name}' and all related data deleted successfully!", "success")
    return redirect(url_for('dashboard'))

@app.route('/share/<int:service_id>', methods=['POST'])
def share_service(service_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    target_email = request.form['email'].strip().lower()

    # ensure only owner can share
    svc = Service.query.get(service_id)
    if not svc or svc.owner_id != session['user_id']:
        flash('Not allowed to share this service', 'danger')
        return redirect(url_for('dashboard'))

    # Get current user's email to prevent self-sharing
    current_user = User.query.get(session['user_id'])
    if current_user.email == target_email:
        flash('You cannot share a service with yourself', 'warning')
        return redirect(url_for('dashboard'))

    target_user = User.query.filter_by(email=target_email).first()

    if target_user:
        # User exists - create share immediately
        # check if already shared
        existing_share = Share.query.filter_by(service_id=service_id, shared_to=target_user.id).first()
        if existing_share:
            flash(f'Service already shared with {target_email}', 'info')
            return redirect(url_for('dashboard'))

        share = Share(service_id=service_id, shared_to=target_user.id, shared_by=session['user_id'])
        db.session.add(share)
        db.session.commit()

        # Send notification email to registered user
        email_sent = send_share_notification_email(target_email, svc.name, current_user.email)
        if email_sent:
            flash(f'Service shared successfully with {target_email}! Notification email sent.', 'success')
        else:
            flash(f'Service shared successfully with {target_email}! (Email notification failed)', 'warning')
    else:
        # User doesn't exist - create pending invite
        existing_invite = PendingInvite.query.filter_by(email=target_email, service_id=service_id).first()
        if existing_invite:
            flash(f'Invitation already sent to {target_email}', 'info')
            return redirect(url_for('dashboard'))

        invite = PendingInvite(
            email=target_email,
            service_id=service_id,
            invited_by=session['user_id']
        )
        db.session.add(invite)
        db.session.commit()

        # Send invitation email to unregistered user
        email_sent = send_invitation_email(target_email, svc.name, current_user.email)
        if email_sent:
            flash(f'Invitation sent to {target_email}! They will get access when they register. Email sent.', 'success')
        else:
            flash(f'Invitation created for {target_email}. They will get access when they register. (Email failed to send)', 'warning')

    return redirect(url_for('dashboard'))

@app.route('/access/<int:service_id>')
def access_service(service_id):
    """
    Show service details without revealing the password.
    Access allowed to:
    - Owner of the service
    - A user who has been shared the service (Share.shared_to)
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    svc = Service.query.get(service_id)
    if not svc:
        flash("Service not found", "danger")
        return redirect(url_for('dashboard'))

    # Access allowed if user is owner or there's a share for this user
    allowed = False
    if svc.owner_id == user_id:
        allowed = True
    else:
        share = Share.query.filter_by(service_id=service_id, shared_to=user_id).first()
        if share:
            allowed = True

    if not allowed:
        flash("You don't have permission to view this service", "danger")
        return redirect(url_for('dashboard'))

    # Show service without password (password_plain=None)
    return render_template('access_logs.html', service=svc, password_plain=None)

@app.route('/reveal/<int:service_id>')
def reveal(service_id):
    """
    Decrypt and show credential only to:
    - Owner of the service
    - A user who has been shared the service (Share.shared_to)
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    svc = Service.query.get(service_id)
    if not svc:
        flash("Service not found", "danger")
        return redirect(url_for('dashboard'))

    # Access allowed if user is owner or there's a share for this user
    allowed = False
    if svc.owner_id == user_id:
        allowed = True
    else:
        share = Share.query.filter_by(service_id=service_id, shared_to=user_id).first()
        if share:
            allowed = True

    if not allowed:
        flash("You don't have permission to view this credential", "danger")
        return redirect(url_for('dashboard'))

    # log the access
    log = AccessLog(service_id=service_id, user_id=user_id, ip=request.remote_addr)
    db.session.add(log)
    db.session.commit()

    # decrypt
    try:
        password_plain = decrypt_password(svc.password_encrypted)
    except InvalidToken:
        flash("Decryption failed (invalid encryption key or corrupted data).", "danger")
        password_plain = "[decryption error]"

    # render a template that shows the decrypted password
    return render_template('access_logs.html', service=svc, password_plain=password_plain)

@app.route('/logs')
def logs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    logs = AccessLog.query.order_by(AccessLog.accessed_at.desc()).all()
    return render_template('access_logs.html', logs=logs)

# ---------------- SHARE MANAGEMENT ----------------

@app.route('/my-shares')
def my_shares():
    """View all services you've shared with others"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Get all shares created by current user
    shares = Share.query.filter_by(shared_by=user_id).all()

    # Enrich with service and recipient details
    shares_details = []
    for share in shares:
        service = Service.query.get(share.service_id)
        recipient = User.query.get(share.shared_to)
        if service and recipient:
            shares_details.append({
                'share_id': share.id,
                'service_id': service.id,
                'service_name': service.name,
                'service_username': service.username,
                'shared_with_email': recipient.email,
                'shared_at': share.timestamp
            })

    return render_template('my_shares.html', shares=shares_details)

@app.route('/unshare/<int:share_id>', methods=['POST'])
def unshare(share_id):
    """Revoke access to a shared service"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    share = Share.query.get(share_id)
    if not share or share.shared_by != session['user_id']:
        flash('Share not found or you do not have permission', 'danger')
        return redirect(url_for('my_shares'))

    # Get details before deleting
    recipient = User.query.get(share.shared_to)
    service = Service.query.get(share.service_id)

    db.session.delete(share)
    db.session.commit()

    if recipient and service:
        flash(f'Access revoked: {recipient.email} can no longer access "{service.name}"', 'success')
    else:
        flash('Share removed successfully', 'success')

    return redirect(url_for('my_shares'))

# ---------------- USERS & INVITES ----------------

@app.route('/users')
def list_users():
    """List all registered users - useful for development/testing"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/invites')
def list_invites():
    """View pending invites sent by current user"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get invites sent by current user
    sent_invites = PendingInvite.query.filter_by(invited_by=session['user_id']).all()

    # Enrich with service names
    invites_with_details = []
    for invite in sent_invites:
        service = Service.query.get(invite.service_id)
        invites_with_details.append({
            'id': invite.id,
            'email': invite.email,
            'service_name': service.name if service else 'Unknown',
            'created_at': invite.created_at
        })

    return render_template('invites.html', invites=invites_with_details)

@app.route('/invites/cancel/<int:invite_id>', methods=['POST'])
def cancel_invite(invite_id):
    """Cancel a pending invite"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    invite = PendingInvite.query.get(invite_id)
    if not invite or invite.invited_by != session['user_id']:
        flash('Invite not found or you do not have permission', 'danger')
        return redirect(url_for('list_invites'))

    email = invite.email
    db.session.delete(invite)
    db.session.commit()
    flash(f'Invitation to {email} cancelled', 'success')
    return redirect(url_for('list_invites'))

# ---------------- INIT ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
