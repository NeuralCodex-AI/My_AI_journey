import fitz
import spacy
from google import genai
import streamlit as st
import pandas as pd
from spacy.matcher import PhraseMatcher

client=genai.Client(api_key="YOUR_API_KEY")


st.title("AI Resume Analyzer")

df=pd.read_csv("skill.csv")  #load csv file 
skills=df["Skill"].tolist()

nlp=spacy.load("en_core_web_sm")
matcher=PhraseMatcher(nlp.vocab)
pattern=[nlp(skill) for skill in skills]
matcher.add("Skills",pattern)

def text_extraction(doc): 
    text = ""
    if doc is not None:
         with fitz.open(stream=doc.read(), filetype="pdf") as pdf:  
            for page in pdf:
                text += page.get_text()
         return text
    return 

def skill_matcher(text):
    doc=nlp(text)
    matches=matcher(doc)
    found_skill=[]
    for match_id,start,end in matches:
        found_skill.append(doc[start:end].text)
    return list(set(found_skill))
 

upload_file = st.file_uploader("Enter the resume", type="pdf")
resume_skill=[]

if upload_file is not None:
    text=text_extraction(upload_file)
    resume_skill=skill_matcher(text.lower()) # extract skill from Resume

JD_text=st.text_area("enter the job description here....")

if upload_file is not None and JD_text:

    JD_skill=skill_matcher(JD_text.lower()) # extract skill from JD 

    match_skill=list(set(JD_skill)&set(resume_skill))
    missing_skill=list(set(JD_skill)-set(resume_skill))
    if len(JD_skill)>0:
        match_score=(len(match_skill)/len(JD_skill))*100
    else:
        match_score=0
    
    st.subheader("Analysis")
    st.write("Resume Skills:", resume_skill)
    st.write("JD Skills:", JD_skill)
    st.write("Matched Skills:", match_skill)
    st.write("Missing Skills:", missing_skill)
    st.metric("Match Score", match_score)

        
    prompt = f"""
        Use ONLY the information provided below. Do NOT make assumptions.
        Resume_data: {text}
        Job_discription:{JD_text}
        Resume Skills: {resume_skill}
        Job Description Skills: {JD_skill}
        Matched Skills: {match_skill}
        Missing Skills: {missing_skill}
        Match Score: {match_score}%
        
        Answer the following questions point to point .
        1. What are the strengths of this resume?
        2. What are the weaknesses of this resume, ?
        3. tell the name of skills should the candidate learn or add?
        4. Which projects should the candidate build?
        5. Explain how the candidate can increase the match score.
        6. Is the candidate suitable for this job? Why or why not?"""
    try:
        response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
        )
        st.subheader("AI_Analysis.....")
        st.write(response.text) 
    except Exception as e:
        st.error(f"ERROR: {e}")

       
else:
    st.write("pls enter the resume and JD")

