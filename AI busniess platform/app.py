import streamlit as st

from modules.auth import Auth
from modules.chat import Chat
from modules.document_ai import DocumentAI
from modules.resume import ResumeAI
from modules.email import EmailAI
from modules.meeting import MeetingAI
from modules.content import ContentAI
from modules.coding import CodingAI


st.set_page_config(
    page_title="AI Business Assistant",
    page_icon="🤖",
    layout="wide"
)


auth = Auth()
chat = Chat()
document = DocumentAI()
resume = ResumeAI()
email = EmailAI()
meeting = MeetingAI()
content = ContentAI()
coding = CodingAI()


if "page" not in st.session_state:
    st.session_state.page = "Login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


def login():

    st.title("AI Business Assistant")

    email_address = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Login",
            use_container_width=True
        ):

            success, message = auth.login(
                email_address,
                password
            )

            if success:
                st.success(message)
                st.rerun()

            st.error(message)

    with col2:

        if st.button(
            "Signup",
            use_container_width=True
        ):

            st.session_state.page = "Signup"
            st.rerun()


def signup():

    st.title("Create Account")

    name = st.text_input("Name")

    email_address = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            success, message = auth.signup(
                name,
                email_address,
                password
            )

            if success:

                st.success(message)

                st.session_state.page = "Login"

                st.rerun()

            st.error(message)

    with col2:

        if st.button(
            "Back",
            use_container_width=True
        ):

            st.session_state.page = "Login"

            st.rerun()


