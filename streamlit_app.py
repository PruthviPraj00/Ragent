import streamlit as st
from ui_agents import flyon_agent
import re

st.set_page_config(
    page_title="FlyonUI Component Assistant",
    page_icon="🎨",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("FlyonUI Component Assistant 🎨")

with st.sidebar:
    st.header("About")
    st.write("""
    This AI assistant helps you generate FlyonUI components by:
    1. Understanding your UI requirements
    2. Suggesting appropriate FlyonUI components
    3. Generating precise implementation code
    
    Simply describe what you need, and the assistant will provide you with the exact component code.
    """)

def clean_response(response_text):
    # Remove debug information
    if "Running:" in response_text:
        response_text = response_text.split("Running:")[1]
    if "search_knowledge_base" in response_text:
        response_text = re.sub(r' - search_knowledge_base\(.*?\)\n', '', response_text)
    
    # Extract code blocks
    code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', response_text, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    
    # If no code blocks, try to extract HTML directly
    html_match = re.search(r'<.*?>.*</.*?>', response_text, re.DOTALL)
    if html_match:
        return html_match.group(0).strip()
    
    return response_text.strip()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "code" in message:
            st.code(message["code"], language="html")
        else:
            st.write(message["content"])

# Chat input
if prompt := st.chat_input("Describe your UI component requirement..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Generating component..."):
            response = flyon_agent.run(prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            clean_code = clean_response(response_text)
            
            # Display the code
            st.code(clean_code, language="html")
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Here's your FlyonUI component:",
                "code": clean_code
            })

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ using FlyonUI")

# Add copy button styling
st.markdown("""
<style>
.stCodeBlock button {
    color: inherit;
    background-color: transparent;
}
</style>
""", unsafe_allow_html=True) 