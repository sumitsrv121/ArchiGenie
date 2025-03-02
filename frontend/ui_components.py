import streamlit as st

def render_header():
    st.markdown("""
    <style>
        .main .block-container { padding-top: 2rem; }
        .stMarkdown { text-align: center; }
        h1 { color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("# 🚀 ArchiGenie - AI Architecture Assistant")
    st.markdown("### Transform Requirements into Cloud Architectures")

def remove_footer():
    st.markdown("""
    <style>
        footer { visibility: hidden; }
        .stAlert { padding: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)

def render_toggle():
    return st.toggle(
        "Switch between Functional and Guided Modes",
        key="toggle_mode",
        help="Functional mode for natural language input, Guided mode for technical specifications"
    )

def render_progress(percentage: int):
    st.markdown(f"""
    <div style="margin: 2rem 0; padding: 1rem; border-radius: 10px; background: #f0f2f6;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span>Generation Progress</span>
            <span>{percentage}%</span>
        </div>
        <div style="height: 20px; background: #e0e0e0; border-radius: 10px;">
            <div style="width: {percentage}%; height: 100%; 
                     background: #1f77b4; border-radius: 10px; 
                     transition: width 0.5s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_error(e):
    st.error(f"Error {e.status_code}: {str(e)}")
