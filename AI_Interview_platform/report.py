from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
def create_final_report(
    candidate_name,
    target_role,
    resume_score,
    ats_score,
    technical_score,
    hr_score,
    overall_score,
    grade,
    strengths,
    weak_areas,
    missing_skills,
    roadmap,
    output_path
):
    """
    Generate complete AI Interview
    Preparation Report.
    Includes:
    Resume Score
    ATS Score
    Technical Score
    HR Score
    Overall Score
    Grade
    Strengths
    Weak Areas
    Missing Skills
    Learning Roadmap
    """
    pdf = SimpleDocTemplate(
        output_path,
        pagesize=A4
    )
    styles = getSampleStyleSheet()
    title_style = styles[
        "Title"
    ]
    heading_style = styles[
        "Heading2"
    ]
    normal_style = styles[
        "BodyText"
    ]
    content = []
    content.append(
        Paragraph(
            "AI Interview Preparation Report",
            title_style
        )
    )
    content.append(
        Spacer(
            1,
            20
        )
    )
    content.append(
        Paragraph(
            "Candidate Information",
            heading_style
        )
    )
    content.append(
        Paragraph(
            f"Candidate Name: {candidate_name}",
            normal_style
        )
    )
    content.append(
        Paragraph(
            f"Target Role: {target_role}",
            normal_style
        )
    )
    content.append(
        Spacer(
            1,
            15
        )
    )
    content.append(
        Paragraph(
            "Performance Summary",
            heading_style
        )
    )
    score_data = [
        [
            "Category",
            "Score"
        ],
        [
            "Resume Score",
            f"{resume_score}%"
        ],
        [
            "ATS Score",
            f"{ats_score}%"
        ],
        [
            "Technical Interview",
            f"{technical_score}%"
        ],
        [
            "HR Interview",
            f"{hr_score}%"
        ],
        [
            "Overall Score",
            f"{overall_score}%"
        ],
        [
            "Grade",
            grade
        ]
    ]
    score_table = Table(
        score_data
    )
    score_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.grey
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )

            ]
        )
    )
    content.append(
        score_table
    )
    content.append(
        Spacer(
            1,
            20
        )
    )
    content.append(
        Paragraph(
            "Candidate Strengths",
            heading_style
        )
    )
    if strengths:
        for strength in strengths:
            content.append(
                Paragraph(
                    f"• {strength}",
                    normal_style
                )
            )
    else:
        content.append(
            Paragraph(
                "No strengths identified.",
                normal_style
            )
        )
    content.append(
        Spacer(
            1,
            15
        )
    )
    content.append(
        Paragraph(
            "Areas Needing Improvement",
            heading_style
        )
    )
    if weak_areas:
        for weak_area in weak_areas:
            content.append(
                Paragraph(
                    f"• {weak_area}",
                    normal_style
                )
            )
    else:
        content.append(
            Paragraph(
                "No major weak areas identified.",
                normal_style
            )
        )
    content.append(
        Spacer(
            1,
            15
        )
    )
    content.append(
        Paragraph(
            "Missing Skills",
            heading_style
        )
    )
    if missing_skills:
        for skill in missing_skills:
            content.append(
                Paragraph(
                    f"• {skill}",
                    normal_style
                )
            )
    else:
        content.append(
            Paragraph(
                "No major missing skills identified.",
                normal_style
            )
        )
    content.append(
        Spacer(
            1,
            15
        )
    )
    content.append(
        Paragraph(
            "Personalized Learning Roadmap",
            heading_style
        )
    )
    roadmap_lines = roadmap.split(
        "\n"
    )
    for line in roadmap_lines:
        if line.strip():
            content.append(
                Paragraph(
                    line,
                    normal_style
                )
            )
            content.append(
                Spacer(
                    1,
                    5
                )
            )
    content.append(
        Spacer(
            1,
            15
        )
    )
    content.append(
        Paragraph(
            "Final Recommendation",
            heading_style
        )
    )
    if overall_score >= 80:
        recommendation = (
            "The candidate demonstrates strong "
            "readiness for the target role. "
            "Focus on improving the identified "
            "weak areas and maintaining interview "
            "practice."
        )
    elif overall_score >= 60:
        recommendation = (
            "The candidate has moderate readiness "
            "for the target role. Focus on the "
            "missing skills and weak interview "
            "areas before applying."
        )
    else:
        recommendation = (
            "The candidate should focus on building "
            "core technical and communication skills "
            "before attempting advanced interviews."
        )
    content.append(
        Paragraph(
            recommendation,
            normal_style
        )
    )
    pdf.build(
        content
    )
    return output_path