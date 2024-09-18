import streamlit as st
from typing import List, Dict
from physics_learning_assistant.rag_ops import llm_response

# Define subjects and chapters
SUBJECTS: List[str] = ["None", "Physics"]
CHAPTERS: Dict[str, List[str]] = {
    "None": ["None"],
    "Physics": ["None", "WORK, ENERGY AND POWER"]
}

def get_ai_response(user_input: str) -> str:
    try:
        response = llm_response(user_query=user_input)
        return response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "I'm sorry, but I couldn't generate a response at this time. Please try again later."

def main():
    st.set_page_config(page_title="Physics Learning Assistant", page_icon="🧠", layout="wide")
    
    st.title("Hello, Welcome to Physics Learning Assistant! 🚀")
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'subject' not in st.session_state:
        st.session_state.subject = "None"
    if 'chapter' not in st.session_state:
        st.session_state.chapter = "None"

    # Sidebar for subject and chapter selection
    with st.sidebar:
        new_subject = st.selectbox("Select a subject:", SUBJECTS, key="subject_select")
        
        # Update available chapters based on selected subject
        available_chapters = CHAPTERS[new_subject]
        new_chapter = st.selectbox("Select a chapter:", available_chapters, key="chapter_select")
        
        # Update session state
        if new_subject != st.session_state.subject:
            st.session_state.subject = new_subject
            st.session_state.chapter = "None"
            st.session_state.messages = []
        elif new_chapter != st.session_state.chapter:
            st.session_state.chapter = new_chapter
            st.session_state.messages = []
        
        st.header("About Physics Learning Assistant")
        st.info(
            "Physics Learning Assistant is an AI-powered assistant designed to help students prepare for the NEET exam. "
            "Select a subject and chapter, then ask your questions to get personalized responses."
        )
        
        st.header("Disclaimer")
        st.warning(
            "This app uses AI to generate responses. While we strive for accuracy, "
            "please verify important information from official sources."
        )

    # Main area
    if st.session_state.subject == "None":
        st.info("Please select a subject to continue.")
    elif st.session_state.chapter == "None":
        st.info("Please select a chapter to start chatting.")
    else:
        st.success(f"Selected Subject: {st.session_state.subject}, Chapter: {st.session_state.chapter}")
        
        # Displaying chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User Chat input
        if prompt := st.chat_input("What is your question?", key="chat_input"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_ai_response(st.session_state.subject, st.session_state.chapter, prompt)
                st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()