"""
Job Application Helper - Streamlit App
A tool to help job applicants create tailored cover letters based on their CV and job descriptions.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from pdf_utils import extract_text_from_pdf, validate_pdf_content
from cover_letter_agent import CoverLetterAgent
from pdf_generator import create_cover_letter_pdf, format_filename

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="CoverCraft AI - Job Application Helper",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main app background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Main content container */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
    }
    
    .main-header {
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-header {
        color: #FF6B6B;
        border-bottom: 3px solid #4ECDC4;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: bold;
        border-radius: 5px;
    }
    
    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        border: 2px solid #4ECDC4;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        color: #2d3748;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
    }
    
    .info-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border: 2px solid #FF9F9B;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        color: #2d3748;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(255, 159, 155, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Radio button styling */
    .stRadio > div {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 15px;
        padding: 1rem;
        border: 2px solid #FFB88C;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        border-radius: 15px;
        border: 2px dashed #FDCB6E;
        padding: 2rem;
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        background: linear-gradient(135deg, #e1f5fe 0%, #f3e5f5 100%);
        border-radius: 15px;
        border: 2px solid #81D4FA;
        color: #2d3748 !important;
        font-weight: 500;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
        border-radius: 10px;
        color: #2d3748;
        font-weight: bold;
    }
    
    /* Expander content styling */
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 0 0 10px 10px;
        color: #2d3748 !important;
        padding: 1rem;
    }
    
    /* Fix text area content color */
    .stTextArea textarea {
        color: #2d3748 !important;
    }
    
    /* Fix disabled text area visibility */
    .stTextArea textarea[disabled] {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #2d3748 !important;
        opacity: 0.8;
    }
    
    /* Specific styling for all text content in containers */
    .stTextArea label {
        color: #2d3748 !important;
        font-weight: 600;
    }
    
    /* Ensure all text inputs have proper contrast */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #2d3748 !important;
        border: 2px solid rgba(78, 205, 196, 0.5) !important;
    }
    
    /* Fix expander text visibility */
    .streamlit-expanderContent p, 
    .streamlit-expanderContent div, 
    .streamlit-expanderContent span {
        color: #2d3748 !important;
    }
    
    /* Sidebar elements */
    .css-1lcbmhc .css-1v0mbdj {
        color: #2d3748;
        font-weight: 500;
    }
    
    /* Download button special styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #a8e6cf 0%, #dcedc8 100%);
        color: #2d3748;
        font-weight: bold;
        border: 2px solid #81C784;
        border-radius: 25px;
        box-shadow: 0 4px 15px rgba(129, 199, 132, 0.3);
    }
    
    /* Fun animations */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .main-header {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Warning and error boxes */
    .stAlert {
        border-radius: 15px;
        border-left: 5px solid #FF6B6B;
    }
    
    /* Spinner customization */
    .stSpinner > div {
        border-top-color: #FF6B6B !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'cv_text' not in st.session_state:
        st.session_state.cv_text = ""
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    if 'cover_letter' not in st.session_state:
        st.session_state.cover_letter = ""
    if 'cv_score' not in st.session_state:
        st.session_state.cv_score = None
    if 'api_key_set' not in st.session_state:
        # Check if API key is available in Streamlit secrets (for cloud deployment) or environment variables (for local)
        try:
            api_key = st.secrets.get("OPENAI_API_KEY", None)
            if not api_key:
                # Fallback to environment variables for local development
                api_key = os.getenv("OPENAI_API_KEY")
        except Exception:
            # If secrets are not available (local development), use environment variables
            api_key = os.getenv("OPENAI_API_KEY")
        
        st.session_state.api_key_set = bool(api_key and api_key != "your_openai_api_key_here")

def main():
    """Main application function."""
    
    # Initialize session state
    initialize_session_state()
    
    # App header
    st.markdown('<h1 class="main-header">✨ CoverCraft AI ✨🚀</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.3em; background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: bold; margin-bottom: 2rem;">🎯 Transform your job search with AI-powered cover letters! 🎯</p>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("### 🎨⚙️ AI Magic Settings ⚙️🎨")
        
        # Temperature slider
        temperature = st.slider(
            "🌡️ Creativity Level",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Lower values (0.0-0.3) for more focused/conservative responses. Higher values (0.7-1.0) for more creative/varied responses."
        )
        
        # Tone selection
        st.markdown("**🎯 Cover Letter Tone:**")
        tone_options = {
            "Professional and Confident": "Write in a professional, confident tone that demonstrates expertise and leadership qualities. Show authority in your field while remaining respectful.",
            "Enthusiastic and Energetic": "Write with enthusiasm and energy, showing genuine excitement about the opportunity. Use dynamic language that conveys passion and motivation.",
            "Formal and Traditional": "Write in a formal, traditional business tone. Use conservative language appropriate for established, corporate environments.",
            "Friendly and Approachable": "Write in a warm, friendly tone that shows personality while maintaining professionalism. Demonstrate cultural fit and collaborative spirit."
        }
        
        # Create tone selection buttons
        selected_tone = st.radio(
            "Choose your preferred tone:",
            options=list(tone_options.keys()),
            index=0,
            help="Select the tone that best fits the company culture and position you're applying for."
        )
        
        # Show tone description
        with st.expander("ℹ️ About this tone"):
            st.write(tone_options[selected_tone])
        
        st.markdown("---")
        st.markdown("### 📋🌟 How to Get Started 🌟📋")
        st.markdown("""
        1. **Adjust AI settings** (creativity level and tone)
        2. **Upload your CV** as a PDF file
        3. **Paste the job description** in the text area
        4. **Click 'Generate Cover Letter'** to create a tailored cover letter
        """)
        
        st.markdown("---")
        st.markdown("### ✨ Quick CV Analysis ✨📊")
        
        # Quick scoring button
        if st.button("🎯 Analyze CV Match", help="Get a quick match score without generating a cover letter", use_container_width=True):
            if st.session_state.api_key_set and st.session_state.cv_text and st.session_state.job_description:
                with st.spinner("📊 Analyzing match... "):
                    try:
                        agent = CoverLetterAgent(temperature=temperature)
                        scoring_result = agent.score_cv_match(
                            st.session_state.cv_text,
                            st.session_state.job_description
                        )
                        st.session_state.cv_score = scoring_result
                        st.success(f"✅ Analysis complete! Score: {scoring_result['stars']}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                missing = []
                if not st.session_state.api_key_set:
                    missing.append("API key")
                if not st.session_state.cv_text:
                    missing.append("CV upload")
                if not st.session_state.job_description:
                    missing.append("job description")
                st.warning(f"⚠️ Please provide: {', '.join(missing)}")
        
        st.markdown("---")
        st.markdown("### ✨ About CoverCraft AI ✨💡")
        st.markdown("""
        🚀 Welcome to the future of job applications! This magical app uses cutting-edge AI to analyze your CV and dream job description, then crafts a personalized cover letter that makes you shine brighter than a diamond! ✨💎
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">✨ Upload Your Amazing CV ✨📋</h2>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type="pdf",
            help="Upload your CV in PDF format"
        )
        
        if uploaded_file is not None:
            with st.spinner("Extracting text from PDF..."):
                cv_text = extract_text_from_pdf(uploaded_file)
                
                if cv_text:
                    if validate_pdf_content(cv_text):
                        st.session_state.cv_text = cv_text
                        st.markdown('<div class="success-box">✅ CV uploaded and processed successfully!</div>', unsafe_allow_html=True)
                        
                        # Show preview of extracted text
                        with st.expander("📖 Preview Extracted Text"):
                            st.text_area(
                                "CV Content (first 500 characters)",
                                value=cv_text[:500] + "..." if len(cv_text) > 500 else cv_text,
                                height=200,
                                disabled=True
                            )
                    else:
                        st.error("⚠️ The uploaded file doesn't appear to be a valid CV. Please check the content and try again.")
                        st.session_state.cv_text = ""
                else:
                    st.error("❌ Failed to extract text from the PDF. Please try a different file.")
                    st.session_state.cv_text = ""
    
    with col2:
        st.markdown('<h2 class="section-header">✨ Dream Job Description ✨💼</h2>', unsafe_allow_html=True)
        
        job_description = st.text_area(
            "Paste the job description here",
            height=350,
            placeholder="Copy and paste the complete job description, including requirements, responsibilities, and company information...",
            help="Include as much detail as possible for better cover letter generation"
        )
        
        if job_description:
            st.session_state.job_description = job_description
            st.markdown('<div class="success-box">✅ Job description added!</div>', unsafe_allow_html=True)
            
            # Show word count
            word_count = len(job_description.split())
            st.info(f"📊 Word count: {word_count}")
    
    # Display CV Match Score (if available)
    if st.session_state.cv_score:
        st.markdown('<h2 class="section-header">📊✨ CV Match Analysis ✨📊</h2>', unsafe_allow_html=True)
        
        score_data = st.session_state.cv_score
        
        # Display score prominently
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; margin: 1rem 0;">
                <h1 style="color: white; font-size: 3rem; margin: 0;">{score_data['stars']}</h1>
                <h2 style="color: white; margin: 0.5rem 0;">Match Score: {score_data['score']}/5</h2>
                <p style="color: white; font-size: 1.2rem; margin: 0;">
                    {'Perfect Match!' if score_data['score'] == 5 else 
                     'Excellent Match!' if score_data['score'] == 4 else
                     'Good Match!' if score_data['score'] == 3 else
                     'Fair Match' if score_data['score'] == 2 else
                     'Needs Improvement'}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed analysis in expandable sections
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.expander("📈 Strengths & Analysis", expanded=True):
                st.markdown("**🎯 Analysis:**")
                st.write(score_data['analysis'])
                st.markdown("**💪 Strengths:**")
                st.write(score_data['strengths'])
        
        with col2:
            with st.expander("📋 Areas for Improvement", expanded=True):
                st.markdown("**🔍 Gaps Identified:**")
                st.write(score_data['gaps'])
                st.markdown("**🚀 Recommendations:**")
                st.write(score_data['recommendations'])
        
        # Re-analyze button
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🔄 Re-analyze Match", help="Generate a new CV match analysis"):
                if st.session_state.api_key_set and st.session_state.cv_text and st.session_state.job_description:
                    with st.spinner("📊 Re-analyzing CV-Job match... "):
                        try:
                            agent = CoverLetterAgent(temperature=temperature)
                            scoring_result = agent.score_cv_match(
                                st.session_state.cv_text,
                                st.session_state.job_description
                            )
                            st.session_state.cv_score = scoring_result
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error re-analyzing: {str(e)}")
    
    # Cover letter generation section
    st.markdown('<h2 class="section-header">🎉✨ Craft Your Perfect Cover Letter ✨🎉</h2>', unsafe_allow_html=True)
    
    # Check if all requirements are met
    requirements_met = (
        st.session_state.api_key_set and 
        st.session_state.cv_text and 
        st.session_state.job_description
    )
    
    if not requirements_met:
        missing_items = []
        if not st.session_state.api_key_set:
            missing_items.append("OpenAI API key")
        if not st.session_state.cv_text:
            missing_items.append("CV upload")
        if not st.session_state.job_description:
            missing_items.append("Job description")
        
        st.warning(f"⚠️ Please complete the following before generating a cover letter: {', '.join(missing_items)}")
    
    # Generate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_button = st.button(
            "🎉✨ Create My Dream Cover Letter! ✨🎉",
            disabled=not requirements_met,
            use_container_width=True,
            type="primary"
        )
    
    # Generate cover letter
    if generate_button and requirements_met:
        with st.spinner("🎨✨ AI is crafting your amazing cover letter... Magic in progress! ✨🎨"):
            try:
                # Initialize the agent with custom temperature
                agent = CoverLetterAgent(temperature=temperature)
                
                # Validate inputs
                is_valid, error_message = agent.validate_inputs(
                    st.session_state.cv_text, 
                    st.session_state.job_description
                )
                
                if not is_valid:
                    st.error(f"❌ {error_message}")
                    return
                
                # Generate cover letter with selected tone
                cover_letter = agent.generate_cover_letter(
                    st.session_state.cv_text,
                    st.session_state.job_description,
                    tone=tone_options[selected_tone]
                )
                
                if cover_letter:
                    st.session_state.cover_letter = cover_letter
                    st.success("🎉🌟 Amazing! Your cover letter has been crafted to perfection! 🌟🎉")
                else:
                    st.error("❌ Failed to generate cover letter. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
    
    # Display generated cover letter
    if st.session_state.cover_letter:
        st.markdown('<h2 class="section-header">🏆✨ Your Masterpiece Cover Letter ✨🏆</h2>', unsafe_allow_html=True)
        
        # Cover letter display and editing
        cover_letter_edited = st.text_area(
            "Generated Cover Letter (you can edit this)",
            value=st.session_state.cover_letter,
            height=500,
            help="You can edit the generated cover letter before using it"
        )
        
        # Update session state if edited
        st.session_state.cover_letter = cover_letter_edited
        
        # Download buttons
        st.markdown("### 📥✨ Download Your Masterpiece ✨📥")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.download_button(
                label="📄 Download as Text",
                data=cover_letter_edited,
                file_name="cover_letter.txt",
                mime="text/plain",
                use_container_width=True,
                help="Download as a plain text file" 
            )
        
        with col3:
            try:
                # Extract applicant name for PDF filename
                lines = cover_letter_edited.split('\n')[:3]
                applicant_name = "[Your Name]"
                for line in lines:
                    if line.strip() and not line.strip().lower().startswith(('dear', 'to whom', 'hiring')):
                        # Try to find a name-like line
                        words = line.strip().split()
                        if 2 <= len(words) <= 4 and not any(word.lower() in ['sincerely', 'regards', 'yours'] for word in words):
                            applicant_name = line.strip()
                            break
                
                # Generate PDF
                pdf_data = create_cover_letter_pdf(cover_letter_edited, applicant_name)
                pdf_filename = format_filename(applicant_name)
                
                st.download_button(
                    label="📋 Download as PDF",
                    data=pdf_data,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    use_container_width=True,
                    help="Download as a formatted PDF document"
                )
            except Exception as e:
                st.error(f"PDF generation error: {str(e)}")
                st.download_button(
                    label="📋 PDF (Install reportlab)",
                    data="",
                    file_name="error.txt",
                    disabled=True,
                    use_container_width=True,
                    help="Install reportlab package for PDF generation"
                )
        
        # Word count for cover letter
        word_count = len(cover_letter_edited.split())
        st.info(f"📊 Cover letter word count: {word_count}")
        
        # Tips section
        with st.expander("💡 Tips for Using Your Cover Letter"):
            st.markdown("""
            - **Review and personalize**: Always review the generated content and add personal touches
            - **Company research**: Add specific details about the company if not already included
            - **Proofread**: Check for any errors or awkward phrasing
            - **Download options**: Choose text format for editing or PDF for professional submission
            - **PDF formatting**: The PDF version includes professional formatting and spacing
            - **Customize**: Tailor the greeting and closing if you know the hiring manager's name
            - **Tone adjustments**: If the tone doesn't feel right, try regenerating with a different tone setting
            - **Creativity level**: Lower creativity (0.0-0.3) for conservative fields, higher (0.7-1.0) for creative roles
            """)

if __name__ == "__main__":
    main()
