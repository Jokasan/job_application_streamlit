# Job Application Helper 📄

A Streamlit application that helps job applicants create tailored cover letters using AI. The app analyzes your CV and job descriptions to generate personalized, professional cover letters.

## Features ✨

- **PDF CV Upload**: Upload your CV in PDF format for automatic text extraction
- **Job Description Input**: Paste job descriptions for analysis
- **AI-Powered Generation**: Uses OpenAI's GPT models via LangChain to create tailored cover letters
- **Interactive Editing**: Edit generated cover letters before downloading
- **Multiple Download Formats**: Download your cover letter as text or professionally formatted PDF
- **Customizable AI Settings**: Adjust creativity level and tone for personalized results
- **Professional Formatting**: Clean, user-friendly interface with helpful guidance

## Setup Instructions 🚀

### Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone or download the project**:
   ```bash
   cd job_application_streamlit
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```
   
   Alternatively, you can enter your API key directly in the app's sidebar.

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## How to Use 📋

1. **Configure API Key**: Enter your OpenAI API key in the sidebar
2. **Upload CV**: Upload your CV as a PDF file
3. **Add Job Description**: Copy and paste the complete job description
4. **Generate Cover Letter**: Click the generate button to create your cover letter
5. **Review and Edit**: Review the generated content and make any necessary edits
6. **Download**: Download your final cover letter as a text file

## File Structure 📁

```
job_application_streamlit/
├── app.py                    # Main Streamlit application
├── cover_letter_agent.py     # LangChain agent for cover letter generation
├── pdf_utils.py              # PDF parsing utilities
├── pdf_generator.py          # PDF generation utilities
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Dependencies 📦

- **streamlit**: Web app framework
- **langchain**: AI framework for building applications
- **langchain-openai**: OpenAI integration for LangChain
- **openai**: OpenAI API client
- **PyPDF2**: PDF text extraction
- **reportlab**: PDF generation for downloads
- **python-dotenv**: Environment variable management
- **tiktoken**: Token counting for OpenAI models

## Tips for Best Results 💡

### CV Upload
- Ensure your CV is in PDF format
- Use a clean, well-formatted CV
- Include comprehensive information about your experience and skills

### Job Description
- Include the complete job description
- Copy all relevant details including requirements and responsibilities
- Include company information if available

### Generated Cover Letters
- Always review and personalize the generated content
- Add specific company details if not already included
- Proofread for any errors or awkward phrasing
- Format according to standard business letter format when using

## Troubleshooting 🔧

### Common Issues

1. **"Error reading PDF file"**:
   - Ensure the PDF is not password-protected
   - Try a different PDF file
   - Check that the PDF contains selectable text (not just images)

2. **"API key not working"**:
   - Verify your OpenAI API key is correct
   - Check that you have sufficient credits in your OpenAI account
   - Ensure the API key has the necessary permissions

3. **"Cover letter generation failed"**:
   - Check your internet connection
   - Verify both CV and job description are substantial (not too short)
   - Try again as it might be a temporary API issue

## Security Notes 🔒

- Your API key is only stored temporarily in the app session
- CV content and job descriptions are sent to OpenAI for processing
- Generated cover letters are not stored permanently
- Always review generated content before using

## Support 📞

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure your OpenAI API key is valid and has sufficient credits

## License 📄

This project is open source. Feel free to modify and distribute as needed.
