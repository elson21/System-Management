# Authentication System for System Management

This document describes the authentication system implemented for the System Management application.

## Overview

The authentication system provides secure user login functionality with **admin-only user creation**:
- **JWT (JSON Web Tokens)** for session management
- **Password hashing** with bcrypt for security
- **Protected routes** that require authentication
- **Admin-only user management** - only administrators can create new users
- **Modern UI** with responsive design

## Features

### 🔐 User Authentication
- **Login**: Users can sign in with email and password
- **Admin-Only Registration**: Only administrators can create new user accounts
- **Password Security**: Passwords are hashed using bcrypt
- **Session Management**: JWT tokens for maintaining user sessions

### 🛡️ Security Features
- **Password Hashing**: Secure bcrypt hashing algorithm
- **JWT Tokens**: Stateless authentication with configurable expiration
- **Protected Routes**: API endpoints require valid authentication
- **Admin Privileges**: User creation restricted to administrators only
- **Input Validation**: Form validation and sanitization

### 🎨 User Interface
- **Modern Design**: Clean, responsive interface using Tailwind CSS
- **Glass Morphism**: Beautiful glass-effect design elements
- **Responsive Layout**: Works on desktop and mobile devices
- **User Feedback**: Success/error messages and loading states
- **Admin Panel**: Specialized interface for user management

## Installation

### 1. Install Dependencies

Run the installation script to install required packages:

```bash
python install_deps.py
```

Or install manually:

```bash
pip install passlib[bcrypt] python-jose[cryptography] python-multipart
```

### 2. Database Setup

Ensure your database is set up with the updated User model that includes:
- `password_hash` field for storing hashed passwords
- `is_admin` field for admin privileges
- `last_login` field for tracking user activity

### 3. Create First Admin User

Run the admin creation script to set up your first administrator:

```bash
python create_admin.py
```

This script will:
- Create the first admin user account
- Set up the default organization
- Allow you to log in and create additional users

### 4. Configuration

Update the `SECRET_KEY` in `app/auth.py` for production use:

```python
SECRET_KEY = "your-production-secret-key-here"  # Change this!
```

## Usage

### User Login

1. Navigate to `/login`
2. Enter your email and password
3. Upon successful authentication, you'll receive a JWT token
4. The token is stored in localStorage and used for subsequent requests

### Admin User Creation

**Only administrators can create new users:**

1. Log in as an administrator
2. Navigate to `/admin/create-user` (or use the "Create User" link in the navbar)
3. Fill in the user creation form:
   - First Name
   - Last Name
   - Email Address
   - Password (minimum 8 characters)
   - Admin privileges (optional)
   - Account status (active/inactive)
4. Submit the form to create the new user

### Protected Routes

The following routes now require authentication:
- `/api/dashboard` - User dashboard
- `/api/systems` - System management
- `/api/activity` - Activity feed
- `/admin/create-user` - Admin-only user creation

### Logout

Users can logout by:
- Clicking the logout button in the user dropdown menu
- The logout clears the stored JWT token and redirects to home

## API Endpoints

### Authentication Endpoints

#### POST `/api/login`
Authenticates a user and returns a JWT token.

**Request Body:**
```form-data
username: user@example.com
password: userpassword
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### POST `/api/admin/create-user`
Creates a new user account (admin only).

**Request Body:**
```form-data
first_name: John
last_name: Doe
email: john@example.com
password: securepassword
is_admin: false
is_active: true
```

**Response:**
```json
{
  "message": "User created successfully"
}
```

### Protected Endpoints

All protected endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## File Structure

```
app/
├── auth.py                 # Authentication utilities and JWT handling
├── main.py                 # Main application with auth endpoints
├── templates/
│   ├── login.html         # Login page template
│   ├── admin_create_user.html  # Admin-only user creation template
│   ├── navbar.html        # Updated navbar with auth status and admin features
│   └── index.html         # Updated home page with auth buttons
└── db/
    └── db_models/
        └── user.py        # User model with password_hash and is_admin fields

create_admin.py             # Script to create the first admin user
```

## Security Considerations

### Production Deployment

1. **Change the SECRET_KEY**: Update the secret key in `app/auth.py`
2. **Use HTTPS**: Always use HTTPS in production
3. **Environment Variables**: Store sensitive configuration in environment variables
4. **Rate Limiting**: Consider implementing rate limiting for login attempts
5. **Password Policy**: Enforce strong password requirements
6. **Admin Access Control**: Regularly review admin user privileges

### Token Management

- JWT tokens expire after 30 minutes (configurable)
- Tokens are stored in localStorage (consider httpOnly cookies for enhanced security)
- Implement token refresh mechanism for long sessions

### Admin Security

- Limit the number of admin users
- Use strong passwords for admin accounts
- Consider implementing two-factor authentication for admin accounts
- Regular audit of admin user activities

## Initial Setup

### 1. Run Dependencies Installation
```bash
python install_deps.py
```

### 2. Create First Admin User
```bash
python create_admin.py
```

### 3. Start the Application
```bash
uvicorn app.main:app --reload
```

### 4. Access the System
- **Home**: `http://localhost:8000/`
- **Login**: `http://localhost:8000/login`
- **Admin Panel**: `http://localhost:8000/admin/create-user` (after admin login)

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Database Errors**: Check that the User model includes the `password_hash` and `is_admin` fields
3. **Authentication Failures**: Verify email/password combinations
4. **Admin Access Denied**: Ensure the user has `is_admin=True` in the database
5. **Token Issues**: Check browser localStorage for stored tokens

### Debug Mode

Enable debug logging by setting environment variables:

```bash
export PYTHONPATH=.
export DEBUG=1
```

## Future Enhancements

- [ ] Password reset functionality
- [ ] Email verification
- [ ] Two-factor authentication
- [ ] Role-based access control (beyond just admin/user)
- [ ] Session management dashboard
- [ ] Audit logging for authentication events
- [ ] User management dashboard for admins
- [ ] Bulk user import/export functionality

## Support

For issues or questions about the authentication system, please check:
1. The application logs for error messages
2. Browser console for JavaScript errors
3. Network tab for API request/response details
4. Database schema for missing fields
5. Admin user privileges in the database
