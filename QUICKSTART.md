# Quick Start Guide - Django Voting System

## 🚀 Quick Setup (5 minutes)

### 1. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac  
source venv/bin/activate
```

### 2. Start the Server
```bash
python manage.py runserver
```

### 3. Open in Browser
- **Home**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/
  - Username: `admin`
  - Password: (set during creation)

## 📝 Basic Usage

### Add Candidates (via Admin)
1. Go to http://127.0.0.1:8000/admin/
2. Click "Candidates" → "Add Candidate"
3. Fill in:
   - Name: `John Doe`
   - Party: `Democratic Party`
4. Click "Save"

**Example Candidates:**
- John Doe - Democratic Party
- Jane Smith - Republican Party  
- Bob Johnson - Independent

### Cast Votes
1. Go to http://127.0.0.1:8000/
2. Enter Voter UID: `V001`
3. Enter Name: `Alice`
4. Select a candidate
5. Click "Submit Vote"

### View Results
1. Click "View Results" on home page
   OR
2. Go to http://127.0.0.1:8000/results/

### View Analytics
1. Click "Analytics" on home page
   OR
2. Go to http://127.0.0.1:8000/analytics/

### Export Data
1. On results page, click "📥 Export CSV"
   OR
2. Go to http://127.0.0.1:8000/export/

## 🧪 Test Scenario

### Quick Demo
```bash
# Add 3 candidates via admin
# Then cast these votes:

Voter UID: V001, Candidate: John Doe
Voter UID: V002, Candidate: Jane Smith
Voter UID: V003, Candidate: John Doe
Voter UID: V004, Candidate: Bob Johnson

# View results and analytics
```

## 🔍 URLs Reference

| URL | Description |
|-----|-------------|
| `/` | Home page - voting form |
| `/vote/` | Process vote (POST) |
| `/results/` | View voting results |
| `/analytics/` | View statistics and charts |
| `/chart/` | Generate chart (JSON API) |
| `/export/` | Download CSV |
| `/admin/` | Admin panel |

## 🛠️ Admin Commands

```bash
# Create superuser
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run checks
python manage.py check

# Access Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

## 📊 Features Checklist

- ✅ Vote form with candidate selection
- ✅ Duplicate vote prevention
- ✅ Results display with percentages
- ✅ Analytics with mean/median
- ✅ Matplotlib charts
- ✅ CSV export
- ✅ Admin CRUD operations
- ✅ Modern UI with CSS
- ✅ Responsive design

## 🐛 Troubleshooting

### Import Errors
```bash
# Make sure venv is activated
venv\Scripts\activate  # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Database Issues
```bash
# Delete old database
del db.sqlite3  # Windows
rm db.sqlite3   # Linux/Mac

# Recreate database
python manage.py migrate

# Recreate superuser
python manage.py createsuperuser
```

### Server Not Starting
```bash
# Check for port conflicts
# Use different port:
python manage.py runserver 8001
```

## 📚 Next Steps

1. Add more candidates via admin
2. Cast votes with different UIDs
3. Explore the analytics dashboard
4. Export data and analyze
5. Customize templates and styling
6. Add new features

---

**Need Help?** Check `README.md` for full documentation.

