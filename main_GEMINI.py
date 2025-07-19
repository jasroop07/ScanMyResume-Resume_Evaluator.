from dotenv import load_dotenv
load_dotenv()
import base64
import json
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import google.generativeai as genai


load_dotenv() ## load all our environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#PREPROCESS INPUT RESUME
def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text




#USING GOOGLE GEMINI MODEL
model=genai.GenerativeModel('gemini-2.0-flash')


# Function to get ATS feedback using GEMINI model
def get_ats_feedback_GEMINI(resume, job_description):
    textt = input_pdf_text(resume)
    
    if not textt.strip():
        return "❌ Could not extract text from the PDF. Please check the file."

    # Double curly braces {{}} to escape in .format()
    input_prompt = """
Hey, act like a highly skilled ATS (Applicant Tracking System) specialized in evaluating resumes 
for roles in tech, data science, software engineering, and big data.

### Task:
- Evaluate the candidate **resume** against the given **job description (JD)**
- Score the match as a percentage
- Highlight **strong points** in the resume
- List **missing keywords or skills**
- Provide **specific suggestions for improvement**

Be concise, accurate, and realistic — assume a competitive job market.

Resume:
{resume_textt}

Job Description:
{job_description}

### Output format (as a single string, exactly this structure):
{{"ATS Score: <score>%", "Strong points: <...>", "Suggestions: <...>"}} 
Only output the structured string, no extra commentary.
    """.format(resume_textt=textt, job_description=job_description)
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(input_prompt)
    return response.text




# Example usage
resume="/Users/jasroopsingh/Desktop/resume_ats/jasroop_final_resume (1) (1).pdf"
job_description="""We are looking for a passionate and results-driven Data Scientist to join our AI research and development team. You will work closely with data engineers, ML engineers, and product managers to build predictive models and extract actionable insights from structured and unstructured datasets.
"""
feedback = get_ats_feedback_GEMINI(resume, job_description)
#print(feedback)


