"""
Interactive Quiz System - Main Streamlit Application
ClassPoint-like quiz system for presenters and participants.
"""
import streamlit as st
import database as db
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Interactive Quiz System",
    page_icon="📝",
    layout="wide"
)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'current_session_id' not in st.session_state:
    st.session_state.current_session_id = None
if 'current_session_code' not in st.session_state:
    st.session_state.current_session_code = None


def login_page():
    """Display login/registration page."""
    st.title("📝 Interactive Quiz System")
    st.markdown("### Welcome! Please select your role to continue")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👨‍🏫 Presenter")
        st.markdown("Create quizzes, launch sessions, and view results")
        presenter_name = st.text_input("Enter your name:", key="presenter_name")
        if st.button("Login as Presenter", use_container_width=True):
            if presenter_name.strip():
                user = db.create_user(presenter_name.strip(), 'presenter')
                st.session_state.user_id = user['id']
                st.session_state.user_name = user['name']
                st.session_state.user_role = user['role']
                st.rerun()
            else:
                st.error("Please enter your name")

    with col2:
        st.subheader("👥 Participant")
        st.markdown("Join a quiz session and answer questions")
        participant_name = st.text_input("Enter your name:", key="participant_name")
        if st.button("Login as Participant", use_container_width=True):
            if participant_name.strip():
                user = db.create_user(participant_name.strip(), 'participant')
                st.session_state.user_id = user['id']
                st.session_state.user_name = user['name']
                st.session_state.user_role = user['role']
                st.rerun()
            else:
                st.error("Please enter your name")


