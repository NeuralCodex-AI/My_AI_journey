def calculate_ats_score(
    skill_match,
    experience_match,
    education_match,
    keyword_match,
    structure_score,
    formatting_score
):
    """
    Calculate ATS score using weighted criteria.
    Weights:
    Skill Match       = 40%
    Experience Match  = 20%
    Education Match   = 10%
    Keyword Match     = 15%
    Structure         = 10%
    Formatting        = 5%
    """
    ats_score = (
        skill_match * 0.40
        + experience_match * 0.20
        + education_match * 0.10
        + keyword_match * 0.15
        + structure_score * 0.10
        + formatting_score * 0.05
    )
    return round(
        ats_score,
        2
    )
def calculate_resume_score(
    skills,
    experience,
    education,
    projects,
    certifications
):
    """
    Calculate overall resume strength score.
    Weights:
    Skills          = 30%
    Experience      = 25%
    Education       = 15%
    Projects        = 20%
    Certifications  = 10%
    """
    resume_score = (
        skills * 0.30
        + experience * 0.25
        + education * 0.15
        + projects * 0.20
        + certifications * 0.10
    )
    return round(
        resume_score,
        2
    )
def calculate_technical_score(
    question_scores
):
    """
    Calculate average technical interview score.
    Example:
    [8, 7, 9, 6]
    Average = 7.5 / 10
    Convert to percentage:
    75%
    """
    if len(question_scores) == 0:
        return 0
    total = sum(
        question_scores
    )
    average = (
        total / len(question_scores)
    )
    percentage = (
        average / 10
    ) * 100
    return round(
        percentage,
        2
    )
def calculate_hr_score(
    question_scores
):
    """
    Calculate average HR interview score.
    Scores are assumed to be
    between 0 and 10.
    """
    if len(question_scores) == 0:
        return 0
    total = sum(
        question_scores
    )
    average = (
        total / len(question_scores)
    )
    percentage = (
        average / 10
    ) * 100
    return round(
        percentage,
        2
    )
def calculate_overall_score(
    resume_score,
    technical_score,
    hr_score
):
    """
    Calculate final platform score.
    Weights:
    Resume      = 20%
    Technical   = 50%
    HR          = 30%
    """
    overall_score = (
        resume_score * 0.20
        + technical_score * 0.50
        + hr_score * 0.30
    )
    return round(
        overall_score,
        2
    )
def get_grade(
    score
):
    """
    Convert percentage score
    into A-F grade.
    """
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
def generate_final_score(
    resume_score,
    technical_scores,
    hr_scores
):
    """
    Generate complete final performance score.
    Returns:
    Resume Score
    Technical Score
    HR Score
    Overall Score
    Grade
    """
    # Calculate Technical Score
    technical_score = calculate_technical_score(
        technical_scores
    )
    # Calculate HR Score
    hr_score = calculate_hr_score(
        hr_scores
    )
    # Calculate Overall Score
    overall_score = calculate_overall_score(
        resume_score,
        technical_score,
        hr_score
    )
    # Calculate Grade
    grade = get_grade(
        overall_score
    )
    return {
        "resume_score": resume_score,
        "technical_score": technical_score,
        "hr_score": hr_score,
        "overall_score": overall_score,
        "grade": grade
    }
def find_strengths(
    scores
):
    """
    Find areas where candidate performed well.
    Example:
    {
        "Python": 90,
        "DSA": 75,
        "Communication": 85
    }
    """
    strengths = []
    for skill, score in scores.items():
        if score >= 80:
            strengths.append(
                skill
            )
    return strengths
def find_weak_areas(
    scores
):
    """
    Find areas where candidate needs improvement.
    """
    weak_areas = []
    for skill, score in scores.items():
        if score < 60:
            weak_areas.append(
                skill
            )
    return weak_areas

def get_improvement_priorities(
    scores
):
    """
    Return top 5 weakest areas.
    """
    sorted_scores = sorted(
        scores.items(),
        key=lambda item: item[1]
    )
    priorities = []
    for skill, score in sorted_scores[:5]:
        priorities.append(
            {
                "skill": skill,
                "score": score
            }
        )
    return priorities