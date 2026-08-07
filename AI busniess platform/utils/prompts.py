SYSTEM_PROMPT = """
You are an intelligent AI Business Assistant.

Always provide:
- Accurate answers
- Professional language
- Well formatted markdown
- Clear explanations
- Concise responses
"""

CHAT_PROMPT = """
Answer the user's question professionally.

Question:
{question}
"""

PDF_CHAT_PROMPT = """
Answer using only the provided document context.

Context:
{context}

Question:
{question}

If the answer is unavailable, say:
'I could not find this information in the uploaded document.'
"""

RESUME_PROMPT = """
Analyze the resume and provide:

1. Professional Summary
2. Skills
3. Technical Skills
4. Soft Skills
5. Education
6. Experience
7. Strengths
8. Weaknesses
9. Missing Skills
10. ATS Score (0-100)
11. Improvement Suggestions
"""

EMAIL_PROMPT = """
Write a professional email.

Purpose:
{purpose}

Details:
{details}
"""

REPLY_PROMPT = """
Generate a professional reply.

Email:
{email}
"""

GRAMMAR_PROMPT = """
Correct grammar without changing the meaning.

Text:
{text}
"""

MEETING_PROMPT = """
Analyze the meeting transcript.

Return:

1. Summary
2. Meeting Notes
3. Action Items
4. Key Decisions
"""

BLOG_PROMPT = """
Write a professional blog.

Topic:
{topic}
"""

SOCIAL_PROMPT = """
Generate a social media post.

Topic:
{topic}

Platform:
{platform}
"""

MARKETING_PROMPT = """
Write persuasive marketing copy.

Product:
{product}
"""

CODE_EXPLAIN_PROMPT = """
Explain the following code in simple language.

Code:
{code}
"""

BUG_PROMPT = """
Find bugs and suggest fixes.

Code:
{code}
"""

CODE_GENERATION_PROMPT = """
Generate Python code.

Requirement:
{requirement}
"""

COVER_LETTER_PROMPT = """
Write a professional cover letter.

Resume:
{resume}

Job Description:
{job}
"""