def dashboard():

    st.sidebar.title("AI Business Assistant")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "AI Chat",
            "Document AI",
            "Resume AI",
            "Email AI",
            "Meeting AI",
            "Content AI",
            "Coding AI"
        ]
    )

    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):

        auth.logout()

        st.rerun()

    if page == "Dashboard":

        st.title("Dashboard")

        st.write(
            f"Welcome {st.session_state.user['name']}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.info("AI Chat")

            st.info("Resume AI")

            st.info("Meeting AI")

            st.info("Content AI")

        with col2:

            st.info("Document AI")

            st.info("Email AI")

            st.info("Coding AI")

    return page

selected_page = None
if not st.session_state.logged_in:

    if st.session_state.page == "Login":
        login()

    else:
        signup()

else:

    selected_page = dashboard()
if selected_page == "AI Chat":

    st.title("AI Chat")

    history = chat.history(
        st.session_state.user["email"]
    )

    for item in history:

        with st.chat_message("user"):
            st.write(item["user"])

        with st.chat_message("assistant"):
            st.write(item["assistant"])

    question = st.chat_input(
        "Ask anything..."
    )

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            placeholder = st.empty()

            answer = ""

            for chunk in chat.stream(
                st.session_state.user["email"],
                question
            ):

                answer += chunk

                placeholder.markdown(answer)


elif selected_page == "Document AI":

    st.title("Document AI")

    uploaded_file = st.file_uploader(
        "Upload Document",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file:

        if "document_vector" not in st.session_state:

            file_path = document.upload_document(
                uploaded_file
            )

            vector_path = document.create_index(
                file_path
            )

            st.session_state.document_vector = vector_path

            st.success("Document Uploaded")

        question = st.text_input(
            "Ask Question"
        )

        if st.button(
            "Generate Answer",
            use_container_width=True
        ):

            answer = document.ask(
                st.session_state.document_vector,
                question
            )

            st.write(answer)


elif selected_page == "Resume AI":

    st.title("Resume AI")

    uploaded_resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )

    if uploaded_resume:

        if st.button(
            "Analyze Resume",
            use_container_width=True
        ):

            result = resume.analyze(
                uploaded_resume,
                st.session_state.user["email"]
            )

            st.markdown(result)

elif selected_page == "Email AI":

    st.title("Email AI")

    option = st.selectbox(

        "Choose",

        [
            "Generate Email",
            "Reply Email",
            "Grammar Check"
        ]

    )

    if option == "Generate Email":

        purpose = st.text_input(
            "Purpose"
        )

        details = st.text_area(
            "Details"
        )

        if st.button(
            "Generate",
            use_container_width=True
        ):

            result = email.generate(
                purpose,
                details
            )

            st.markdown(result)

    elif option == "Reply Email":

        email_text = st.text_area(
            "Paste Email"
        )

        if st.button(
            "Generate Reply",
            use_container_width=True
        ):

            result = email.reply(
                email_text
            )

            st.markdown(result)

    else:

        text = st.text_area(
            "Enter Text"
        )

        if st.button(
            "Correct Grammar",
            use_container_width=True
        ):

            result = email.grammar(
                text
            )

            st.markdown(result)
elif selected_page == "Meeting AI":

    st.title("Meeting AI")

    transcript = st.text_area(
        "Paste Meeting Transcript",
        height=250
    )

    if st.button(
        "Generate Summary",
        use_container_width=True
    ):

        if transcript:

            result = meeting.summarize(
                transcript,
                st.session_state.user["email"]
            )

            st.markdown(result)


elif selected_page == "Content AI":

    st.title("Content AI")

    option = st.selectbox(
        "Content Type",
        [
            "Blog",
            "Social Media",
            "Marketing Copy"
        ]
    )

    if option == "Blog":

        topic = st.text_input(
            "Topic"
        )

        if st.button(
            "Generate Blog",
            use_container_width=True
        ):

            result = content.blog(
                topic
            )

            st.markdown(result)

    elif option == "Social Media":

        topic = st.text_input(
            "Topic"
        )

        platform = st.selectbox(
            "Platform",
            [
                "Instagram",
                "Facebook",
                "LinkedIn",
                "Twitter"
            ]
        )

        if st.button(
            "Generate Post",
            use_container_width=True
        ):

            result = content.social_post(
                topic,
                platform
            )

            st.markdown(result)

    else:

        product = st.text_input(
            "Product"
        )

        if st.button(
            "Generate Copy",
            use_container_width=True
        ):

            result = content.marketing_copy(
                product
            )

            st.markdown(result)


elif selected_page == "Coding AI":

    st.title("Coding AI")

    option = st.selectbox(
        "Choose",
        [
            "Explain Code",
            "Generate Code",
            "Debug Code",
            "Optimize Code",
            "Convert Code",
            "Documentation",
            "Complexity",
            "Review"
        ]
    )

    if option == "Generate Code":

        requirement = st.text_area(
            "Requirement"
        )

        if st.button(
            "Generate",
            use_container_width=True
        ):

            result = coding.generate(
                requirement
            )

            st.code(result)

    else:

        code = st.text_area(
            "Code",
            height=300
        )

        if option == "Explain Code":

            if st.button(
                "Explain",
                use_container_width=True
            ):

                result = coding.explain(
                    code
                )

                st.markdown(result)

        elif option == "Debug Code":

            if st.button(
                "Debug",
                use_container_width=True
            ):

                result = coding.debug(
                    code
                )

                st.markdown(result)

        elif option == "Optimize Code":

            if st.button(
                "Optimize",
                use_container_width=True
            ):

                result = coding.optimize(
                    code
                )

                st.markdown(result)

        elif option == "Convert Code":

            language = st.text_input(
                "Target Language"
            )

            if st.button(
                "Convert",
                use_container_width=True
            ):

                result = coding.convert(
                    code,
                    language
                )

                st.markdown(result)

        elif option == "Documentation":

            if st.button(
                "Generate Documentation",
                use_container_width=True
            ):

                result = coding.documentation(
                    code
                )

                st.markdown(result)

        elif option == "Complexity":

            if st.button(
                "Analyze",
                use_container_width=True
            ):

                result = coding.complexity(
                    code
                )

                st.markdown(result)

        elif option == "Review":

            if st.button(
                "Review Code",
                use_container_width=True
            ):

                result = coding.review(
                    code
                )

                st.markdown(result)