"""
LangChain agent for generating cover letters based on CV and job description.
"""

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
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
        
        # Create the modern LangChain chain using prompt | llm
        self.chain = self.prompt_template | self.llm
        
        # Define the prompt template for CV scoring
        self.scoring_prompt_template = PromptTemplate(
            input_variables=["cv_content", "job_description"],
            template="""
You are an expert HR professional and career advisor. Analyze how well the provided CV matches the job description and provide a detailed scoring assessment.

CV Content:
{cv_content}

Job Description:
{job_description}

Instructions:
1. Carefully analyze the alignment between the CV and job description
2. Consider these key factors:
   - Required skills and qualifications match
   - Experience level and years of experience
   - Educational background alignment
   - Industry/domain knowledge
   - Technical skills and tools mentioned
   - Soft skills and competencies
   - Career progression and achievements relevance

3. Provide a score from 1 to 5 stars based on overall fit:
   - ⭐ (1 star): Poor match - Major gaps in requirements
   - ⭐⭐ (2 stars): Below average match - Some relevant experience but significant gaps
   - ⭐⭐⭐ (3 stars): Good match - Meets most requirements with minor gaps
   - ⭐⭐⭐⭐ (4 stars): Excellent match - Strong alignment with most/all requirements
   - ⭐⭐⭐⭐⭐ (5 stars): Perfect match - Exceeds requirements significantly

4. Your response MUST follow this exact format:
SCORE: [1-5]
ANALYSIS: [Detailed explanation of the scoring rationale]
STRENGTHS: [Key matching points between CV and job]
GAPS: [Areas where CV doesn't fully meet job requirements]
RECOMMENDATIONS: [Suggestions to improve the application]

Provide your assessment:
            """
        )
        
        # Create the modern scoring chain using prompt | llm
        self.scoring_chain = self.scoring_prompt_template | self.llm
    
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
            
            # Generate the cover letter using the modern chain
            result = self.chain.invoke({
                "cv_content": cv_content,
                "job_description": job_description,
                "applicant_name": applicant_name or "[Your Name]",
                "tone": tone
            })
            
            # Extract content from AIMessage object
            return result.content
            
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
    
    def score_cv_match(self, cv_content, job_description):
        """
        Score how well the CV matches the job description out of 5 stars.
        
        Args:
            cv_content (str): Extracted text from the CV
            job_description (str): Job description text
            
        Returns:
            dict: Dictionary containing score, analysis, strengths, gaps, and recommendations
        """
        try:
            # Generate the scoring assessment using the modern chain
            result = self.scoring_chain.invoke({
                "cv_content": cv_content,
                "job_description": job_description
            })
            
            # Extract content from AIMessage object and parse the structured response
            parsed_result = self._parse_scoring_result(result.content)
            return parsed_result
            
        except Exception as e:
            st.error(f"Error scoring CV match: {str(e)}")
            return {
                "score": 0,
                "stars": "",
                "analysis": "Error occurred during scoring",
                "strengths": "Unable to analyze",
                "gaps": "Unable to analyze", 
                "recommendations": "Please try again"
            }
    
    def _parse_scoring_result(self, result):
        """
        Parse the structured scoring result from the LLM.
        
        Args:
            result (str): Raw result from the scoring chain
            
        Returns:
            dict: Parsed scoring components
        """
        # Initialize with defaults
        parsed = {
            "score": 3,
            "stars": "⭐⭐⭐",
            "analysis": "Analysis not available",
            "strengths": "Not specified",
            "gaps": "Not specified",
            "recommendations": "Not specified"
        }
        
        try:
            lines = result.strip().split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('SCORE:'):
                    score_text = line.replace('SCORE:', '').strip()
                    # Extract number from score text
                    import re
                    score_match = re.search(r'(\d+)', score_text)
                    if score_match:
                        score = int(score_match.group(1))
                        parsed["score"] = max(1, min(5, score))  # Ensure score is between 1-5
                        parsed["stars"] = "⭐" * parsed["score"]
                        
                elif line.startswith('ANALYSIS:'):
                    current_section = "analysis"
                    parsed["analysis"] = line.replace('ANALYSIS:', '').strip()
                    
                elif line.startswith('STRENGTHS:'):
                    current_section = "strengths"
                    parsed["strengths"] = line.replace('STRENGTHS:', '').strip()
                    
                elif line.startswith('GAPS:'):
                    current_section = "gaps"
                    parsed["gaps"] = line.replace('GAPS:', '').strip()
                    
                elif line.startswith('RECOMMENDATIONS:'):
                    current_section = "recommendations"
                    parsed["recommendations"] = line.replace('RECOMMENDATIONS:', '').strip()
                    
                elif line and current_section and not line.startswith(('SCORE:', 'ANALYSIS:', 'STRENGTHS:', 'GAPS:', 'RECOMMENDATIONS:')):
                    # Continue building the current section
                    parsed[current_section] += " " + line
                    
        except Exception as e:
            print(f"Error parsing scoring result: {e}")
            
        return parsed
