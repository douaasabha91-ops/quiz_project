# Quick Start Guide - Get Running in 5 Minutes

## ⚡ Prerequisites Check

Before starting, verify you have:
- ✅ Python 3.9+ installed
- ✅ PostgreSQL 12+ installed and running
- ✅ PostgreSQL password known

---

## 🚀 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)

Open terminal in the `quiz_project` folder and run:

```bash
pip install streamlit pandas plotly "psycopg[binary]" python-dotenv
```

**Alternative:** Run the automated script
```bash
setup_windows.bat
```

### Step 2: Set Up Database (1 minute)

```bash
setup_database.bat
```

Enter your PostgreSQL password when prompted.

**Manual alternative:**
```bash
psql -U postgres -c "CREATE DATABASE quiz_system;"
psql -U postgres -d quiz_system -f schema.sql
```

### Step 3: Configure Password (30 seconds)

Edit `.env` file and change the password:

```env
DB_PASSWORD=your_actual_postgres_password
```

### Step 4: Run Application (30 seconds)

```bash
python -m streamlit run app.py
```

The app opens at `http://localhost:8501`

### Step 5: Test It (1 minute)

1. Click "Login as Presenter"
2. Enter name: "Teacher"
3. Create a test quiz
4. Open incognito window
5. Login as "Student"
6. Join and answer!

---

## 🎯 That's It!

Your quiz system is now running with all features:
- ✅ Participant tracking
- ✅ Answer locking
- ✅ Real-time results
- ✅ Interactive charts

---

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Check [FEATURES.md](FEATURES.md) for all capabilities
- See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions

---

## 🆘 Quick Troubleshooting

**Problem:** Dependencies fail to install
```bash
# Use Anaconda instead
conda create -n quiz_system python=3.11
conda activate quiz_system
conda install -c conda-forge streamlit pandas plotly python-dotenv psycopg2
```

**Problem:** Database connection fails
- Check PostgreSQL is running
- Verify password in `.env` matches PostgreSQL password

**Problem:** Streamlit won't start
```bash
# Try with full path
python -m streamlit run app.py
```

---

## 📊 File Checklist

Ensure you have all these files:

- [x] app.py
- [x] database.py
- [x] schema.sql
- [x] requirements.txt
- [x] .env (configured with your password)
- [x] setup_database.bat
- [x] setup_windows.bat
- [x] README.md
- [x] FEATURES.md
- [x] SETUP_GUIDE.md
- [x] PROJECT_SUMMARY.md

**All files present!** ✅

---

**Ready to demo!** 🎉
