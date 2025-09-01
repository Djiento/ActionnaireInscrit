# Investor Registration Platform

## Overview

This is a Flask-based web application for managing investor registrations. The platform allows potential investors to register by providing personal information, investment preferences, and identity documents. It includes an admin dashboard for managing registrations and a WhatsApp group integration for investor communication.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with SQLAlchemy ORM for database operations
- **Authentication**: Flask-Login for session management with admin-only access
- **Database**: SQLite for development with support for PostgreSQL in production via environment variables
- **File Handling**: Werkzeug for secure file uploads with UUID-based naming for identity documents
- **Forms**: Flask-WTF with WTForms for form validation and CSRF protection

### Database Schema
- **Admin Model**: User management with username, email, and hashed passwords
- **Investor Model**: Core entity storing registration data including personal info, investment preferences, and document references
- **Settings Model**: Configuration storage for WhatsApp group links and other platform settings

### Frontend Architecture
- **Template Engine**: Jinja2 with Bootstrap 5 for responsive UI components
- **Styling**: Custom CSS with CSS variables for theming and responsive design
- **JavaScript**: Vanilla JavaScript for form validation, file upload handling, and user interactions
- **Icons**: Font Awesome for consistent iconography

### Security Features
- **File Upload Security**: Restricted file types (PDF, JPG, JPEG, PNG) with secure filename handling
- **CSRF Protection**: Built-in Flask-WTF CSRF tokens on all forms
- **Password Security**: Werkzeug password hashing for admin accounts
- **Session Management**: Secure session handling with configurable secret keys

### File Storage
- **Upload Directory**: Local filesystem storage for identity documents
- **File Naming**: UUID-based naming to prevent conflicts and enhance security
- **Size Limits**: 16MB maximum file size for document uploads

### Admin Features
- **Dashboard**: Statistics overview with total investors and estimated investment amounts
- **Data Export**: CSV export functionality for investor data
- **Search and Filter**: Real-time search capabilities for investor management
- **WhatsApp Integration**: Configurable group invite links for investor communication

## External Dependencies

### Python Packages
- **Flask**: Web framework and core application structure
- **Flask-SQLAlchemy**: Database ORM and model management
- **Flask-Login**: User session and authentication management
- **Flask-WTF**: Form handling and validation with CSRF protection
- **WTForms**: Form field validation and rendering
- **Werkzeug**: Security utilities for password hashing and file handling

### Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design and UI components
- **Font Awesome 6**: Icon library for user interface elements
- **Vanilla JavaScript**: Client-side functionality without additional frameworks

### Database Support
- **SQLite**: Default development database (file-based)
- **PostgreSQL**: Production database support via DATABASE_URL environment variable

### Third-Party Integrations
- **WhatsApp**: Group invitation links for investor communication (configured via admin settings)
- **File System**: Local storage for uploaded identity documents

### Environment Configuration
- **SESSION_SECRET**: Application secret key for session security
- **DATABASE_URL**: Database connection string for production deployments
- **Upload Directory**: Configurable file storage location