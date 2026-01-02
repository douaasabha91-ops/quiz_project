# Interactive Quiz System - ClassPoint Alternative

A professional interactive quiz application built with Python, Streamlit, and PostgreSQL. This system allows presenters to create quizzes, launch interactive sessions, and track individual participant responses in real-time.

## 🌟 Key Features

### For Presenters
- ✅ Create multiple-choice quizzes (2-4 answer options)
- ✅ Launch sessions with unique 6-character codes
- ✅ **Track individual participant responses** - See who chose each answer
- ✅ View real-time results with interactive Plotly charts
- ✅ Monitor accuracy and performance metrics
- ✅ Manage multiple active sessions

### For Participants
- ✅ Join sessions easily with session codes
- ✅ Answer multiple-choice questions
- ✅ **Answer locking** - Cannot change answers after submission
- ✅ Immediate feedback on correctness
- ✅ Clean, intuitive interface

### Security & Integrity
- 🔒 **Dual-layer answer protection** - UI and database level
- 🔒 Prevents answer modification after submission
- 🔒 First response is preserved
- 🔒 Academic integrity guaranteed

## 📊 Technology Stack

- **Python 3.9-3.11** - Application logic
- **Streamlit 1.52+** - Web interface
- **PostgreSQL 12+** - Relational database
- **psycopg3** - PostgreSQL driver (Python 3.14 compatible)
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation

## 🗄️ Database Schema

```sql
users (id, name, role, created_at)
quizzes (id, title, created_by, created_at)
questions (id, quiz_id, text, option_a, option_b, option_c, option_d, correct_answer)
sessions (id, quiz_id, session_code, is_active, created_at, ended_at)
responses (id, question_id, user_id, session_id, answer, is_correct, submitted_at)
```

**Key Constraints:**
- Unique session codes
- Unique constraint on `(question_id, user_id, session_id)` - prevents duplicate responses
- Foreign key relationships for data integrity

## 🚀 Installation

### Prerequisites
- Python 3.9-3.11 (3.14 supported with psycopg3)
- PostgreSQL 12 or higher
- pip package manager

### Step 1: Install Dependencies

**Windows (Recommended):**
```bash
# Run automated setup
setup_windows.bat
```

**Manual Installation:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install packages
pip install streamlit python-dotenv pandas plotly "psycopg[binary]"
```

**Using Anaconda (Most Reliable):**
```bash
conda create -n quiz_system python=3.11
conda activate quiz_system
conda install -c conda-forge streamlit pandas plotly python-dotenv psycopg2
```

### Step 2: Set Up PostgreSQL Database

**Option A: Automated (Windows)**
```bash
setup_database.bat
```

**Option B: Manual**
```bash
# Create database
psql -U postgres -c "CREATE DATABASE quiz_system;"

# Load schema
psql -U postgres -d quiz_system -f schema.sql
```

### Step 3: Configure Environment

```bash
# Copy example file
copy .env.example .env

# Edit .env with your PostgreSQL password
```

**.env file:**
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=quiz_system
DB_USER=postgres
DB_PASSWORD=your_actual_password
```

### Step 4: Run the Application

```bash
python -m streamlit run app.py
```

The app opens at `http://localhost:8501`

## 📖 User Guide

### As a Presenter

**1. Create a Quiz**
- Login as Presenter
- Sidebar → "Create Quiz"
- Enter quiz title
- Add questions with 2-4 multiple-choice options
- Mark the correct answer
- Click "Done Adding Questions"

**2. Launch a Session**
- Sidebar → "Launch Session"
- Select your quiz
- Click "Launch Session"
- Share the 6-character session code with participants

**3. View Results**
- Sidebar → "View Results"
- Select a session
- See:
  - Interactive bar chart showing response distribution
  - **Participant names grouped by their answer choice**
  - Accuracy percentage
  - Correct/incorrect indicators

