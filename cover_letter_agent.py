"""
LangChain agent for generating cover letters based on CV and job description.
"""

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st


class CoverLetterAgent:
    """Agent responsible for generating cover letters using OpenAI and LangChain."""
    
    def __init__(self, api_key=None, temperature=0.7):
        """
        Initialize the cover letter agent.
        
        Args:
            api_key (str): OpenAI API key
            temperature (float): Temperature parameter for LLM (0.0 to 1.0)
        """
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        # Initialize the OpenAI chat model
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=temperature,
            max_tokens=8000
        )
        
        # Define the prompt template for cover letter generation
        self.prompt_template = PromptTemplate(
            input_variables=["cv_content", "job_description", "applicant_name", "tone"],
            template="""
You are an expert career advisor and cover letter writer. Based on the provided CV and job description, 
create a professional, compelling cover letter that highlights the applicant's most relevant qualifications 
and demonstrates their suitability for the position.

CV Content:
{cv_content}

Job Description:
{job_description}

Tone Instructions:
{tone}

Instructions:
1. Write a comprehensive, detailed cover letter that is approximately 4-6 paragraphs long
2. Follow the specified tone while maintaining professionalism
3. Provide specific examples and detailed explanations of relevant skills, experiences, and achievements from the CV that match the job requirements
4. Show genuine enthusiasm for the role and company with specific reasons why you're interested
5. Include a strong, compelling opening that immediately grabs attention
6. Dedicate sufficient space to explain how your background aligns with each major requirement
7. Include a paragraph about your understanding of the company/role and why you're a great fit
8. End with a confident call to action
9. If the applicant's name is not clearly identifiable from the CV, use "[Your Name]" as a placeholder
10. Use "[Company Name]" and "[Hiring Manager]" as placeholders if not specified in the job description

Applicant Name (if identified): {applicant_name}

Generate a professional cover letter:
            """
        )
        
        # Create the LangChain chain
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template
        )
    
    def extract_applicant_name(self, cv_text):
        """
        Attempt to extract the applicant's name from the CV text.
        
        Args:
            cv_text (str): The extracted CV text
            
        Returns:
            str: The applicant's name or None if not found
        """
        # Simple name extraction - look for name patterns at the beginning of the CV
        lines = cv_text.split('\n')[:5]  # Check first 5 lines
        
        for line in lines:
            line = line.strip()
            # Skip empty lines and common CV headers
            if not line or line.lower() in ['cv', 'resume', 'curriculum vitae']:
                continue
            
            # If line has 2-4 words and doesn't contain common CV keywords, it might be a name
            words = line.split()
            if (2 <= len(words) <= 4 and 
                not any(keyword in line.lower() for keyword in 
                       ['phone', 'email', 'address', 'linkedin', 'experience', 'education'])):
                return line
        
        return None
    
    def generate_cover_letter(self, cv_content, job_description, tone="Professional and confident"):
        """
        Generate a cover letter based on CV content and job description.
        
        Args:
            cv_content (str): Extracted text from the CV
            job_description (str): Job description text
            tone (str): Tone/style for the cover letter
            
        Returns:
            str: Generated cover letter
        """
        try:
            # Extract applicant name
            applicant_name = self.extract_applicant_name(cv_content)
            
            # Generate the cover letter using the chain
            result = self.chain.run(
                cv_content=cv_content,
                job_description=job_description,
                applicant_name=applicant_name or "[Your Name]",
                tone=tone
            )
            
            return result
            
        except Exception as e:
            st.error(f"Error generating cover letter: {str(e)}")
            return None
    
    def validate_inputs(self, cv_content, job_description):
        """
        Validate that the inputs are sufficient for cover letter generation.
        
        Args:
            cv_content (str): CV content
            job_description (str): Job description
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not cv_content or len(cv_content.strip()) < 50:
            return False, "CV content is too short or empty. Please upload a valid CV."
        
        if not job_description or len(job_description.strip()) < 50:
            return False, "Job description is too short or empty. Please provide a detailed job description."
        
        return True, None
