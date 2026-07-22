from config import GOOGLE_API_KEY
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)
from langchain_core.documents import Document
from langchain_core.prompts import (
    ChatPromptTemplate
)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

def create_documents(
    text,
    document_type
):
    """
    Convert text into LangChain Documents
    and split the document into chunks.
    """
    document = Document(
        page_content=text,
        metadata={
            "type": document_type
        }
    )
    chunks = splitter.split_documents(
        [document]
    )
    return chunks
def create_vector_store(
    text,
    document_type
):
    """
    Create embeddings for document chunks
    and store them inside FAISS.
    """
    documents = create_documents(
        text,
        document_type
    )
    vectorstore = FAISS.from_documents(
        documents,
        embeddings
    )
    return vectorstore
def save_vector_store(
    vectorstore,
    path
):
    """
    Save FAISS vector database locally.
    """
    vectorstore.save_local(
        path
    )
def load_vector_store(
    path
):
    """
    Load previously saved FAISS vector database.
    """
    vectorstore = FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore
def retrieve(
    vectorstore,
    question
):
    """
    Retrieve the most relevant chunks
    from FAISS according to the question.
    """
    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 4
        }
    )
    documents = retriever.invoke(
        question
    )
    return documents
def get_context(
    vectorstore,
    question
):
    """
    Get relevant text from FAISS
    to provide context to Gemini.
    """
    documents = retrieve(
        vectorstore,
        question
    )
    context = "\n\n".join(
        document.page_content
        for document in documents
    )
    return context
def ask_rag(
    vectorstore,
    question
):
    """
    General RAG question answering.
    FAISS:
        Retrieves relevant information.
    Gemini:
        Generates answer using retrieved context.
    """
    context = get_context(
        vectorstore,
        question
    )
    prompt = ChatPromptTemplate.from_template(
        """
        You are an AI Career Assistant.
        Use ONLY the provided candidate context
        to answer the question.
        Candidate Context:
        {context}
        Question:
        {question}
        Rules:
        1. Do not invent information.
        2. Do not assume information.
        3. Use only the provided context.
        4. If information is not available,
           say:
           "Information not found in the context."
        """
    )
    chain = prompt | llm
    response = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )
    return response.content
def analyze_resume(
    resume_vectorstore
):
    """
    Analyze resume using RAG.
    Extracts:
    - Skills
    - Experience
    - Education
    - Projects
    - Certifications
    Also gives:
    - Strengths
    - Weaknesses
    - Suggestions
    """
    context = get_context(
        resume_vectorstore,
        """
        Find all information about:
        Skills
        Work Experience
        Education
        Projects
        Certifications
        Achievements
        """
    )
    prompt = f"""
    You are an expert resume analyzer.
    Analyze ONLY the following resume context:
    {context}
    Extract and explain:
    1. Skills
    2. Work Experience
    3. Education
    4. Projects
    5. Certifications
    6. Achievements
    Then provide:
    7. Resume Strengths
    8. Resume Weaknesses
    9. Resume Improvement Suggestions
    Give clear and structured feedback.
    Do not invent information that is not
    available in the resume.
    """
    response = llm.invoke(
        prompt
    )
    return response.content
def calculate_resume_score(
    resume_vectorstore
):
    """
    Calculate resume strength score.
    Score is based on:
    Skills       = 20%
    Experience   = 20%
    Education    = 15%
    Projects     = 15%
    Certifications = 10%
    Achievements = 10%
    Completeness = 10%
    Total = 100%
    """
    context = get_context(
        resume_vectorstore,
        """
        Find whether the resume contains:
        Skills
        Work Experience
        Education
        Projects
        Certifications
        Achievements
        Contact Information
        Professional Summary
        """
    )
    prompt = f"""
    You are a resume scoring expert.
    Analyze this resume context:
    {context}
    Give a score from 0 to 10 for each:
    Skills
    Experience
    Education
    Projects
    Certifications
    Achievements
    Completeness
    Return ONLY this format:
    Skills: X
    Experience: X
    Education: X
    Projects: X
    Certifications: X
    Achievements: X
    Completeness: X
    Do not add any other text.
    """
    response = llm.invoke(
        prompt
    )
    result = response.content
    return result
