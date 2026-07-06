# 🎓 MentorApp - College Mentorship Platform

A professional Django-based mentorship platform for college students, featuring secure authentication, cloud database integration, and modern UI.

---

## ✨ Features

### 🔐 Authentication & Security
- Secure user registration with email validation
- Strong password enforcement (8+ chars, uppercase, lowercase, numbers, special)
- Real-time password strength meter
- Secure password reset with verification
- Session-based authentication
- Admin panel access

### 🎨 Professional UI/UX
- Dark blue institutional color scheme (#1a3a52)
- College-branded landing page
- Responsive design
- Clean, modern typography
- Password strength indicators
- Smooth user experience

### 📊 Database
- Cloud-hosted PostgreSQL via Neon
- Auto-backups and security
- Scalable architecture
- SSL/TLS encrypted connections

### 📱 College-Focused Apps
- **Accounts** - User management
- **Students** - Student profiles
- **Academic** - Academic tracking
- **Career Guidance** - Career resources
- **Meetings** - Mentor-student meetings
- **Activity** - User activities
- **Chatbot** - AI assistant

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip or conda
- Git
- Neon account (free: https://console.neon.tech)

### Installation (5 minutes)

#### 1. Clone or Download Project
```bash
cd your-project-directory
```

#### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Setup Neon Database

**A. Create Neon Account**
```
1. Go to https://console.neon.tech
2. Sign up with email/Google/GitHub
3. Create project "mentorapp"
4. Get connection string
```

**B. Configure .env**
```bash
# Edit .env file and add your Neon credentials
DATABASE_URL=postgresql://username:password@ep-xxxxx.neon.tech/neondb
```

Or use individual variables:
```env
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=your_password_here
DB_HOST=ep-xxxxx.neon.tech
DB_PORT=5432
```

#### 5. Run Migrations
```bash
python manage.py migrate
```

#### 6. Create Admin Account
```bash
python manage.py createsuperuser
```

#### 7. Start Development Server
```bash
python manage.py runserver
```

#### 8. Access the App
- **Landing Page:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

---

## 📋 Project Structure

```
mentorapp/
├── mentorapp/
│   ├── settings.py          # Django configuration (PostgreSQL setup)
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── accounts/
│   ├── models.py            # User models
│   ├── views.py             # Authentication views
│   ├── forms.py             # Form validation
│   ├── urls.py              # Account URLs
│   └── migrations/          # Database schema
├── templates/
│   ├── home.html            # Landing page
│   ├── login.html           # Login form
│   ├── register.html        # Registration form
│   └── forgot_password.html # Password reset
├── static/                  # CSS, JS, images
├── media/                   # User uploads
├── manage.py                # Django management
├── .env                     # Environment variables
├── .gitignore               # Git ignore rules
└── requirements.txt         # Python dependencies
```

---

## 🔧 Configuration

### Environment Variables (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@host/database
# OR use individual variables:
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=your_password
DB_HOST=ep-xxxxx.neon.tech
DB_PORT=5432

# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `INTEGRATION_SUMMARY.md` | Project overview and status |
| `NEON_TESTING_GUIDE.md` | Step-by-step testing instructions |
| `NEON_QUICK_REFERENCE.txt` | Quick command reference |
| `QUICK_START_NEON.md` | 5-minute setup guide |
| `NEON_DATABASE_SETUP.md` | Comprehensive database setup |
| `NEON_FAQ_TROUBLESHOOTING.md` | Common issues and solutions |
| `SETUP_FLOWCHART.md` | Visual setup flowchart |

---

## 🧪 Testing

### Test User Registration
```bash
python manage.py runserver
# Visit http://127.0.0.1:8000/
# Click Sign Up and create account
```

### Test User Login
```bash
# Use credentials from registration
# Visit http://127.0.0.1:8000/login/
```

### Test Admin Panel
```bash
# Visit http://127.0.0.1:8000/admin/
# Login with superuser credentials
```

### Run Django Tests
```bash
python manage.py test
```

---

## 🌐 Neon PostgreSQL Setup

### What is Neon?
Neon is a managed PostgreSQL database service:
- ✅ Free tier (0.5 GB storage)
- ✅ Cloud-hosted (no local installation)
- ✅ Auto-backups
- ✅ SSL/TLS encryption
- ✅ Easy scaling

### Why PostgreSQL?
- Production-ready
- Scalable
- Reliable
- Better than SQLite for production
- Industry standard

### Neon Free Tier Limits
- 3 projects
- 0.5 GB storage
- 1 compute unit
- Projects suspend after 7 days idle

### Resume Suspended Project
1. Go to https://console.neon.tech
2. Find suspended project
3. Click "Resume"
4. Wait 30 seconds

---

## 🔒 Security

### Implemented
- ✅ SSL/TLS database connections
- ✅ Strong password validation
- ✅ CSRF protection
- ✅ Session-based authentication
- ✅ Environment variable secrets
- ✅ SQL injection prevention

### Recommended for Production
- [ ] Change DEBUG=False
- [ ] Use strong SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up HTTPS
- [ ] Configure email backend
- [ ] Set up static file serving
- [ ] Regular backups

---

## 📱 Mobile Support

The app is responsive and works on:
- ✅ Desktop browsers
- ✅ Tablets
- ✅ Mobile phones

---

## 🐛 Troubleshooting

### Connection Issues
See `NEON_FAQ_TROUBLESHOOTING.md` for common solutions.

### Common Errors
- **"password authentication failed"** → Check .env credentials
- **"could not translate host name"** → Verify hostname in .env
- **"database does not exist"** → Check database name in Neon console
- **"psycopg2 module not found"** → Run `pip install -r requirements.txt`

### Debug Mode
```bash
# Enable verbose output
python manage.py migrate --verbosity=3

# Test database connection
python manage.py dbshell

# Check configuration
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DATABASES)
```

---

## 🚀 Deployment

### Prepare for Production
1. Set `DEBUG=False` in `.env`
2. Generate new `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Set up email backend
5. Configure static files
6. Set up HTTPS/SSL

### Deploy Options
- **Heroku** - Easy deployment, free tier available
- **PythonAnywhere** - Python-focused hosting
- **Railway** - Modern deployment platform
- **AWS** - Scalable cloud platform
- **DigitalOcean** - Simple VPS hosting

---

## 📊 Database Migrations

### Create New Migration
```bash
python manage.py makemigrations app_name
```

### Apply Migrations
```bash
python manage.py migrate
```

### Check Status
```bash
python manage.py showmigrations
```

### Rollback Migration
```bash
python manage.py migrate app_name 0001
```

---

## 👥 Contributing

Contributions welcome! Please:
1. Create a new branch
2. Make changes
3. Test thoroughly
4. Submit pull request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👨‍💼 Support

### Documentation
- Read the documentation files (*.md)
- Check `NEON_FAQ_TROUBLESHOOTING.md` for issues

### Contact
- For Neon issues: https://neon.tech/docs
- For Django issues: https://docs.djangoproject.com

---

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ User authentication
- ✅ Professional UI
- ✅ Neon PostgreSQL integration

### Phase 2
- [ ] Mentor-student matching
- [ ] Meeting scheduling
- [ ] Real-time chat
- [ ] Notifications

### Phase 3
- [ ] Mobile app (React Native)
- [ ] Video conferencing
- [ ] AI chatbot
- [ ] Analytics dashboard

---

## ✨ Tech Stack

### Backend
- Django 5.2.15
- PostgreSQL (via Neon)
- psycopg2-binary

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap (optional)

### Database
- Neon PostgreSQL
- SSL/TLS encryption

### Tools
- Git
- Python 3.10+
- pip

---

## 📊 Statistics

- **Lines of Code:** 1000+
- **Database Tables:** 15+
- **API Endpoints:** 10+
- **Frontend Pages:** 5+

---

## 🎉 Getting Started

**Estimated setup time: 13 minutes**

1. Follow "Quick Start" section above
2. Read `NEON_TESTING_GUIDE.md` for detailed steps
3. Create Neon account and get connection string
4. Update `.env` file
5. Run migrations
6. Start server
7. Test!

---

## 🙏 Acknowledgments

- Django framework
- Neon PostgreSQL
- Bootstrap framework
- Python community

---

## 📞 Questions?

Check the documentation files:
- `NEON_TESTING_GUIDE.md` - Detailed setup
- `NEON_FAQ_TROUBLESHOOTING.md` - Common issues
- `INTEGRATION_SUMMARY.md` - Project overview

---

**Happy coding! 🚀**

Last updated: July 2026
