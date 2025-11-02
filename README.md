# 🗳️ Django Voting System

A comprehensive web-based voting system built with Django that allows registered voters to cast votes for candidates and view real-time analytics and results.

## 📋 Features

- **Secure Voting**: One vote per voter with duplicate prevention
- **Real-time Results**: Live voting results with percentages and visualizations
- **Analytics Dashboard**: Statistical analysis using numpy and pandas
- **Interactive Charts**: Dynamic matplotlib-generated bar charts
- **CSV Export**: Export voting data for external analysis
- **Admin Panel**: Full CRUD operations for all models
- **Modern UI**: Beautiful, responsive web interface

## 🛠️ Technology Stack

- **Backend**: Django 5.2.7 (Python 3.13)
- **Data Analysis**: numpy, pandas
- **Visualization**: matplotlib
- **Database**: SQLite
- **Frontend**: Django Templates with modern CSS

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd D:\VOTING
   ```

2. **Activate the virtual environment** (if not already active):
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (if not already created):
   ```bash
   python manage.py createsuperuser
   ```
   - Username: admin
   - Email: admin@example.com
   - Password: (set during creation)

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Home page: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 🎯 Usage Guide

### Admin Panel

1. Navigate to http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials
3. Add Candidates:
   - Go to "Candidates" → "Add Candidate"
   - Enter name and party
   - Save
4. Add Voters (optional):
   - Go to "Voters" → "Add Voter"
   - Enter UID and name
   - Save

### Voting Process

1. Go to http://127.0.0.1:8000/
2. Enter your Voter UID
3. Enter your name (optional)
4. Select a candidate
5. Click "Submit Vote"
6. View results or analytics

### Features Overview

#### Home Page (`/`)
- Voting form with candidate selection
- Voter UID lookup
- Quick navigation to results and analytics

#### Results Page (`/results/`)
- Total vote count
- Votes per candidate
- Percentage breakdown
- Visual progress bars
- CSV export button

#### Analytics Page (`/analytics/`)
- Statistical metrics (mean, median)
- Interactive matplotlib bar chart
- Detailed candidate breakdown

#### CSV Export (`/export/`)
- Downloads all votes as CSV
- Includes voter, candidate, and timestamp data

#### Chart Generation (`/chart/`)
- API endpoint returning base64-encoded chart
- Used dynamically by analytics page

## 🗄️ Database Models

### Candidate
- `name`: Full name of candidate
- `party`: Political party affiliation
- `created_at`: Timestamp of creation

### Voter
- `uid`: Unique voter identifier
- `name`: Full name of voter
- `registered_on`: Registration timestamp

### Vote
- `voter`: Foreign key to Voter
- `candidate`: Foreign key to Candidate
- `timestamp`: When vote was cast
- **Constraint**: One vote per voter (enforced at database level)

## 🔒 Security Features

- CSRF protection on all forms
- Duplicate vote prevention
- SQL injection protection (Django ORM)
- Input validation
- Secure password handling in admin

## 📊 Analytics Features

- **Mean Votes**: Average votes per candidate
- **Median Votes**: Median votes per candidate
- **Bar Chart**: Visual representation using matplotlib
- **CSV Export**: Data export for external analysis

## 🎨 UI/UX Highlights

- Gradient backgrounds
- Responsive design
- Smooth animations
- Progress bars
- Modern card-based layouts
- Mobile-friendly

## 🧪 Testing the Application

### Sample Workflow

1. **Add Candidates via Admin:**
   - Candidate 1: John Doe - Democratic Party
   - Candidate 2: Jane Smith - Republican Party
   - Candidate 3: Bob Johnson - Independent

2. **Cast Votes:**
   - Use UID: V001, V002, V003, etc.
   - Vote for different candidates

3. **View Results:**
   - Check real-time vote counts
   - View percentages
   - Export CSV

4. **Explore Analytics:**
   - See mean/median statistics
   - View interactive chart

## 📁 Project Structure

```
voting_project/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3                 # SQLite database
├── venv/                      # Virtual environment
├── voting_project/            # Project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── votes_app/                 # Main application
    ├── models.py              # Database models
    ├── views.py               # View functions
    ├── urls.py                # URL routing
    ├── admin.py               # Admin configuration
    └── templates/
        └── votes_app/
            ├── index.html     # Home/voting page
            ├── results.html   # Results page
            └── analytics.html # Analytics page
```

## 🚀 Deployment Notes

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Update `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Set up static file serving
5. Use HTTPS
6. Implement proper user authentication
7. Add rate limiting
8. Set up logging

## 🤝 Contributing

This is a demo project. Feel free to extend with:
- User authentication
- Email notifications
- Real-time updates
- Advanced analytics
- Social media integration

## 📝 License

This project is for educational purposes.

## 👨‍💻 Author

Created with Django 5.2.7 and Python 3.13

---

**Enjoy voting! 🗳️**

