import streamlit as st
from rag.chatbot import CustomerChatbot

# Database
from database.database import DatabaseManager
from database.auth import Authentication
from database.history import HistoryManager
from database.feedback import FeedbackManager

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="TechNova AI Support",
    page_icon="🤖",
    layout="wide"
)

# ================= DATABASE =================

db = DatabaseManager()
db.connect()
db.create_tables()

auth = Authentication(db)
history = HistoryManager(db)
feedback = FeedbackManager(db)

# ================= SESSION =================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_chat_id" not in st.session_state:
    st.session_state.last_chat_id = None

# ✅ CHANGE 1: ADD THIS - For tracking feedback
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

# ================= LOGIN / REGISTER =================

if not st.session_state.logged_in:

    st.title("🤖 TechNova AI Support")

    st.subheader("Login or Register")

    option = st.radio(
        "Choose Option",
        ["Login", "Register"],
        horizontal=True
    )

    # ================= REGISTER =================

    if option == "Register":

        name = st.text_input("Full Name")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Create Account"):

            if password != confirm:

                st.error("Passwords do not match.")

            else:

                success, message = auth.register_user(
                    name,
                    email,
                    password
                )

                if success:

                    st.success(message)

                    st.info("Please Login.")

                else:

                    st.error(message)

    # ================= LOGIN =================

    else:

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            success, result = auth.login_user(
                email,
                password
            )

            if success:

                st.session_state.logged_in = True
                st.session_state.user = result

                st.success(
                    f"Welcome {result[1]}"
                )

                st.rerun()

            else:

                st.error(result)

    st.stop()

# ================= MAIN UI =================

st.markdown("""
<style>

.main-title{
font-size:40px;
font-weight:bold;
text-align:center;
}

.subtitle{
text-align:center;
font-size:18px;
color:gray;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
🤖 TechNova AI Support Center
</div>

<div class="subtitle">
Your Intelligent Electronics Customer Assistant
</div>
""", unsafe_allow_html=True)

st.divider()

# ================= LOAD BOT =================

if "bot" not in st.session_state:

    st.session_state.bot = CustomerChatbot()

    try:

        st.session_state.bot.load_database()

    except:

        st.session_state.bot.build_database()

# ================= WELCOME =================

if len(st.session_state.messages) == 0:

    st.info(
        f"👋 Welcome {st.session_state.user[1]}!\n\n"
        "I can help you with Products, Shipping, Refunds and Warranty."
    )

# ================= SIDEBAR =================

with st.sidebar:

    st.success(
        f"Logged in as\n\n{st.session_state.user[1]}"
    )

    st.title("⚡ Quick Help")

    if st.button("📦 Track Order"):

        st.session_state.quick_question = "How can I track my order?"

    if st.button("💻 Product Information"):

        st.session_state.quick_question = "Tell me about available products."

    if st.button("💰 Refund Policy"):

        st.session_state.quick_question = "What is your refund policy?"

    if st.button("🚚 Shipping"):

        st.session_state.quick_question = "Tell me about shipping policy."

    if st.button("🛡 Warranty"):

        st.session_state.quick_question = "Explain warranty policy."

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []
        st.session_state.feedback_given = False  # ✅ CHANGE 2: Reset feedback
        st.rerun()

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.messages = []
        st.session_state.last_chat_id = None
        st.session_state.feedback_given = False  # ✅ CHANGE 3: Reset feedback

        st.rerun()
# ================= SHOW OLD CHAT =================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# ================= QUICK QUESTION =================

if "quick_question" in st.session_state:

    question = st.session_state.quick_question

    del st.session_state.quick_question

    st.session_state.feedback_given = False  # ✅ CHANGE 4: Reset for new question

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.write(question)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = st.session_state.bot.ask(question)

            st.write(answer)

    # Save Chat History

    chat_id = history.save_chat(

        user_id=st.session_state.user[0],

        knowledge_base_id=None,

        user_message=question,

        bot_response=answer
    )

    st.session_state.last_chat_id = chat_id

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# ================= USER CHAT =================

user_question = st.chat_input(
    "Ask anything about TechNova..."
)

if user_question:

    st.session_state.feedback_given = False  # ✅ CHANGE 5: Reset for new question

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):

        st.write(user_question)

    with st.chat_message("assistant"):

        with st.spinner("Searching Knowledge Base..."):

            answer = st.session_state.bot.ask(user_question)

            st.write(answer)

    # Save Chat History

    chat_id = history.save_chat(

        user_id=st.session_state.user[0],

        knowledge_base_id=None,

        user_message=user_question,

        bot_response=answer
    )

    st.session_state.last_chat_id = chat_id

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()


# ================= FEEDBACK =================
if (
    st.session_state.last_chat_id is not None
    and len(st.session_state.messages) > 0
):
    st.divider()
    
    # ✅ CHANGE 6: Check if feedback already given
    if st.session_state.feedback_given:
        st.write(" Thank you for your feedback! ")
    else:
        st.write("### Was this answer helpful?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("👍 Yes", key=f"yes_{st.session_state.last_chat_id}"):
                feedback.save_feedback(
                    st.session_state.last_chat_id,
                    "Yes"
                )
                st.session_state.feedback_given = True 
                st.rerun()
        
        with col2:
            if st.button("👎 No", key=f"no_{st.session_state.last_chat_id}"):
                feedback.save_feedback(
                    st.session_state.last_chat_id,
                    "No"
                )
                st.session_state.feedback_given = True  
                st.rerun()