def presenter_interface():
    """Display presenter interface."""
    st.title(f"👨‍🏫 Presenter Dashboard - {st.session_state.user_name}")

    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select Page:",
            ["Create Quiz", "Manage Quizzes", "Active Sessions", "Launch Session", "View Results"]
        )
        st.divider()
        if st.button("Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    if page == "Create Quiz":
        create_quiz_page()
    elif page == "Manage Quizzes":
        manage_quizzes_page()
    elif page == "Active Sessions":
        active_sessions_page()
    elif page == "Launch Session":
        launch_session_page()
    elif page == "View Results":
        view_results_page()


def create_quiz_page():
    """Page for creating a new quiz."""
    st.header("Create New Quiz")

    quiz_title = st.text_input("Quiz Title:", placeholder="e.g., Python Programming Basics")

    if st.button("Create Quiz", type="primary"):
        if quiz_title.strip():
            quiz = db.create_quiz(quiz_title.strip(), st.session_state.user_id)
            st.success(f"✅ Quiz '{quiz['title']}' created successfully!")
            st.session_state.editing_quiz_id = quiz['id']
            st.rerun()
        else:
            st.error("Please enter a quiz title")

    # If a quiz was just created, show the question form
    if 'editing_quiz_id' in st.session_state:
        st.divider()
        add_questions_form(st.session_state.editing_quiz_id)


def add_questions_form(quiz_id):
    """Form to add questions to a quiz."""
    quiz = db.get_quiz_by_id(quiz_id)
    st.subheader(f"Add Questions to: {quiz['title']}")

    with st.form("add_question_form", clear_on_submit=True):
        question_text = st.text_area("Question:", placeholder="Enter your question here")

        col1, col2 = st.columns(2)
        with col1:
            option_a = st.text_input("Option A:", placeholder="First option")
            option_c = st.text_input("Option C:", placeholder="Third option (optional)")
        with col2:
            option_b = st.text_input("Option B:", placeholder="Second option")
            option_d = st.text_input("Option D:", placeholder="Fourth option (optional)")

        correct_answer = st.selectbox("Correct Answer:", ["A", "B", "C", "D"])

        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Add Question", type="primary", use_container_width=True)
        with col2:
            done = st.form_submit_button("Done Adding Questions", use_container_width=True)

        if submit:
            if question_text.strip() and option_a.strip() and option_b.strip():
                db.add_question(
                    quiz_id,
                    question_text.strip(),
                    option_a.strip(),
                    option_b.strip(),
                    option_c.strip() if option_c else None,
                    option_d.strip() if option_d else None,
                    correct_answer
                )
                st.success("✅ Question added!")
                st.rerun()
            else:
                st.error("Please fill in the question and at least options A and B")

        if done:
            del st.session_state.editing_quiz_id
            st.rerun()

    # Display existing questions
    questions = db.get_questions_by_quiz(quiz_id)
    if questions:
        st.subheader(f"Questions ({len(questions)})")
        for i, q in enumerate(questions, 1):
            with st.expander(f"Question {i}: {q['text'][:50]}..."):
                st.write(f"**{q['text']}**")
                st.write(f"A) {q['option_a']}")
                st.write(f"B) {q['option_b']}")
                if q['option_c']:
                    st.write(f"C) {q['option_c']}")
                if q['option_d']:
                    st.write(f"D) {q['option_d']}")
                st.write(f"✅ Correct Answer: {q['correct_answer']}")


def manage_quizzes_page():
    """Page to view and manage existing quizzes."""
    st.header("Manage Quizzes")

    quizzes = db.get_all_quizzes()

    if not quizzes:
        st.info("No quizzes created yet. Go to 'Create Quiz' to get started!")
        return

    for quiz in quizzes:
        with st.expander(f"📝 {quiz['title']} (Created: {quiz['created_at'].strftime('%Y-%m-%d %H:%M')})"):
            questions = db.get_questions_by_quiz(quiz['id'])
            st.write(f"**Number of Questions:** {len(questions)}")

            if questions:
                for i, q in enumerate(questions, 1):
                    st.markdown(f"**Q{i}:** {q['text']}")
                    cols = st.columns(4)
                    options = [
                        ('A', q['option_a']),
                        ('B', q['option_b']),
                        ('C', q['option_c']),
                        ('D', q['option_d'])
                    ]
                    for idx, (letter, option) in enumerate(options):
                        if option:
                            correct = "✅ " if letter == q['correct_answer'] else ""
                            cols[idx].write(f"{correct}{letter}) {option}")
                    st.divider()
            else:
                st.warning("No questions added yet")
                if st.button(f"Add Questions to {quiz['title']}", key=f"add_q_{quiz['id']}"):
                    st.session_state.editing_quiz_id = quiz['id']
                    st.rerun()


def launch_session_page():
    """Page to launch a new quiz session."""
    st.header("Launch Quiz Session")

    quizzes = db.get_all_quizzes()

    if not quizzes:
        st.warning("No quizzes available. Create a quiz first!")
        return

    quiz_options = {f"{q['title']} (ID: {q['id']})": q['id'] for q in quizzes}
    selected_quiz = st.selectbox("Select Quiz:", list(quiz_options.keys()))

    if st.button("Launch Session", type="primary"):
        quiz_id = quiz_options[selected_quiz]
        questions = db.get_questions_by_quiz(quiz_id)

        if not questions:
            st.error("Cannot launch session: Quiz has no questions!")
            return

        session = db.create_session(quiz_id)
        st.success(f"✅ Session launched successfully!")
        st.info(f"**Session Code:** `{session['session_code']}`")
        st.markdown("Share this code with participants to join the session.")

        # Display QR code-like box
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 30px; border-radius: 10px; text-align: center; margin: 20px 0;">
            <h1 style="font-size: 72px; margin: 0; color: #1f77b4;">{session['session_code']}</h1>
            <p style="font-size: 18px; color: #666;">Participants can join with this code</p>
        </div>
        """, unsafe_allow_html=True)


def active_sessions_page():
    """Page to view active sessions."""
    st.header("Active Sessions")

    sessions = db.get_active_sessions()

    if not sessions:
        st.info("No active sessions. Launch a session to get started!")
        return

    for session in sessions:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.subheader(f"📍 {session['quiz_title']}")
            st.write(f"Session Code: **{session['session_code']}**")
            st.write(f"Started: {session['created_at'].strftime('%Y-%m-%d %H:%M')}")
        with col2:
            if st.button("View Results", key=f"view_{session['id']}"):
                st.session_state.viewing_session_id = session['id']
                st.rerun()
        with col3:
            if st.button("End Session", key=f"end_{session['id']}", type="primary"):
                db.end_session(session['id'])
                st.success("Session ended")
                st.rerun()

        st.divider()


def view_results_page():
    """Page to view session results."""
    st.header("View Session Results")

    sessions = db.get_active_sessions()
    all_sessions = sessions  # Could extend to include ended sessions

    if not all_sessions:
        st.info("No sessions available")
        return

    session_options = {
        f"{s['quiz_title']} - {s['session_code']} ({s['created_at'].strftime('%Y-%m-%d %H:%M')})": s['id']
        for s in all_sessions
    }

    selected_session = st.selectbox("Select Session:", list(session_options.keys()))
    session_id = session_options[selected_session]

    display_session_results(session_id)


def display_session_results(session_id):
    """Display detailed results for a session."""
    session = db.get_session_by_code(
        [s for s in db.get_active_sessions() if s['id'] == session_id][0]['session_code']
    )
    quiz = db.get_quiz_by_id(session['quiz_id'])
    questions = db.get_questions_by_quiz(session['quiz_id'])

    st.subheader(f"Results: {quiz['title']}")

    for i, question in enumerate(questions, 1):
        st.markdown(f"### Question {i}: {question['text']}")

        # Display question options
        st.markdown("**Options:**")
        option_cols = st.columns(4)
        options = [
            ('A', question['option_a']),
            ('B', question['option_b']),
            ('C', question['option_c']),
            ('D', question['option_d'])
        ]
        for idx, (letter, option) in enumerate(options):
            if option:
                correct_indicator = " ✅" if letter == question['correct_answer'] else ""
                option_cols[idx].markdown(f"**{letter})** {option}{correct_indicator}")

        st.markdown("---")

        # Get aggregated results for chart
        results = db.get_question_results(question['id'], session_id)
        # Get detailed responses with participant names
        detailed_responses = db.get_question_responses_detailed(question['id'], session_id)

        if results:
            # Create two columns: chart and participant list
            col1, col2 = st.columns([3, 2])

            with col1:
                # Create DataFrame for visualization
                df = pd.DataFrame(results)

                # Add all options (A, B, C, D) even if no responses
                all_options = ['A', 'B', 'C', 'D']
                for opt in all_options:
                    if opt not in df['answer'].values:
                        df = pd.concat([df, pd.DataFrame({'answer': [opt], 'count': [0]})], ignore_index=True)

                df = df.sort_values('answer')

                # Create bar chart
                fig = go.Figure(data=[
                    go.Bar(
                        x=df['answer'],
                        y=df['count'],
                        text=df['count'],
                        textposition='auto',
                        marker_color=['#2ecc71' if opt == question['correct_answer'] else '#3498db'
                                       for opt in df['answer']]
                    )
                ])

                fig.update_layout(
                    title=f"Responses Distribution",
                    xaxis_title="Answer",
                    yaxis_title="Number of Responses",
                    height=400
                )

                st.plotly_chart(fig, use_container_width=True)

                # Show correct answer percentage
                total_responses = df['count'].sum()
                correct_responses = df[df['answer'] == question['correct_answer']]['count'].sum()
                if total_responses > 0:
                    accuracy = (correct_responses / total_responses) * 100
                    st.metric("Accuracy", f"{accuracy:.1f}%", f"{correct_responses}/{total_responses} correct")

            with col2:
                # Show participant breakdown by answer
                st.markdown("**Participant Responses:**")

                if detailed_responses:
                    # Group responses by answer
                    responses_by_answer = {}
                    for resp in detailed_responses:
                        answer = resp['answer']
                        if answer not in responses_by_answer:
                            responses_by_answer[answer] = []
                        responses_by_answer[answer].append(resp)

                    # Display each answer group
                    for answer in ['A', 'B', 'C', 'D']:
                        if answer in responses_by_answer:
                            participants = responses_by_answer[answer]
                            is_correct = answer == question['correct_answer']

                            # Color code based on correctness
                            if is_correct:
                                st.markdown(f"**Answer {answer}** ✅ ({len(participants)} participant{'s' if len(participants) > 1 else ''})")
                            else:
                                st.markdown(f"**Answer {answer}** ❌ ({len(participants)} participant{'s' if len(participants) > 1 else ''})")

                            # List participants who chose this answer
                            for participant in participants:
                                st.markdown(f"• {participant['participant_name']}")

                            st.markdown("")  # Add spacing
                else:
                    st.info("No participants have answered yet")

        else:
            st.info("No responses yet for this question")

        st.divider()


def participant_interface():
    """Display participant interface."""
    st.title(f"👥 Participant - {st.session_state.user_name}")

    with st.sidebar:
        st.header("Menu")
        if st.button("Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # If not in a session, show join form
    if not st.session_state.current_session_id:
        join_session_form()
    else:
        # Show quiz questions
        take_quiz()


def join_session_form():
    """Form for participants to join a session."""
    st.header("Join Quiz Session")

    col1, col2 = st.columns([2, 1])
    with col1:
        session_code = st.text_input(
            "Enter Session Code:",
            placeholder="e.g., ABC123",
            max_chars=6
        ).upper()
    with col2:
        st.write("")
        st.write("")
        if st.button("Join Session", type="primary", use_container_width=True):
            if session_code:
                session = db.get_session_by_code(session_code)
                if session and session['is_active']:
                    st.session_state.current_session_id = session['id']
                    st.session_state.current_session_code = session['session_code']
                    st.success(f"✅ Joined session: {session_code}")
                    st.rerun()
                else:
                    st.error("Invalid or inactive session code")
            else:
                st.error("Please enter a session code")


def take_quiz():
    """Display quiz questions for participants."""
    session = db.get_session_by_code(st.session_state.current_session_code)
    quiz = db.get_quiz_by_id(session['quiz_id'])
    questions = db.get_questions_by_quiz(session['quiz_id'])

    st.header(f"📝 {quiz['title']}")
    st.info(f"Session Code: {st.session_state.current_session_code}")

    if st.button("Leave Session"):
        st.session_state.current_session_id = None
        st.session_state.current_session_code = None
        st.rerun()

    st.divider()

    # Display questions
    for i, question in enumerate(questions, 1):
        st.subheader(f"Question {i}")
        st.write(question['text'])

        # Check if already answered
        existing_response = db.get_user_response(
            question['id'],
            st.session_state.user_id,
            st.session_state.current_session_id
        )

        options = []
        if question['option_a']:
            options.append(('A', question['option_a']))
        if question['option_b']:
            options.append(('B', question['option_b']))
        if question['option_c']:
            options.append(('C', question['option_c']))
        if question['option_d']:
            options.append(('D', question['option_d']))

        # Check if already answered - disable interaction if yes
        if existing_response:
            # Display the submitted answer (read-only)
            st.markdown("**Your submitted answer:**")
            submitted_answer = existing_response['answer']
            for letter, text in options:
                if letter == submitted_answer:
                    st.markdown(f"**{letter}) {text}** ← Your answer")
                else:
                    st.markdown(f"{letter}) {text}")

            # Show if correct or incorrect
            if existing_response['is_correct']:
                st.success("✅ Your answer is correct!")
            else:
                st.error("❌ Your answer is incorrect")

            st.info("⚠️ Answer already submitted. You cannot change your response.")
        else:
            # Allow answering only if not yet submitted
            option_labels = [f"{letter}) {text}" for letter, text in options]

            selected = st.radio(
                "Select your answer:",
                option_labels,
                index=None,
                key=f"q_{question['id']}"
            )

            if st.button(f"Submit Answer", key=f"submit_{question['id']}", type="primary"):
                if selected:
                    answer_letter = selected.split(')')[0]
                    db.submit_response(
                        question['id'],
                        st.session_state.user_id,
                        st.session_state.current_session_id,
                        answer_letter
                    )
                    st.success("✅ Answer submitted!")
                    st.rerun()
                else:
                    st.warning("⚠️ Please select an answer before submitting")

        st.divider()


def main():
    """Main application logic."""
    # Check if user is logged in
    if st.session_state.user_id is None:
        login_page()
    else:
        # Route to appropriate interface
        if st.session_state.user_role == 'presenter':
            presenter_interface()
        else:
            participant_interface()


if __name__ == "__main__":
    main()
