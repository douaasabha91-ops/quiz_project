"""
Database connection and operations module for the Interactive Quiz System.
Alternative version using psycopg3 (better Windows compatibility)
"""
import psycopg
from psycopg.rows import dict_row
from contextlib import contextmanager
import os
from dotenv import load_dotenv
import random
import string

load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'dbname': os.getenv('DB_NAME', 'quiz_system'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}


@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = None
    try:
        conn = psycopg.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def generate_session_code():
    """Generate a unique 6-character session code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


# User operations
def create_user(name, role='participant'):
    """Create a new user."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "INSERT INTO users (name, role) VALUES (%s, %s) RETURNING id, name, role",
                (name, role)
            )
            return cur.fetchone()


def get_user_by_id(user_id):
    """Get user by ID."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            result = cur.fetchone()
            return result if result else None


# Quiz operations
def create_quiz(title, created_by):
    """Create a new quiz."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "INSERT INTO quizzes (title, created_by) VALUES (%s, %s) RETURNING id, title, created_at",
                (title, created_by)
            )
            return cur.fetchone()


def get_all_quizzes():
    """Get all quizzes."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM quizzes ORDER BY created_at DESC")
            return cur.fetchall()


def get_quiz_by_id(quiz_id):
    """Get quiz by ID."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM quizzes WHERE id = %s", (quiz_id,))
            result = cur.fetchone()
            return result if result else None


# Question operations
def add_question(quiz_id, text, option_a, option_b, option_c, option_d, correct_answer):
    """Add a question to a quiz."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """INSERT INTO questions (quiz_id, text, option_a, option_b, option_c, option_d, correct_answer)
                   VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (quiz_id, text, option_a, option_b, option_c, option_d, correct_answer)
            )
            return cur.fetchone()['id']


def get_questions_by_quiz(quiz_id):
    """Get all questions for a quiz."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM questions WHERE quiz_id = %s ORDER BY id", (quiz_id,))
            return cur.fetchall()


def get_question_by_id(question_id):
    """Get question by ID."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM questions WHERE id = %s", (question_id,))
            result = cur.fetchone()
            return result if result else None


# Session operations
def create_session(quiz_id):
    """Create a new quiz session with a unique code."""
    session_code = generate_session_code()
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # Ensure unique session code
            while True:
                try:
                    cur.execute(
                        "INSERT INTO sessions (quiz_id, session_code) VALUES (%s, %s) RETURNING id, session_code",
                        (quiz_id, session_code)
                    )
                    conn.commit()
                    return cur.fetchone()
                except psycopg.errors.UniqueViolation:
                    session_code = generate_session_code()
                    conn.rollback()


def get_session_by_code(session_code):
    """Get session by code."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM sessions WHERE session_code = %s", (session_code,))
            result = cur.fetchone()
            return result if result else None


def get_active_sessions():
    """Get all active sessions."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """SELECT s.*, q.title as quiz_title
                   FROM sessions s
                   JOIN quizzes q ON s.quiz_id = q.id
                   WHERE s.is_active = TRUE
                   ORDER BY s.created_at DESC"""
            )
            return cur.fetchall()


def end_session(session_id):
    """End a quiz session."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE sessions SET is_active = FALSE, ended_at = CURRENT_TIMESTAMP WHERE id = %s",
                (session_id,)
            )


# Response operations
def submit_response(question_id, user_id, session_id, answer):
    """Submit a response to a question. Once submitted, it cannot be changed."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # Check if response already exists
            cur.execute(
                """SELECT id FROM responses
                   WHERE question_id = %s AND user_id = %s AND session_id = %s""",
                (question_id, user_id, session_id)
            )
            existing = cur.fetchone()

            if existing:
                # Response already submitted - do not allow updates
                raise ValueError("Answer already submitted. Cannot modify response.")

            # Get correct answer
            cur.execute("SELECT correct_answer FROM questions WHERE id = %s", (question_id,))
            correct = cur.fetchone()['correct_answer']
            is_correct = (answer == correct)

            # Insert response (only if doesn't exist)
            cur.execute(
                """INSERT INTO responses (question_id, user_id, session_id, answer, is_correct)
                   VALUES (%s, %s, %s, %s, %s)
                   RETURNING id""",
                (question_id, user_id, session_id, answer, is_correct)
            )
            return cur.fetchone()['id']


def get_responses_by_session(session_id):
    """Get all responses for a session."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """SELECT r.*, u.name as user_name, q.text as question_text
                   FROM responses r
                   JOIN users u ON r.user_id = u.id
                   JOIN questions q ON r.question_id = q.id
                   WHERE r.session_id = %s
                   ORDER BY r.submitted_at""",
                (session_id,)
            )
            return cur.fetchall()


def get_question_results(question_id, session_id):
    """Get aggregated results for a specific question in a session."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """SELECT answer, COUNT(*) as count
                   FROM responses
                   WHERE question_id = %s AND session_id = %s
                   GROUP BY answer
                   ORDER BY answer""",
                (question_id, session_id)
            )
            return cur.fetchall()


def get_question_responses_detailed(question_id, session_id):
    """Get detailed responses for a specific question showing participant names."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """SELECT r.answer, u.name as participant_name, r.is_correct, r.submitted_at
                   FROM responses r
                   JOIN users u ON r.user_id = u.id
                   WHERE r.question_id = %s AND r.session_id = %s
                   ORDER BY r.answer, r.submitted_at""",
                (question_id, session_id)
            )
            return cur.fetchall()


def get_user_response(question_id, user_id, session_id):
    """Check if user has already answered a question in this session."""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """SELECT * FROM responses
                   WHERE question_id = %s AND user_id = %s AND session_id = %s""",
                (question_id, user_id, session_id)
            )
            result = cur.fetchone()
            return result if result else None