**Example Results Display:**
```
Question 1: What is 2+2?
Options: A) 3    B) 4 ✅    C) 5    D) 6

┌────────────────────┬─────────────────────────┐
│   Bar Chart        │  Participant Responses  │
│   A: 1             │  Answer B ✅ (3 people) │
│   B: 3 (green)     │  • Sarah Johnson        │
│   C: 0             │  • Mike Davis          │
│   D: 1             │  • Emily Brown         │
│   Accuracy: 60%    │                         │
│                    │  Answer A ❌ (1 person) │
│                    │  • John Smith          │
│                    │                         │
│                    │  Answer D ❌ (1 person) │
│                    │  • Tom Wilson          │
└────────────────────┴─────────────────────────┘
```

### As a Participant

**1. Join a Session**
- Login as Participant
- Enter your name
- Enter the 6-character session code
- Click "Join Session"

**2. Answer Questions**
- Read each question
- Select your answer from the radio buttons
- Click "Submit Answer"
- **Note: You cannot change your answer after submission!**

**3. View Feedback**
- After submission, you'll see:
  - Your submitted answer (read-only)
  - Whether it's correct ✅ or incorrect ❌
  - Warning that answer is locked

## 🔐 Security Features

### Answer Submission Protection

**Layer 1: UI Protection**
- Radio buttons removed after submission
- Submit button hidden
- Read-only answer display
- Clear warning message

**Layer 2: Database Protection**
```python
# Checks if response already exists
if existing:
    raise ValueError("Answer already submitted. Cannot modify response.")
```

**Benefits:**
- Prevents accidental resubmission
- Blocks programmatic manipulation
- Ensures academic integrity
- Preserves first response data

## 🎨 User Interface

### Results View Features
- Split-screen layout: Chart (60%) + Participants (40%)
- Color-coded answers: Green for correct, Blue for incorrect
- Participant names grouped by answer choice
- Count of participants per answer
- Overall accuracy metrics

### Participant View Features
- Clean question display
- Easy answer selection
- Immediate submission feedback
- Locked state after submission
- Cannot modify answers

## 🧪 Testing

### Quick Test (5 minutes)

1. **Start the application:**
   ```bash
   python -m streamlit run app.py
   ```

2. **Create a quiz (Presenter):**
   - Login as "Teacher"
   - Create quiz: "Test Quiz"
   - Add 2 questions

3. **Join as multiple participants:**
   - Open 3-4 browser windows (incognito)
   - Login as "Alice", "Bob", "Carol", "Dave"
   - Each joins the same session
   - Each answers the questions (choose different answers)

4. **Test answer locking:**
   - As Alice, submit an answer
   - Try to change it → Should be locked ✅
   - Refresh page → Still locked ✅

5. **View results (Presenter):**
   - Go to "View Results"
   - See participant names under each answer ✅

## 📂 Project Structure

```
quiz_project/
├── app.py                    # Main Streamlit application
├── database.py              # Database operations (psycopg3)
├── schema.sql               # PostgreSQL database schema
├── requirements.txt         # Python dependencies
├── .env.example            # Environment configuration template
├── .gitignore              # Git ignore rules
├── setup_database.bat      # Database setup script (Windows)
├── setup_windows.bat       # Dependencies install script (Windows)
└── README.md               # This file
```

## 🔧 Troubleshooting

### Installation Issues

**Problem:** `psycopg2-binary` build fails on Windows
```bash
# Solution: Use psycopg3 instead
pip install "psycopg[binary]"
```

**Problem:** Microsoft Visual C++ required
```bash
# Solution: Use Anaconda or install Visual Studio Build Tools
conda install -c conda-forge psycopg2
```

### Database Issues

**Problem:** Connection refused
```bash
# Check if PostgreSQL is running
pg_isready

# Or check Windows Services for postgresql service
```

**Problem:** Authentication failed
```bash
# Verify password in .env file matches PostgreSQL password
```

**Problem:** Database does not exist
```bash
# Create the database
psql -U postgres -c "CREATE DATABASE quiz_system;"
```

### Application Issues

**Problem:** Streamlit not found
```bash
# Use module syntax
python -m streamlit run app.py
```

**Problem:** Names not showing in results
```bash
# Refresh the page
# Verify participants submitted answers
# Check database connection
```

**Problem:** Answer not locking
```bash
# Clear browser cache
# Restart the application
# Verify database.py has updated submit_response() function
```