def compare_resume_with_jd(
    resume_vectorstore,
    jd_vectorstore
):
    """
    Compare resume with Job Description.
    Finds:
    - Matching Skills
    - Missing Skills
    - Experience Match
    - Education Match
    - Qualification Gaps
    - Strengths
    - Weaknesses
    - Improvements
    """
    resume_context = get_context(
        resume_vectorstore,
        """
        Find candidate:
        Skills
        Work Experience
        Education
        Projects
        Certifications
        Qualifications
        """
    )
    jd_context = get_context(
        jd_vectorstore,
        """
        Find job requirements:
        Required Skills
        Required Experience
        Education Requirements
        Qualifications
        Responsibilities
        Preferred Skills
        """
    )
    prompt = f"""
    You are an expert recruitment analyst.
    CANDIDATE RESUME:
    {resume_context}
    JOB DESCRIPTION:
    {jd_context}
    Compare the candidate with the job.
    Analyze:
    1. Matching Skills
    2. Missing Skills
    3. Experience Match
    4. Education Match
    5. Qualification Gaps
    6. Strengths
    7. Weaknesses
    8. Recommended Improvements
    Also provide:
    9. Overall Job Match Percentage
    Give detailed and structured analysis.
    Do not invent information.
    """
    response = llm.invoke(
        prompt
    )
    return response.content
def analyze_ats(
    resume_vectorstore,
    jd_vectorstore
):
    """
    Analyze ATS compatibility.
    Checks:
    - Skill Keywords
    - Missing Keywords
    - Job Title
    - Experience
    - Education
    - Qualifications
    - Resume Structure
    - Formatting
    """
    resume_context = get_context(
        resume_vectorstore,
        """
        Find:
        Resume Skills
        Resume Keywords
        Job Titles
        Work Experience
        Education
        Qualifications
        Resume Sections
        """
    )
    jd_context = get_context(
        jd_vectorstore,
        """
        Find:
        Required Skills
        Important Keywords
        Job Title
        Qualifications
        Experience Requirements
        Education Requirements
        """
    )
    prompt = f"""
    You are an expert ATS resume analyst.
    RESUME:
    {resume_context}
    JOB DESCRIPTION:
    {jd_context}
    Analyze ATS compatibility.
    Check:
    1. Matching Skill Keywords
    2. Missing Skill Keywords
    3. Job Title Match
    4. Experience Match
    5. Education Match
    6. Required Qualifications
    7. Resume Structure
    8. ATS Formatting Problems
    9. Keywords to Add
    10. ATS Improvement Suggestions
    Also estimate:
    11. ATS Score out of 100
    Explain clearly how the score
    was estimated.
    Give actionable suggestions.
    """
    response = llm.invoke(
        prompt
    )
    return response.content
def generate_technical_question(
    resume_vectorstore,
    role,
    difficulty,
    category
):
    """
    Generate resume-aware technical question.
    """
    context = get_context(
        resume_vectorstore,
        f"""
        Find candidate skills
        and experience related to:
        Role:
        {role}
        Category:
        {category}
        """
    )
    prompt = f"""
    You are an expert technical interviewer.
    Target Role:
    {role}
    Difficulty:
    {difficulty}
    Category:
    {category}
    Candidate Resume:
    {context}
    Generate ONE technical interview question.
    The question must:
    - Match target role
    - Match candidate skills
    - Match difficulty
    - Test real understanding
    Return ONLY the question.
    """
    response = llm.invoke(
        prompt
    )
    return response.content
