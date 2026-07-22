import streamlit as st
import requests
from auth import login_user, register_user
from database import create_tables
create_tables()
st.set_page_config(
    page_title="AI Interview Prep",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"

)
API_URL = (
    "http://127.0.0.1:8000"
)
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "db_user_id" not in st.session_state:
    st.session_state.db_user_id = None

if st.session_state.user_id is None:
    st.title(" AI Interview Preparation Platform")
    option = st.radio(
        "Choose Option",
        ["Login", "Register"]
    )
    if option == "Login":
        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )
        if st.button("Login"):
            result = login_user(
                email,
                password
            )
            if result["success"]:
                st.session_state.user_id = result["user_id"]
                st.session_state.user_name = result["name"]
                st.session_state.db_user_id = result["user_id"]
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])
    else:
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )
        if st.button("Register"):
            result = register_user(
                name,
                email,
                password
            )
            if result["success"]:
                st.success(result["message"])
                st.info("Please login with your credentials")
            else:
                st.error(result["message"])
    st.stop()

st.markdown(
    """
    <style>
    .main {
        background-color: #f8fafc;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    .hero {
        padding: 35px;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #1e293b,
            #334155
        );
        color: white;
        margin-bottom: 25px;
    }
    .hero h1 {
        font-size: 42px;
        margin-bottom: 10px;
    }
    .hero p {
        font-size: 18px;
        color: #e2e8f0;
    }
    .card {
        padding: 25px;
        border-radius: 18px;
        background: white;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    .score-card {
        padding: 25px;
        border-radius: 18px;
        background: white;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .score {
        font-size: 36px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)
if "resume_id" not in st.session_state:
    st.session_state.resume_id = None
if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = None
if "question" not in st.session_state:
    st.session_state.question = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "follow_up" not in st.session_state:
    st.session_state.follow_up = None
if "job_analysis" not in st.session_state:
    st.session_state.job_analysis = None
if "ats_analysis" not in st.session_state:
    st.session_state.ats_analysis = None
if "roadmap" not in st.session_state:
    st.session_state.roadmap = None
if "results" not in st.session_state:
    st.session_state.results = None
with st.sidebar:
    st.title(
        "🎯 AI Interview Prep"
    )
    st.caption(
        "Your AI-powered career preparation assistant"
    )
    st.divider()
    page = st.radio(
        "Navigate",
        [
            "🏠 Dashboard",
            "📄 Resume Analysis",
            "🎯 Job Matching",
            "🎤 AI Interview",
            "📊 Results",
            "🗺️ Learning Roadmap",
            "📥 Final Report"
        ]
    )
    st.divider()
    st.info(
        "Upload your resume first "
        "to unlock AI-powered "
        "interview preparation."
    )
    st.divider()
    st.write(f"👤 {st.session_state.user_name}")
    if st.button("🚪 Logout"):
        try:
            requests.post(
                f"{API_URL}/clear-session",
                data={"user_id": st.session_state.db_user_id}
            )
        except:
            pass
        
        # Clear session state
        st.session_state.user_id = None
        st.session_state.user_name = ""
        st.session_state.db_user_id = None  
        st.session_state.resume_id = None
        st.session_state.resume_analysis = None
        st.session_state.question = None
        st.session_state.feedback = None
        st.session_state.follow_up = None
        st.session_state.job_analysis = None
        st.session_state.ats_analysis = None
        st.session_state.roadmap = None
        st.session_state.results = None
        st.rerun()

st.markdown(
    """
    <div class="hero">
    <h1>AI Interview Preparation Platform</h1>
    <p>
    Analyze your resume, match it with job descriptions,
    practice AI-generated interviews, identify skill gaps,
    and build your personalized career roadmap.
    </p>
    </div>
    """,
    unsafe_allow_html=True
)
if page == "🏠 Dashboard":
    st.header(
        "Welcome to Your Career Dashboard 👋"
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Resume Status",
            "Uploaded"
            if st.session_state.resume_id
            else "Not Uploaded"
        )
    with col2:
        st.metric(
            "Job Match",
            "Analyzed"
            if st.session_state.job_analysis
            else "Pending"

        )
    with col3:
        st.metric(
            "Interview",
            "Ready"
            if st.session_state.resume_id
            else "Upload Resume"
        )
    st.subheader(
        "How It Works"
    )
    step1, step2, step3, step4 = st.columns(4)
    with step1:
        st.markdown(
            "### 1️⃣\nUpload Resume"
        )
        st.caption(
            "Upload your PDF or DOCX resume."
        )
    with step2:
        st.markdown(
            "### 2️⃣\nAnalyze"
        )
        st.caption(
            "AI analyzes your skills and experience."
        )
    with step3:
        st.markdown(
            "### 3️⃣\nPractice"
        )
        st.caption(
            "Practice personalized AI interviews."
        )
    with step4:
        st.markdown(
            "### 4️⃣\nImprove"
        )
        st.caption(
            "Get scores, feedback and roadmap."
        )
elif page == "📄 Resume Analysis":
    st.header(
        "📄 Resume Analysis"
    )
    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=[
            "pdf",
            "docx"
        ]
    )
    if uploaded_file:
        st.info(
            f"Selected: {uploaded_file.name}"
        )
        if st.button(
            "🚀 Analyze My Resume",
            use_container_width=True
        ):
            with st.spinner(
                "AI is analyzing your resume..."
            ):
                try:
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type
                        )
                    }
                    data = {
                        "user_id": st.session_state.db_user_id
                    }
                    response = requests.post(
                        f"{API_URL}/resume/upload",
                        files=files,
                        data=data,  
                        timeout=300

                    )
                    data = response.json()
                    if data.get(
                        "success"
                    ):
                        st.session_state.resume_id = (
                            data[
                                "resume_id"
                            ]
                        )
                        st.session_state.resume_analysis = (
                            data[
                                "analysis"
                            ]
                        )
                        st.success(
                            "Resume analyzed successfully!"
                        )
                    else:
                        st.error(
                            data.get(
                                "error",
                                "Something went wrong."
                            )
                        )
                except Exception as e:
                    st.error(
                        f"API Error: {e}"
                    )
    if st.session_state.resume_analysis:
        st.divider()
        st.subheader(
            "🤖 AI Resume Analysis"
        )
        st.markdown(
            st.session_state[
                "resume_analysis"
            ]
        )
elif page == "🎯 Job Matching":
    st.header(
        "🎯 Resume vs Job Description"
    )
    if not st.session_state.resume_id:
        st.warning(
            "Please upload and analyze your resume first."
        )
    else:
        job_description = st.text_area(
            "Paste Job Description",
            height=300,
            placeholder=
                "Paste the complete job description here..."
        )
        if st.button(
            "🔍 Analyze Job Match",
            use_container_width=True
        ):
            if not job_description.strip():
                st.warning(
                    "Please enter a job description."
                )
            else:
                with st.spinner(
                    "Comparing your resume with the job..."
                ):
                    response = requests.post(
                        f"{API_URL}/job-description/analyze",
                        data={
                            "resume_id":
                                st.session_state[
                                    "resume_id"
                                ],
                            "job_description":
                                job_description,
                            "user_id": st.session_state.db_user_id
                        },
                        timeout=300
                    )
                    data = response.json()
                    if data.get(
                        "success"
                    ):
                        st.session_state.job_analysis = (
                            data[
                                "comparison"
                            ]
                        )
                        st.session_state.ats_analysis = (
                            data[
                                "ats_analysis"
                            ]
                        )

                        st.success(
                            "Job analysis completed!"
                        )
                    else:
                        st.error(
                            data.get(
                                "error"
                            )
                        )
        if st.session_state.job_analysis:
            st.subheader(
                "📊 Resume & Job Match"
            )
            st.markdown(
                st.session_state[
                    "job_analysis"
                ]
            )
        if st.session_state.ats_analysis:
            st.subheader(
                "🤖 ATS Analysis"
            )
            st.markdown(
                st.session_state[
                    "ats_analysis"
                ]
            )
elif page == "🎤 AI Interview":
    st.header(
        "🎤 AI Mock Interview"
    )
    if not st.session_state.resume_id:
        st.warning(
            "Please upload your resume first."
        )
    else:
        role = st.text_input(
            "Target Job Role",
            placeholder=
                "Example: Python AI Developer"
        )
        interview_type = st.selectbox(
            "Interview Type",
            [
                "Technical",
                "HR"
            ]
        )
        if interview_type == "Technical":
            category = st.selectbox(
                "Question Category",
                [
                    "Data Structures",
                    "Algorithms",
                    "System Design",
                    "Technology",
                    "Problem Solving"
                ]
            )
            difficulty = st.selectbox(
                "Difficulty",
                [
                    "Easy",
                    "Medium",
                    "Hard"
                ]
            )
            if st.button(
                "🎯 Generate Technical Question",
                use_container_width=True
            ):
                with st.spinner(
                    "Generating personalized question..."
                ):
                    response = requests.post(
                        f"{API_URL}/interview/technical/question",
                        data={
                            "resume_id":
                                st.session_state[
                                    "resume_id"
                                ],
                            "role":
                                role,
                            "difficulty":
                                difficulty,
                            "category":
                                category,
                            "user_id": st.session_state.db_user_id
                        },
                        timeout=300
                    )
                    data = response.json()
                    if data.get(
                        "success"
                    ):
                        st.session_state.question = (
                            data[
                                "question"
                            ]
                        )
                        st.session_state.feedback = None
                        st.session_state.follow_up = None
                    else:
                        st.error(
                            data.get(
                                "error"
                            )
                        )
        else:
            category = st.selectbox(
                "HR Question Category",
                [
                    "Motivation",
                    "Teamwork",
                    "Conflict Resolution",
                    "Leadership",
                    "Communication",
                    "Career Goals"
                ]
            )
            if st.button(
                "🎯 Generate HR Question",
                use_container_width=True
            ):
                with st.spinner(
                    "Generating personalized HR question..."
                ):
                    response = requests.post(
                        f"{API_URL}/interview/hr/question",
                        data={
                            "resume_id":
                                st.session_state[
                                    "resume_id"
                                ],
                            "role":
                                role,
                            "category":
                                category,
                            "user_id": st.session_state.db_user_id
                        },
                        timeout=300
                    )
                    data = response.json()
                    if data.get(
                        "success"
                    ):
                        st.session_state.question = (
                            data[
                                "question"
                            ]
                        )
                        st.session_state.feedback = None
                        st.session_state.follow_up = None
                    else:
                        st.error(
                            data.get(
                                "error"
                            )
                        )
        if st.session_state.question:
            st.divider()
            st.subheader(
                "❓ Interview Question"
            )
            st.info(
                st.session_state[
                    "question"
                ]
            )
            answer = st.text_area(
                "✍️ Your Answer",
                height=220,
                placeholder=
                    "Type your answer here..."
            )
            if st.button(
                "🤖 Evaluate My Answer",
                use_container_width=True
            ):
                if not answer.strip():
                    st.warning(
                        "Please write your answer."
                    )
                else:
                    with st.spinner(
                        "AI is evaluating your answer..."
                    ):
                        response = requests.post(
                            f"{API_URL}/interview/evaluate",
                            data={
                                "question":
                                    st.session_state[
                                        "question"
                                    ],
                                "answer":
                                    answer,
                                "interview_type":
                                    interview_type
                            },
                            timeout=300

                        )
                        data = response.json()
                        if data.get(
                            "success"
                        ):
                            st.session_state.feedback = (
                                data[
                                    "feedback"
                                ]
                            )
                            st.session_state.follow_up = (
                                data[
                                    "follow_up"
                                ]
                            )
                        else:
                            st.error(
                                data.get(
                                    "error"
                                )
                            )
        if st.session_state.feedback:
            st.divider()
            st.subheader(
                "📊 AI Feedback"
            )
            st.markdown(
                st.session_state[
                    "feedback"
                ]
            )
            st.subheader(
                "🔄 Follow-up Question"
            )
            st.warning(
                st.session_state[
                   "follow_up"
                ]
            )
elif page == "📊 Results":
    st.header(
        "📊 Interview Performance"
    )
    st.info(
        "Enter your question scores from 0 to 10. "
        "Example: 8, 7, 9, 6"
    )
    resume_score = st.number_input(
        "Resume Score (%)",
        min_value=0.0,
        max_value=100.0,
        value=70.0
    )
    technical_scores = st.text_input(
        "Technical Question Scores",
        "8, 7, 9, 6"
    )
    hr_scores = st.text_input(
        "HR Question Scores",
        "8, 9, 7, 8"
    )
    if st.button(
        "📊 Calculate Final Results",
        use_container_width=True
    ):
        response = requests.post(
            f"{API_URL}/results/calculate",
            data={
                "resume_score":
                    resume_score,

                "technical_scores":
                    technical_scores,
                "hr_scores":
                    hr_scores
            }
        )
        data = response.json()
        if data.get(
            "success"
        ):
            st.session_state.results = data
    if st.session_state.results:
        results = (
            st.session_state[
                "results"
            ]
        )
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Resume",
                f"{results['resume_score']}%"
            )
        with col2:
            st.metric(
                "Technical",
                f"{results['technical_score']}%"
            )
        with col3:
            st.metric(
                "HR",
                f"{results['hr_score']}%"
            )
        with col4:
            st.metric(
                "Overall",
                f"{results['overall_score']}%"
            )
        st.success(
            f"Final Grade: {results['grade']}"
        )
elif page == "🗺️ Learning Roadmap":
    st.header(
        "🗺️ Personalized Learning Roadmap"
    )
    role = st.text_input(
        "Target Role"
        "AI Engineer"
    )
    weak_areas = st.text_input(
        "Weak Areas",
        "Python, SQL, System Design"
    )
    hours = st.number_input(
        "Study Hours Per Week",
        min_value=1,
        max_value=100,
        value=10
    )
    if st.button(
        "🚀 Generate Learning Roadmap",
        use_container_width=True
    ):
        with st.spinner(
            "Creating personalized roadmap..."
        ):
            response = requests.post(
                f"{API_URL}/roadmap/generate",
                data={
                    "role":
                        role,
                    "weak_areas":
                        weak_areas,
                    "hours_per_week":
                        hours
                },
                timeout=300
            )
            data = response.json()
            if data.get(
                "success"
            ):
                st.session_state.roadmap = (
                    data[
                        "roadmap"
                    ]
                )
    if st.session_state.roadmap:
        st.divider()
        st.subheader(
            "📚 Your Learning Roadmap"
        )
        st.markdown(
            st.session_state[
                "roadmap"
            ]
        )
elif page == "📥 Final Report":
    st.header(
        "📥 Generate Final PDF Report"
    )
    st.info(
        "Complete your resume analysis, "
        "interview results and learning roadmap "
        "before generating the report."
    )
    candidate_name = st.text_input(
        "Candidate Name"
    )
    target_role = st.text_input(
        "Target Role"
    )
    col1, col2 = st.columns(2)
    with col1:
        resume_score = st.number_input(
            "Resume Score",
            0.0,
            100.0,
            70.0
        )
        ats_score = st.number_input(
            "ATS Score",
            0.0,
            100.0,
            70.0
        )
        technical_score = st.number_input(
            "Technical Score",
            0.0,
            100.0,
            70.0
        )
    with col2:
        hr_score = st.number_input(

            "HR Score",
            0.0,
            100.0,
            70.0
        )
        overall_score = st.number_input(
            "Overall Score",
            0.0,
            100.0,
            70.0
        )
        grade = st.text_input(
            "Grade",
            "C"
        )
    strengths = st.text_input(
        "Strengths",
        "Python, Communication"
    )
    weak_areas = st.text_input(
        "Weak Areas",
        "SQL, System Design"
    )
    missing_skills = st.text_input(
        "Missing Skills",
        "AWS, Docker"
    )
    roadmap = st.text_area(
        "Learning Roadmap",
        value=
            st.session_state.roadmap
            if st.session_state.roadmap
            else "Complete your learning roadmap first."
    )
    if st.button(
        "📥 Generate PDF Report",
        use_container_width=True
    ):
        with st.spinner(
            "Generating your final report..."
        ):
            response = requests.post(
                f"{API_URL}/report/generate",
                data={
                    "candidate_name":
                        candidate_name,
                    "target_role":
                        target_role,
                    "resume_score":
                        resume_score,
                    "ats_score":
                        ats_score,
                    "technical_score":
                        technical_score,
                    "hr_score":
                        hr_score,
                    "overall_score":
                        overall_score,
                    "grade":
                        grade,
                    "strengths":
                        strengths,
                    "weak_areas":
                        weak_areas,
                    "missing_skills":
                        missing_skills,
                    "roadmap":
                        roadmap,
                    "user_id": st.session_state.db_user_id
                },
                timeout=300
            )
            data = response.json()
            if data.get(
                "success"
            ):
                st.success(
                    "PDF report generated successfully!"
                )
                report_path = data[
                    "report_path"
                ]
                try:
                    with open(
                        report_path,
                        "rb"
                    ) as file:
                        st.download_button(
                            label=
                                "⬇️ Download Final Report",
                            data=
                                file,
                            file_name=
                                "AI_Interview_Report.pdf",
                            mime=
                                "application/pdf",
                            use_container_width=True
                        )
                except FileNotFoundError:
                    st.warning(
                        "Report generated on backend. "
                        "The file is available in the reports folder."
                    )
            else:
                st.error(
                    data.get(
                        "error",
                        "Report generation failed."
                    )
                )