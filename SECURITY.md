# Security Guidelines

## Environment Setup

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Configure secure credentials in `.env`:**
   ```env
   DB_PASSWORD=your_secure_database_password
   SECRET_KEY=your-very-long-random-secret-key-at-least-32-characters
   ADMIN_USERNAME=your_secure_admin_username
   ADMIN_PASSWORD=your_secure_admin_password
   ```

3. **Generate secure secret key:**
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

## Security Measures Implemented

- ✅ Environment variables for sensitive data
- ✅ Input validation and sanitization
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Path traversal prevention
- ✅ CSRF protection
- ✅ Resource leak prevention
- ✅ Error handling without information disclosure

## Production Deployment

1. Set `FLASK_DEBUG=False`
2. Use HTTPS
3. Secure database credentials
4. Monitor application logs
5. Regular security updates

## File Security

- **Never commit `.env` file**
- **Keep `.env.example` as template**
- **Wordcloud images are auto-generated**
- **Upload directory secured**