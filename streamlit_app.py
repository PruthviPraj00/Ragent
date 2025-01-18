import streamlit as st
from ui_agents import analyzer, generator

st.set_page_config(
    page_title="FlyonUI Component Assistant",
    page_icon="🎨",
    layout="wide"
)

st.title("FlyonUI Component Assistant 🎨")

with st.sidebar:
    st.header("About")
    st.write("""
    This tool helps you:
    1. Analyze UI requirements
    2. Suggest appropriate FlyonUI components
    3. Generate implementation code
    """)

# Main content
requirement = st.text_area(
    "Describe your UI requirement:",
    placeholder="Example: I need a responsive navigation bar with a logo, menu items, and a user profile dropdown",
    height=100
)

if requirement:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Component Analysis")
        with st.spinner("Analyzing components..."):
            analysis = analyzer.run(requirement)
            st.markdown(analysis)
    
    with col2:
        st.header("Code Implementation")
        with st.spinner("Generating code..."):
            code = generator.run(requirement)
            st.markdown(code)

if __name__ == "__main__":
    st.sidebar.markdown("---")
    st.sidebar.markdown("Made with ❤️ using FlyonUI") 