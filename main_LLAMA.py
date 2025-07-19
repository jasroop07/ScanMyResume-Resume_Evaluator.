from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv 
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json



load_dotenv()  # Load environment variables from .env file
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

#PREPROCESS INPUT RESUME
def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

# USING LLAMA MODEL
llm =ChatGroq(
    model_name="llama3-70b-8192",
    groq_api_key=GROQ_API_KEY,
    temperature=0.7
)

# response = llm.invoke("What is the capital of india?")
# print(response)




# Function to get ATS feedback using LLAMA model
def get_ats_feedback_LLAMA(resume_path, job_description):
    text = input_pdf_text(resume_path)

    if not text.strip():
        return "❌ Could not extract text from the PDF. Please check the file."

    prompt = PromptTemplate.from_template(
"""
You are an advanced ATS (Applicant Tracking System) assistant.

### Task:
- Evaluate the resume text below against the given job description.
- Provide a match score (in %)
- Mention 2–3 strong points from the resume.
- Suggest 2–3 specific improvements or missing skills.

Be concise and realistic. Output should be **well-structured text** — readable on a web page.

Resume:
{text}

Job Description:
{job_description}

### Output format (plain text, structured):
ATS Score: <score>%

Strong Points:
- Point 1
- Point 2
- Point 3

Suggestions:
- Suggestion 1
- Suggestion 2
- Suggestion 3
"""
    )

    formatted_prompt = prompt.format(text=text, job_description=job_description)

    # Define the LLM chain
    chain = prompt | llm | StrOutputParser()

    # Run the chain
   
    result = chain.invoke({
        "text": text,
        "job_description": job_description
    })
    return result



# Example usage
resume="/Users/jasroopsingh/Desktop/resume_ats/jasroop_final_resume (1) (1).pdf"
job_description="""We are looking for a passionate and results-driven Data Scientist to join our AI research and development team. You will work closely with data engineers, ML engineers, and product managers to build predictive models and extract actionable insights from structured and unstructured datasets.
"""
feedback = get_ats_feedback_LLAMA(resume, job_description)
#print(feedback)





# # 4. Output parser to extract the string
# parser = StrOutputParser()

# # 5. Create the full chain
# chain = prompt | llm | parser

# # 6. Example review
# review_text = "I had a very disappointing experience with Dr. Big. The consultation felt rushed, and I barely had time to explain my symptoms before being cut off. He seemed disinterested and offered little explanation about the diagnosis or treatment. The prescribed medication didn’t improve my condition and led to side effects. I had to follow up multiple times just to get basic clarification. The staff wasn't very helpful either, making the overall visit frustrating. I wouldn’t recommend this clinic based on my experience."



# # 7. Run the chain
# response = chain.invoke({"review": review_text})

# print(response)