## 📊 Database Functions

### Core Functions

**User Management:**
- `create_user(name, role)` - Register new user
- `get_user_by_id(user_id)` - Retrieve user info

**Quiz Management:**
- `create_quiz(title, created_by)` - Create new quiz
- `add_question(...)` - Add question to quiz
- `get_questions_by_quiz(quiz_id)` - Get all questions

**Session Management:**
- `create_session(quiz_id)` - Generate session with unique code
- `get_session_by_code(code)` - Find session by code
- `get_active_sessions()` - List all active sessions
- `end_session(session_id)` - Close a session

**Response Management:**
- `submit_response(...)` - Submit answer (prevents resubmission)
- `get_question_results(...)` - Aggregated results
- `get_question_responses_detailed(...)` - **NEW** - Individual participant responses
- `get_user_response(...)` - Check if user answered

## 🎯 Assignment Requirements

This project fulfills all assignment requirements:

### Functional Requirements ✅
- ✅ Create multiple-choice quiz questions
- ✅ Store questions and answers in PostgreSQL
- ✅ Generate session codes for participants
- ✅ Allow participants to answer via Streamlit UI
- ✅ Display live results (bar charts and participant tracking)

### Technology Requirements ✅
- ✅ Python 3.x for application logic
- ✅ Streamlit for web interface
- ✅ PostgreSQL for database
- ✅ psycopg3 for database connectivity

### Database Design ✅
- ✅ users table (id, name, role)
- ✅ quizzes table (id, title, created_at)
- ✅ questions table (id, quiz_id, text, correct_answer)
- ✅ responses table (id, question_id, user_id, answer)
- ✅ sessions table (for session management)

### Extra Features ✅
- ✅ **Participant answer tracking** - See who chose each answer
- ✅ **Answer locking** - Cannot modify after submission
- ✅ Interactive visualizations
- ✅ Real-time updates
- ✅ Session management
- ✅ Academic integrity protection

## 🎥 Demo Video Guide

### What to Show (2-5 minutes)

1. **Introduction (15 sec)**
   - Brief overview of the system
   - Key features

2. **Presenter Workflow (60 sec)**
   - Create a quiz with 2-3 questions
   - Launch a session
   - Show session code

3. **Participant Workflow (45 sec)**
   - Multiple participants joining
   - Answering questions
   - Show answer locking feature

4. **Results View (45 sec)**
   - Show bar chart
   - **Highlight participant names by answer**
   - Show accuracy metrics

5. **Security Demo (30 sec)**
   - Participant tries to change answer
   - Shows locked state
   - Explain dual-layer protection

6. **Conclusion (15 sec)**
   - Recap key features
   - Benefits for education

## 🌟 Highlights

### What Makes This Project Stand Out

1. **Professional Quality**
   - Clean, intuitive UI
   - Robust error handling
   - Production-ready code

2. **Enhanced Features**
   - Individual participant tracking
   - Answer submission integrity
   - Real-time interactive charts

3. **Security**
   - Dual-layer answer protection
   - Database constraints
   - Data integrity guarantees

4. **Educational Value**
   - Promotes academic honesty
   - Provides actionable insights
   - Easy to use for all users

## 📝 Future Enhancements

Potential additions:
- [ ] Timer for questions
- [ ] Leaderboard functionality
- [ ] Export results to CSV/PDF
- [ ] Question banks and categories
- [ ] True/False and short answer questions
- [ ] Image support in questions
- [ ] Email notifications
- [ ] Analytics dashboard

## 📄 License

Educational project for ISDI 506 - Communication Infrastructures & Platforms for Ambient Intelligence

## 👨‍💻 Author

Created as part of the Interactive Quiz Add-in Assignment (ClassPoint-like system)

---

## Quick Start Commands

```bash
# Install dependencies
pip install streamlit pandas plotly "psycopg[binary]" python-dotenv

# Set up database
setup_database.bat

# Configure environment
copy .env.example .env
# (Edit .env with your password)

# Run application
python -m streamlit run app.py
```

---

**Version:** 2.0 (Enhanced Edition)

**Status:** Production Ready ✅

**Last Updated:** 2026-01-02
