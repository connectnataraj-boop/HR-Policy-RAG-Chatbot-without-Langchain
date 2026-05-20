import streamlit as st
from query_processing import query_processor

st.title("HR Policy Chatbot")
st.write("Ask anything about the HR Policy document.")

# Keep chat history visible on screen
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box at bottom
query = st.chat_input("Ask your question...")

if query:
    # Show user message
    with st.chat_message("user"):
        st.write(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # Get answer
    with st.spinner("Thinking..."):
        answer = query_processor(query)

    # Show assistant answer
    with st.chat_message("assistant"):
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
