# 🚀 How to Run the Django Voting System

## Step-by-Step Guide

### 📋 Prerequisites Check

Make sure you have:
- ✅ Python installed (3.8 or higher)
- ✅ Git installed
- ✅ Code cloned from GitHub

---

## 🎯 Quick Start (5 Minutes)

### Step 1: Open Terminal/Command Prompt
- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **Mac/Linux**: Open Terminal

### Step 2: Navigate to Project Folder
```bash
cd D:\VOTING
```

### Step 3: Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**You should see `(venv)` in your terminal**

### Step 4: Install Dependencies (If not already installed)
```bash
pip install -r requirements.txt
```

### Step 5: Run Database Migrations
```bash
python manage.py migrate
```

### Step 6: Create Admin User (If not already done)
```bash
python manage.py createsuperuser
```

Enter when prompted:
- Username: `admin` (or any username you prefer)
- Email: `admin@example.com` (optional)
- Password: Choose a secure password

### Step 7: Start the Server
```bash
python manage.py runserver
```

**You should see:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 8: Open in Browser
- **Home Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 🎉 That's It! Your System is Running!

---

## 📖 Next: Add Some Data

### Option 1: Via Admin Panel (Recommended)

1. **Go to Admin**: http://127.0.0.1:8000/admin/
2. **Login** with your admin credentials
3. **Add Candidates**:
   - Click "Candidates" → "Add Candidate"
   - Enter:
     - Name: `John Doe`
     - Party: `Democratic Party`
   - Click "Save"
   - Repeat for more candidates:
     - Name: `Jane Smith`, Party: `Republican Party`
     - Name: `Bob Johnson`, Party: `Independent`

### Option 2: Via Python Shell (Advanced)

```bash
python manage.py shell
```

Then in the shell:
```python
from votes_app.models import Candidate

# Create candidates
Candidate.objects.create(name="John Doe", party="Democratic Party")
Candidate.objects.create(name="Jane Smith", party="Republican Party")
Candidate.objects.create(name="Bob Johnson", party="Independent")

# Exit
exit()
```

---

## 🗳️ Test the Voting System

### 1. Go to Home Page
http://127.0.0.1:8000/

### 2. Cast a Vote
- Enter Voter UID: `V001`
- Enter Your Name: `Alice`
- Select a candidate
- Click "Submit Vote"

### 3. Cast More Votes
Try different UIDs:
- V002, V003, V004, etc.
- Vote for different candidates

### 4. View Results
Click "View Results" on home page or go to:
http://127.0.0.1:8000/results/

### 5. View Analytics
Click "Analytics" or go to:
http://127.0.0.1:8000/analytics/

### 6. Test Duplicate Prevention
Try voting again with the same UID (e.g., V001)
- You should see an error message!

---

## 🔧 Troubleshooting

### Problem: "Module not found" or Import Error
**Solution**: Activate virtual environment
```bash
venv\Scripts\activate  # Windows
```

### Problem: "No module named django"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Problem: "Database is locked" or SQLite error
**Solution**: Close any other Python processes, then:
```bash
python manage.py migrate
```

### Problem: Port 8000 already in use
**Solution**: Use a different port
```bash
python manage.py runserver 8001
```
Then access: http://127.0.0.1:8001/

### Problem: Can't see candidates when voting
**Solution**: Add candidates first via admin panel

### Problem: "Superuser already exists"
**Solution**: That's fine! Just login with existing credentials

---

## 🎯 Common Commands Reference

### Start/Stop Server
```bash
# Start
python manage.py runserver

# Stop
Press CTRL+C (or CTRL+BREAK on Windows)
```

### Admin Commands
```bash
# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Run checks
python manage.py check
```

### Database Commands
```bash
# Apply migrations
python manage.py migrate

# Create migrations (if you change models)
python manage.py makemigrations
```

### Virtual Environment
```bash
# Activate
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Deactivate
deactivate
```

---

## 📚 Quick Links

- **Home Page**: http://127.0.0.1:8000/
- **Results**: http://127.0.0.1:8000/results/
- **Analytics**: http://127.0.0.1:8000/analytics/
- **Admin**: http://127.0.0.1:8000/admin/

---

## ✅ Checklist

Use this to verify everything works:

- [ ] Server starts without errors
- [ ] Home page loads
- [ ] Can access admin panel
- [ ] Can add candidates
- [ ] Can cast votes
- [ ] Can view results
- [ ] Can view analytics/charts
- [ ] Can export CSV
- [ ] Duplicate prevention works

---

## 💡 Tips

1. **Keep the terminal open** while server is running
2. **Use separate terminals** for:
   - One for running server
   - One for admin commands
3. **Refresh browser** after adding candidates
4. **Check the terminal** for error messages
5. **Read the README.md** for more details

---

## 🎓 Learning More

- 📖 Read: `README.md` for full documentation
- ⚡ Quick: `QUICKSTART.md` for fast reference
- 🚀 Getting: `GETTING_STARTED.md` for overview

---

## 🎉 Success!

If you see the voting form, congratulations! Your Django Voting System is working perfectly!

**Need Help?**
- Check `README.md` for troubleshooting
- Review error messages in terminal
- Check Django documentation: https://docs.djangoproject.com

---

**Happy Voting! 🗳️**

