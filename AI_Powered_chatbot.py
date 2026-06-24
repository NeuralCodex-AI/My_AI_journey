import streamlit as st
from google import genai

st.title("**AI Powered ChatBOt**")
st.write("Hello! how can I help you")

client = genai.Client(api_key="Your_API_KEY")

# initialize memory
if "messages" not in st.session_state:
    st.session_state.messages = []
# display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
user_input = st.chat_input("Start Chat------")# input box

if user_input:
    if user_input.lower() == "exit chat":
        st.session_state.messages = []
        st.rerun()
    # store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)
    
    history = ""
    for msg in st.session_state.messages:
        history += f"{msg['role']}: {msg['content']}\n"
    # get AI response
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=history
    )

    bot_reply = response.text
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    with st.chat_message("assistant"):
        st.write(bot_reply)