from rag import (
    generate_technical_question,
    generate_hr_question,
    evaluate_answer,
    generate_follow_up,
    choose_next_difficulty
)
from scoring import (
    calculate_technical_score,
    calculate_hr_score
)
def get_technical_question(
    resume_vectorstore,
    role,
    difficulty="Easy",
    category="Problem Solving"
):
    """
    Generate one resume-aware technical question.
    Categories:
    - Data Structures
    - Algorithms
    - System Design
    - Technology
    - Problem Solving
    """
    question = generate_technical_question(
        resume_vectorstore,
        role,
        difficulty,
        category
    )
    return question
def get_hr_question(
    resume_vectorstore,
    role,
    category="Communication"
):
    """
    Generate one resume-aware HR question.
    Categories:
    - Motivation
    - Teamwork
    - Conflict Resolution
    - Leadership
    - Communication
    - Career Goals
    """
    question = generate_hr_question(
        resume_vectorstore,
        role,
        category
    )
    return question
def evaluate_technical_answer(
    question,
    answer
):
    """
    Evaluate candidate's technical answer.

    AI evaluates:
    - Correctness
    - Relevance
    - Clarity
    - Technical Depth
    - Communication
    - Confidence
    """
    feedback = evaluate_answer(
        question,
        answer,
        "Technical"
    )
    return feedback
def evaluate_hr_answer(
    question,
    answer
):
    """
    Evaluate candidate's HR answer.
    AI evaluates:
    - Relevance
    - Clarity
    - Communication
    - Confidence
    - STAR structure
    """
    feedback = evaluate_answer(
        question,
        answer,
        "HR"
    )
    return feedback
def get_follow_up_question(
    question,
    answer
):
    """
    Generate follow-up question
    if candidate answer is:
    - Incomplete
    - Unclear
    - Incorrect
    Otherwise:
    NO_FOLLOW_UP
    """
    follow_up = generate_follow_up(
        question,
        answer
    )
    return follow_up
def get_next_difficulty(
    score
):
    """
    Change difficulty according
    to candidate's performance.
    Score 8-10:
        Hard
    Score 5-7:
        Medium
    Score 0-4:
        Easy
    """
    difficulty = choose_next_difficulty(
        score
    )
    return difficulty
def run_technical_interview(
    resume_vectorstore,
    role,
    categories,
    number_of_questions
):
    """
    Generate technical interview questions.
    Initial difficulty:
        Easy
    The actual answer evaluation and
    adaptive difficulty update are handled
    by process_technical_answer().
    """
    questions = []
    difficulty = "Easy"
    for i in range(
        number_of_questions
    ):
        category = categories[
            i % len(categories)
        ]
        question = get_technical_question(
            resume_vectorstore,
            role,
            difficulty,
            category
        )
        questions.append(
            {
                "question": question,
                "category": category,
                "difficulty": difficulty,
                "question_number": i + 1
            }
        )
    return questions
def run_hr_interview(
    resume_vectorstore,
    role,
    categories,
    number_of_questions
):
    """
    Generate HR interview questions.
    HR questions are based on:
    - Resume
    - Target Role
    - HR Category
    """
    questions = []
    for i in range(
        number_of_questions
    ):
        category = categories[
            i % len(categories)
        ]
        question = get_hr_question(
            resume_vectorstore,
            role,
            category
        )
        questions.append(
            {
                "question": question,
                "category": category,
                "type": "HR",
                "question_number": i + 1
            }
        )
    return questions
def process_technical_answer(
    question,
    answer
):
    """
    Complete technical answer process.
    Flow:
    Question
       ↓
    Candidate Answer
       ↓
    AI Evaluation
       ↓
    Score
       ↓
    Next Difficulty
       ↓
    Follow-up Question
    """
    feedback = evaluate_technical_answer(
        question,
        answer
    )
    follow_up = get_follow_up_question(
        question,
        answer
    )
    return {
        "question":
            question,
        "answer":
            answer,
        "feedback":
            feedback,
        "follow_up":
            follow_up
    }
def process_hr_answer(
    question,
    answer
):
    """
    Complete HR answer process.
    Flow:
    Question
       ↓
    Candidate Answer
       ↓
    STAR Evaluation
       ↓
    Feedback
       ↓
    Follow-up
    """
    feedback = evaluate_hr_answer(
        question,
        answer
    )
    follow_up = get_follow_up_question(
        question,
        answer
    )
    return {
        "question":
            question,
        "answer":
            answer,
        "feedback":
            feedback,
        "follow_up":
            follow_up
    }
def process_technical_answer_adaptive(
    question,
    answer,
    current_difficulty
):
    """
    Evaluate answer and decide
    next interview difficulty.
    Flow:
    Answer
       ↓
    AI Evaluation
       ↓
    Score
       ↓
    Next Difficulty
    """
    feedback = evaluate_technical_answer(
        question,
        answer
    )
    follow_up = get_follow_up_question(
        question,
        answer
    )
    return {
        "question":
            question,
        "answer":
            answer,
        "feedback":
            feedback,
        "follow_up":
            follow_up,
        "current_difficulty":
            current_difficulty
    }
def get_technical_result(
    question_scores
):
    """
    Calculate final technical
    interview percentage.
    Example:
    Scores:
    [8, 7, 9, 6]
    Result:
    75%
    """
    score = calculate_technical_score(
        question_scores
    )
    return {
        "technical_score":
            score,
        "total_questions":
            len(
                question_scores
            ),
        "question_scores":
            question_scores
    }
def get_hr_result(
    question_scores
):
    """
    Calculate final HR
    interview percentage.
    """
    score = calculate_hr_score(
        question_scores
    )
    return {
        "hr_score":
            score,
        "total_questions":
            len(
                question_scores
            ),
        "question_scores":
            question_scores
    }
def run_full_mock_interview(
    resume_vectorstore,
    role
):
    """
    Full Mock Interview.
    Technical:
    - Data Structures
    - Algorithms
    - Technology
    - Problem Solving
    HR:
    - Motivation
    - Teamwork
    - Communication
    - Leadership
    """
    technical_categories = [
        "Data Structures",
        "Algorithms",
        "Technology",
        "Problem Solving"
    ]
    hr_categories = [
        "Motivation",
        "Teamwork",
        "Communication",
        "Leadership"
    ]
    technical_questions = run_technical_interview(
        resume_vectorstore,
        role,
        technical_categories,
        4
    )
    hr_questions = run_hr_interview(
        resume_vectorstore,
        role,
        hr_categories,
        4
    )
    return {
        "technical_questions":
            technical_questions,
        "hr_questions":
            hr_questions
    }