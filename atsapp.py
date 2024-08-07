import streamlit as st
import openai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can choose another engine if you prefer
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text() or ""
    return text

# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experienced ATS (Applicant Tracking System)
with a deep understanding of tech field, software engineering, data science, data analysis,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on JD and
the missing keywords with high accuracy.
resume: {text}
description: {jd}

I want the response in one single string having the structure:
{{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
"""

# Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd.strip():
        resume_text = input_pdf_text(uploaded_file)
        prompt = input_prompt.format(text=resume_text, jd=jd)
        response = get_openai_response(prompt)
        st.subheader("Evaluation Result")
        st.text(response)
    else:
        st.error("Please upload a PDF resume and provide a job description.")

