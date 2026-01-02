# Complete Setup Guide

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Windows Installation](#windows-installation)
3. [Database Setup](#database-setup)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Python 3.9-3.11** (3.14 also supported)
   - Download: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **PostgreSQL 12+**
   - Download: https://www.postgresql.org/download/windows/
   - Remember the password you set for the `postgres` user

3. **Git** (Optional, for version control)
   - Download: https://git-scm.com/downloads

### System Requirements

- Windows 10/11 (or Linux/Mac with PostgreSQL)
- 4GB RAM minimum
- 500MB free disk space
- Internet connection for package installation

---

## Windows Installation

### Method 1: Automated Setup (Recommended)

1. **Open Command Prompt or PowerShell** in the project directory

2. **Run the setup script:**
   ```bash
   setup_windows.bat
   ```

3. **If psycopg2 fails**, the script will automatically try psycopg3

4. **Wait for installation** to complete

### Method 2: Manual Installation

1. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

2. **Install packages one by one:**
   ```bash
   pip install streamlit
   pip install python-dotenv
   pip install pandas
   pip install plotly
   pip install "psycopg[binary]"
   ```

### Method 3: Using Anaconda (Most Reliable)

1. **Install Miniconda:**
   - Download: https://docs.conda.io/en/latest/miniconda.html

2. **Create environment:**
   ```bash
   conda create -n quiz_system python=3.11
   conda activate quiz_system
   ```

3. **Install packages:**
   ```bash
   conda install -c conda-forge streamlit pandas plotly python-dotenv psycopg2
   ```

### Verify Installation

```bash
python -c "import streamlit, pandas, plotly, psycopg, dotenv; print('All packages installed successfully!')"
```

---

## Database Setup

### Step 1: Start PostgreSQL

**Check if PostgreSQL is running:**
```bash
pg_isready
```

**If not running**, start it from Windows Services:
1. Press `Win + R`
2. Type `services.msc`
3. Find "postgresql-x64-[version]"
4. Right-click → Start

### Step 2: Create Database

**Option A: Automated (Windows)**
```bash
setup_database.bat
```
- Enter your PostgreSQL password when prompted
- Script will create database and load schema

**Option B: Manual**

1. **Connect to PostgreSQL:**
   ```bash
   psql -U postgres
   ```

2. **Create database:**
   ```sql
   CREATE DATABASE quiz_system;
   ```

3. **Exit psql:**
   ```sql
   \q
   ```

4. **Load schema:**
   ```bash
   psql -U postgres -d quiz_system -f schema.sql
   ```

### Step 3: Verify Database

```bash
# Connect to database
psql -U postgres -d quiz_system

# List tables
\dt

# Should see: users, quizzes, questions, sessions, responses

# Exit
\q
```

---

## Configuration

### Step 1: Create Environment File

```bash
# Copy the example file
copy .env.example .env
```

### Step 2: Edit Configuration

Open `.env` in a text editor (Notepad, VS Code, etc.) and update:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=quiz_system
DB_USER=postgres
DB_PASSWORD=your_actual_password_here
```

**Important:** Replace `your_actual_password_here` with your PostgreSQL password

### Step 3: Verify Configuration

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('DB Config:', os.getenv('DB_NAME'))"
```

Should output: `DB Config: quiz_system`

---

## Running the Application

### Start the Application

```bash
python -m streamlit run app.py
```

**Alternative (if streamlit is in PATH):**
```bash
streamlit run app.py
```

### Expected Output

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Access the Application

Open your browser and go to: `http://localhost:8501`

### Stop the Application

Press `Ctrl + C` in the terminal

---

## Testing

### Quick Functionality Test

**1. Test Presenter Interface:**

```bash
# Start the app
python -m streamlit run app.py
```

- Click "Login as Presenter"
- Enter name: "Test Teacher"
- Create a quiz: "Sample Quiz"
- Add 2 questions with different options
- Launch a session
- Note the session code

**2. Test Participant Interface:**

- Open a **new incognito/private browser window**
- Go to `http://localhost:8501`
- Click "Login as Participant"
- Enter name: "Test Student"
- Enter the session code
- Answer the questions
- Try to change answer → Should be locked ✅

**3. Test Results View:**

- Go back to presenter window
- Click "View Results" in sidebar
- Select your session
- Verify you see:
  - Bar chart ✅
  - Participant name "Test Student" ✅
  - Correct/incorrect indicators ✅

### Multi-Participant Test

**1. Open 4 browser windows (incognito):**
- Window 1: Presenter
- Windows 2-4: Participants (Alice, Bob, Carol)

**2. Presenter (Window 1):**
- Create quiz with 2-3 questions
- Launch session → get code

**3. Participants (Windows 2-4):**
- Each login as participant with different name
- Each join with session code
- Each answer questions (choose different answers)

**4. Verify Results (Window 1):**
- View Results
- Should see all participant names grouped by answer
- Verify counts match

---

## Troubleshooting

### Installation Issues

#### Problem: `pip install` fails with permission error

**Solution:**
```bash
pip install --user streamlit pandas plotly "psycopg[binary]" python-dotenv
```

#### Problem: `psycopg2-binary` build fails

**Solution:** Use psycopg3 instead
```bash
pip install "psycopg[binary]"
```

#### Problem: Microsoft Visual C++ required

**Solutions:**
1. Install Visual Studio Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Or use Anaconda (recommended)

### Database Issues

#### Problem: `pg_isready` command not found

**Solution:** Add PostgreSQL to PATH
```bash
# Add this to your PATH environment variable:
C:\Program Files\PostgreSQL\[version]\bin
```

#### Problem: Password authentication failed

**Solution:**
1. Verify password in `.env` matches PostgreSQL password
2. Try resetting PostgreSQL password:
   ```bash
   psql -U postgres
   ALTER USER postgres WITH PASSWORD 'newpassword';
   ```

#### Problem: Database "quiz_system" does not exist

**Solution:**
```bash
psql -U postgres -c "CREATE DATABASE quiz_system;"
psql -U postgres -d quiz_system -f schema.sql
```

#### Problem: Connection refused (port 5432)

**Solution:**
1. Check if PostgreSQL is running
2. Verify port in PostgreSQL config (postgresql.conf)
3. Check Windows Firewall settings

### Application Issues

#### Problem: Streamlit shows blank page

**Solution:**
1. Clear browser cache
2. Try a different browser
3. Check terminal for errors
4. Verify all dependencies installed

#### Problem: Cannot see participant names in results

**Solution:**
1. Refresh the page (F5)
2. Verify participants actually submitted answers
3. Check database: `SELECT * FROM responses;`
4. Verify `get_question_responses_detailed()` function exists in database.py

#### Problem: Answers not locking

**Solution:**
1. Clear browser cache
2. Check database.py has updated `submit_response()` function
3. Verify database constraint exists:
   ```sql
   \d responses
   -- Should show UNIQUE constraint on (question_id, user_id, session_id)
   ```

#### Problem: Import errors

**Solution:**
```bash
# Reinstall specific package
pip uninstall streamlit
pip install streamlit

# Or reinstall all
pip install -r requirements.txt --force-reinstall
```

### Performance Issues

#### Problem: Slow page loads

**Solution:**
1. Check PostgreSQL performance
2. Ensure indexes exist on responses table
3. Limit number of active sessions

#### Problem: Memory issues

**Solution:**
1. Close unnecessary browser tabs
2. Restart Streamlit application
3. Check database connections are being closed properly

---

## Advanced Configuration

### Custom Port

```bash
# Run on different port
streamlit run app.py --server.port 8502
```

### Production Deployment

```bash
# Run with production settings
streamlit run app.py --server.headless true --server.port 80
```

### Database Connection Pooling

Edit `database.py` to add connection pooling for better performance in production.

---

## Useful Commands

### Database Commands

```bash
# Connect to database
psql -U postgres -d quiz_system

# List all tables
\dt

# View table structure
\d responses

# Count responses
SELECT COUNT(*) FROM responses;

# View active sessions
SELECT * FROM sessions WHERE is_active = TRUE;

# Exit
\q
```

### Application Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Update a package
pip install --upgrade streamlit

# Create virtual environment
python -m venv venv
venv\Scripts\activate
```

---

## Backup and Restore

### Backup Database

```bash
# Backup entire database
pg_dump -U postgres quiz_system > backup.sql

# Backup with custom format
pg_dump -U postgres -Fc quiz_system > backup.dump
```

### Restore Database

```bash
# Restore from SQL file
psql -U postgres quiz_system < backup.sql

# Restore from custom format
pg_restore -U postgres -d quiz_system backup.dump
```

---

## Next Steps

After successful setup:

1. ✅ Read the [README.md](README.md) for full documentation
2. ✅ Test all features with multiple participants
3. ✅ Create your demo quiz
4. ✅ Record demo video (2-5 minutes)
5. ✅ Prepare project submission

---

## Support Resources

- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Streamlit Documentation**: https://docs.streamlit.io/
- **Python Documentation**: https://docs.python.org/3/
- **psycopg3 Documentation**: https://www.psycopg.org/psycopg3/docs/

---

## Quick Reference

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Set up database | `setup_database.bat` |
| Run application | `python -m streamlit run app.py` |
| Check database | `psql -U postgres -d quiz_system` |
| Backup database | `pg_dump -U postgres quiz_system > backup.sql` |

---

**Setup Complete!** 🎉

You're ready to use the Interactive Quiz System!