def generate_hr_question(
    resume_vectorstore,
    role,
    category
):
    """
    Generate resume-aware HR question.
    Uses STAR framework.
    """
    context = get_context(
        resume_vectorstore,
        f"""
        Find candidate experiences
        related to:
        {category}
        """
    )
    prompt = f"""
    You are an expert HR interviewer.
    Target Role:
    {role}
    Category:
    {category}
    Candidate Resume:
    {context}
    Generate ONE behavioral or
    situational interview question.
    The question should encourage
    the candidate to answer using:
    Situation
    Task
    Action
    Result
    Make the question relevant
    to the candidate's experience.
    Return ONLY the question.
    """
    response = llm.invoke(
        prompt
    )
    return response.content
def evaluate_answer(
    question,
    answer,
    interview_type
):
    """
    Evaluate candidate interview answer.
    Returns feedback for:
    - Correctness
    - Relevance
    - Clarity
    - Technical Depth
    - Communication
    - Confidence
    - STAR Structure
    """
    prompt = f"""
    You are an expert interview evaluator.
    Interview Type:
    {interview_type}
    Question:
    {question}
    Candidate Answer:
    {answer}
    Evaluate the answer.
    Give:
    1. Score out of 10
    2. Correctness
    3. Relevance
    4. Clarity
    5. Technical Depth
    6. Communication Quality
    7. Confidence
    8. STAR Structure
    9. Strengths
    10. Weaknesses
    11. Improvement Suggestions
    If this is an HR interview,
    evaluate the STAR framework.
    If this is a Technical interview,
    focus on correctness and
    technical understanding.
    Give detailed feedback.
    """
    response = llm.invoke(
        prompt
    )
    return response.content
def generate_follow_up(
    question,
    answer
):
    """
    Generate adaptive follow-up question.
    If answer is incomplete,
    unclear or incorrect,
    ask one follow-up question.
    Otherwise return NO_FOLLOW_UP.
    """
    prompt = f"""
    You are conducting an adaptive interview.
    Original Question:
    {question}
    Candidate Answer:
    {answer}
    Analyze the candidate answer.
    If the answer is:
    - Incomplete
    - Unclear
    - Incorrect
    Generate ONE follow-up question.
    If the answer is complete,
    return exactly:
    NO_FOLLOW_UP
    Return only the result.
    """
    response = llm.invoke(
        prompt
    )
    return response.content.strip()
def choose_next_difficulty(
    score
):
    """
    Select next interview difficulty
    based on candidate performance.
    """
    if score >= 8:
        return "Hard"
    elif score >= 5:
        return "Medium"
    else:
        return "Easy"
def generate_learning_roadmap(
    weak_areas,
    role,
    hours_per_week
):
    """
    Generate personalized learning roadmap
    according to weak areas.
    """
    prompt = f"""
    You are an AI career learning advisor.
    Target Role:
    {role}
    Weak Areas:
    {weak_areas}
    Available Study Hours:
    {hours_per_week}
    Create a personalized learning roadmap.
    Divide topics into:
    1. Critical
    2. Important
    3. Nice-to-Have
    For every topic provide:
    - Topic
    - Reason
    - Estimated Learning Time
    - Recommended Resource
    - Mini Project
    - Milestone
    Also create:
    Weekly Study Plan
    Give practical and actionable roadmap.
    """
    response = llm.invoke(
        prompt
    )
    return response.content
def generate_final_feedback(
    resume_score,
    ats_score,
    technical_score,
    hr_score,
    weak_areas
):
    """
    Generate final personalized
    career feedback.
    """
    prompt = f"""
    You are an AI career coach.
    Resume Score:
    {resume_score}
    ATS Score:
    {ats_score}
    Technical Interview Score:
    {technical_score}
    HR Interview Score:
    {hr_score}
    Weak Areas:
    {weak_areas}
    Generate personalized final feedback.
    Include:
    1. Overall Performance
    2. Main Strengths
    3. Main Weaknesses
    4. Top 3-5 Improvement Priorities
    5. Final Career Advice
    Give professional,
    personalized and actionable feedback.
    """
    response = llm.invoke(
        prompt
    )
    return response.content