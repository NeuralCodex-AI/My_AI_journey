from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import uuid
from resume import process_resume
from rag import (
    create_vector_store,
    compare_resume_with_jd,
    analyze_ats,
    generate_technical_question,
    generate_hr_question,
    evaluate_answer,
    generate_follow_up
)
from scoring import (
    calculate_technical_score,
    calculate_hr_score,
    calculate_overall_score,
    get_grade
)
from roadmap import create_learning_roadmap
from report import create_final_report
from database import (
    save_resume,
    save_job_description,
    create_interview_session,
    save_question,
    save_answer,
    update_interview_result,
    save_report,
    get_user_by_id
)

app = FastAPI(
    title="AI Interview Preparation Platform",
    description="AI-powered Resume Analysis and Interview Preparation API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

os.makedirs("uploads", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# User-specific session storage
user_resume_stores = {}
user_jd_stores = {}

@app.get("/")
def home():
    return {"success": True, "message": "AI Interview Preparation API is running"}

@app.post("/clear-session")
async def clear_session(user_id: int = Form(...)):
    try:
        if user_id in user_resume_stores:
            del user_resume_stores[user_id]
        if user_id in user_jd_stores:
            del user_jd_stores[user_id]
        return {"success": True, "message": "Session cleared successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    user_id: int = Form(...)
):
    try:
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in [".pdf", ".docx"]:
            return {"success": False, "error": "Only PDF and DOCX files are supported."}
        
        resume_id = str(uuid.uuid4())
        saved_filename = resume_id + file_extension
        file_path = os.path.join("uploads", saved_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result = process_resume(file_path)
        if "error" in result:
            return {"success": False, "error": result["error"]}
        
        # Save to database
        resume_id_db = save_resume(
            user_id=user_id,
            file_name=file.filename,
            resume_text=result["resume_text"]
        )
        
        # Store in user-specific session
        if user_id not in user_resume_stores:
            user_resume_stores[user_id] = {}
        user_resume_stores[user_id][resume_id] = result["vectorstore"]
        
        return {
            "success": True,
            "resume_id": resume_id,
            "resume_text": result["resume_text"],
            "analysis": result["analysis"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/job-description/analyze")
async def analyze_job_description(
    resume_id: str = Form(...),
    job_description: str = Form(...),
    user_id: int = Form(...)
):
    try:
        if user_id not in user_resume_stores or resume_id not in user_resume_stores[user_id]:
            return {"success": False, "error": "Resume session not found."}
        
        if not job_description.strip():
            return {"success": False, "error": "Job description cannot be empty."}
        
        resume_vectorstore = user_resume_stores[user_id][resume_id]
        jd_vectorstore = create_vector_store(job_description, "job_description")
        
        if user_id not in user_jd_stores:
            user_jd_stores[user_id] = {}
        user_jd_stores[user_id][resume_id] = jd_vectorstore
        
        comparison = compare_resume_with_jd(resume_vectorstore, jd_vectorstore)
        ats_analysis = analyze_ats(resume_vectorstore, jd_vectorstore)
        
        jd_id = save_job_description(
            user_id=user_id,
            job_title="Job Description",
            jd_text=job_description
        )
        
        return {
            "success": True,
            "comparison": comparison,
            "ats_analysis": ats_analysis
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/interview/technical/question")
async def technical_question(
    resume_id: str = Form(...),
    role: str = Form(...),
    difficulty: str = Form("Easy"),
    category: str = Form("Problem Solving"),
    user_id: int = Form(...)
):
    try:
        if user_id not in user_resume_stores or resume_id not in user_resume_stores[user_id]:
            return {"success": False, "error": "Resume not found."}
        
        question = generate_technical_question(
            user_resume_stores[user_id][resume_id],
            role,
            difficulty,
            category
        )
        
        session_id = create_interview_session(
            user_id=user_id,
            resume_id=1,
            jd_id=1,
            role=role,
            mode="Technical",
            difficulty=difficulty
        )
        
        question_id = save_question(
            session_id=session_id,
            question=question,
            category=category,
            interview_type="Technical",
            difficulty=difficulty,
            question_number=1
        )
        
        return {
            "success": True,
            "question": question,
            "difficulty": difficulty,
            "category": category
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/interview/hr/question")
async def hr_question(
    resume_id: str = Form(...),
    role: str = Form(...),
    category: str = Form("Communication"),
    user_id: int = Form(...)
):
    try:
        if user_id not in user_resume_stores or resume_id not in user_resume_stores[user_id]:
            return {"success": False, "error": "Resume not found."}
        
        question = generate_hr_question(
            user_resume_stores[user_id][resume_id],
            role,
            category
        )
        
        session_id = create_interview_session(
            user_id=user_id,
            resume_id=1,
            jd_id=1,
            role=role,
            mode="HR",
            difficulty="Easy"
        )
        
        question_id = save_question(
            session_id=session_id,
            question=question,
            category=category,
            interview_type="HR",
            difficulty="Easy",
            question_number=1
        )
        
        return {
            "success": True,
            "question": question,
            "category": category
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/interview/evaluate")
async def evaluate_interview_answer(
    question: str = Form(...),
    answer: str = Form(...),
    interview_type: str = Form(...)
):
    try:
        feedback = evaluate_answer(question, answer, interview_type)
        follow_up = generate_follow_up(question, answer)
        
        answer_id = save_answer(
            question_id=1,
            answer=answer,
            score=0,
            feedback=feedback,
            strengths="",
            weaknesses="",
            follow_up_question=follow_up
        )
        
        return {
            "success": True,
            "feedback": feedback,
            "follow_up": follow_up
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/roadmap/generate")
async def generate_roadmap(
    role: str = Form(...),
    weak_areas: str = Form(...),
    hours_per_week: int = Form(...)
):
    try:
        weak_area_list = [
            item.strip()
            for item in weak_areas.split(",")
            if item.strip()
        ]
        roadmap = create_learning_roadmap(
            weak_area_list,
            role,
            hours_per_week
        )
        return {
            "success": True,
            "role": role,
            "weak_areas": weak_area_list,
            "roadmap": roadmap
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/results/calculate")
async def calculate_results(
    resume_score: float = Form(...),
    technical_scores: str = Form(...),
    hr_scores: str = Form(...)
):
    try:
        technical_score_list = [
            float(score.strip())
            for score in technical_scores.split(",")
            if score.strip()
        ]
        hr_score_list = [
            float(score.strip())
            for score in hr_scores.split(",")
            if score.strip()
        ]
        
        technical_score = calculate_technical_score(technical_score_list)
        hr_score = calculate_hr_score(hr_score_list)
        overall_score = calculate_overall_score(resume_score, technical_score, hr_score)
        grade = get_grade(overall_score)
        
        update_interview_result(
            session_id=1,
            resume_score=resume_score,
            ats_score=0,
            technical_score=technical_score,
            hr_score=hr_score,
            overall_score=overall_score,
            grade=grade
        )
        
        return {
            "success": True,
            "resume_score": resume_score,
            "technical_score": technical_score,
            "hr_score": hr_score,
            "overall_score": overall_score,
            "grade": grade
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/report/generate")
async def generate_report(
    candidate_name: str = Form(...),
    target_role: str = Form(...),
    resume_score: float = Form(...),
    ats_score: float = Form(...),
    technical_score: float = Form(...),
    hr_score: float = Form(...),
    overall_score: float = Form(...),
    grade: str = Form(...),
    strengths: str = Form(...),
    weak_areas: str = Form(...),
    missing_skills: str = Form(...),
    roadmap: str = Form(...),
    user_id: int = Form(...)
):
    try:
        report_id = str(uuid.uuid4())
        output_path = os.path.join("reports", f"report_{report_id}.pdf")
        
        strengths_list = [
            item.strip()
            for item in strengths.split(",")
            if item.strip()
        ]
        weak_areas_list = [
            item.strip()
            for item in weak_areas.split(",")
            if item.strip()
        ]
        missing_skills_list = [
            item.strip()
            for item in missing_skills.split(",")
            if item.strip()
        ]
        
        create_final_report(
            candidate_name,
            target_role,
            resume_score,
            ats_score,
            technical_score,
            hr_score,
            overall_score,
            grade,
            strengths_list,
            weak_areas_list,
            missing_skills_list,
            roadmap,
            output_path
        )
        
        report_id_db = save_report(
            user_id=user_id,
            session_id=1,
            file_path=output_path,
            share_token=str(uuid.uuid4())
        )
        
        return {
            "success": True,
            "report_path": output_path
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )