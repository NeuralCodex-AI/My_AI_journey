from rag import generate_learning_roadmap
def create_learning_roadmap(
    weak_areas,
    role,
    hours_per_week
):
    """
    Generate a personalized learning roadmap.
    weak_areas:
        Skills or topics where candidate is weak.
    role:
        Candidate's target job role.
    hours_per_week:
        How many hours candidate can study per week.
    """
    roadmap = generate_learning_roadmap(
        weak_areas,
        role,
        hours_per_week
    )
    return roadmap
def create_roadmap_from_scores(
    skill_scores,
    role,
    hours_per_week
):
    """
    Automatically find weak skills
    from skill scores and create roadmap.
    Example:
    skill_scores = {
        "Python": 90,
        "SQL": 45,
        "DSA": 50,
        "Communication": 80
    }
    Weak Areas:
    SQL
    DSA
    """
    weak_areas = []
    for skill, score in skill_scores.items():
        if score < 60:
            weak_areas.append(
                skill
            )
    roadmap = create_learning_roadmap(
        weak_areas,
        role,
        hours_per_week
    )
    return {
        "weak_areas":
            weak_areas,
        "roadmap":
            roadmap
    }
def create_roadmap_from_missing_skills(
    missing_skills,
    role,
    hours_per_week
):
    """
    Create roadmap using skills
    missing from Resume vs Job Description.
    Example:
    Resume Skills:
    Python
    SQL
    Job Requirements:
    Python
    SQL
    Docker
    AWS
    Missing Skills:
    Docker
    AWS
    """
    roadmap = create_learning_roadmap(
        missing_skills,
        role,
        hours_per_week
    )
    return {
        "missing_skills":
            missing_skills,
        "roadmap":
            roadmap

    }
def create_career_development_plan(
    skill_scores,
    missing_skills,
    role,
    hours_per_week
):
    """
    Create complete personalized
    career development plan.
    Combines:
    1. Weak interview skills
    2. Missing job skills
    3. Target role
    4. Available study time
    """
    weak_areas = []
    for skill, score in skill_scores.items():
        if score < 60:
            weak_areas.append(
                skill
            )
    for skill in missing_skills:
        if skill not in weak_areas:
            weak_areas.append(
                skill
            )
    roadmap = create_learning_roadmap(
        weak_areas,
        role,
        hours_per_week
    )
    return {
        "target_role":
            role,
        "weak_areas":
            weak_areas,
        "missing_skills":
            missing_skills,
        "hours_per_week":
            hours_per_week,
        "roadmap":
            roadmap
    }