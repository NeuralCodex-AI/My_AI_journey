import sqlite3
DATABASE_NAME = "interview_platform.db"
def get_connection():
    connection = sqlite3.connect(
        DATABASE_NAME
    )
    connection.row_factory = sqlite3.Row
    return connection
def create_tables():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            target_role TEXT,
            experience_level TEXT,
            industry TEXT,
            FOREIGN KEY (user_id)
            REFERENCES users(id)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            file_name TEXT,
            resume_text TEXT,
            resume_score REAL DEFAULT 0,
            ats_score REAL DEFAULT 0,
            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
            REFERENCES users(id)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS job_descriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_title TEXT,
            jd_text TEXT,
            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
            REFERENCES users(id)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS interview_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resume_id INTEGER,
            jd_id INTEGER,
            role TEXT,
            mode TEXT,
            difficulty TEXT,
            resume_score REAL DEFAULT 0,
            ats_score REAL DEFAULT 0,
            technical_score REAL DEFAULT 0,
            hr_score REAL DEFAULT 0,
            overall_score REAL DEFAULT 0,
            grade TEXT,
            started_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id)
            REFERENCES users(id),
            FOREIGN KEY (resume_id)
            REFERENCES resumes(id),
            FOREIGN KEY (jd_id)
            REFERENCES job_descriptions(id)

        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS interview_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            category TEXT,
            interview_type TEXT,
            difficulty TEXT,
            question_number INTEGER,
            FOREIGN KEY (session_id)
            REFERENCES interview_sessions(id)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS interview_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            answer TEXT,
            score REAL DEFAULT 0,
            feedback TEXT,
            strengths TEXT,
            weaknesses TEXT,
            follow_up_question TEXT,
            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id)
            REFERENCES interview_questions(id)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS skill_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id INTEGER,
            skill_name TEXT NOT NULL,
            score REAL DEFAULT 0,
            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
            REFERENCES users(id),
            FOREIGN KEY (session_id)
            REFERENCES interview_sessions(id)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weak_areas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id INTEGER,
            skill_name TEXT NOT NULL,
            score REAL DEFAULT 0,
            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
            REFERENCES users(id),
            FOREIGN KEY (session_id)
            REFERENCES interview_sessions(id)

        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id INTEGER NOT NULL,
            file_path TEXT,
            share_token TEXT UNIQUE,
            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
            REFERENCES users(id),
            FOREIGN KEY (session_id)
            REFERENCES interview_sessions(id)
        )
        """
    )
    connection.commit()
    connection.close()
def create_user(
    name,
    email,
    password
):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password
            )
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                password
            )
        )
        connection.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        connection.close()
def get_user_by_email(
    email
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (
            email,
        )
    )
    user = cursor.fetchone()
    connection.close()
    return user
def get_user_by_id(
    user_id
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (
            user_id,
        )
    )
    user = cursor.fetchone()
    connection.close()
    return user
def save_profile(
    user_id,
    target_role,
    experience_level,
    industry
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO profiles
        (
            user_id,
            target_role,
            experience_level,
            industry
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            target_role,
            experience_level,
            industry
        )
    )
    connection.commit()
    connection.close()
def save_resume(
    user_id,
    file_name,
    resume_text,
    resume_score=0,
    ats_score=0
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO resumes
        (
            user_id,
            file_name,
            resume_text,
            resume_score,
            ats_score
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            file_name,
            resume_text,
            resume_score,
            ats_score
        )
    )
    connection.commit()
    resume_id = cursor.lastrowid
    connection.close()
    return resume_id
def save_job_description(
    user_id,
    job_title,
    jd_text
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO job_descriptions
        (
            user_id,
            job_title,
            jd_text
        )
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            job_title,
            jd_text
        )
    )
    connection.commit()
    jd_id = cursor.lastrowid
    connection.close()
    return jd_id
def create_interview_session(
    user_id,
    resume_id,
    jd_id,
    role,
    mode,
    difficulty
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO interview_sessions
        (
            user_id,
            resume_id,
            jd_id,
            role,
            mode,
            difficulty
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            resume_id,
            jd_id,
            role,
            mode,
            difficulty
        )
    )
    connection.commit()
    session_id = cursor.lastrowid
    connection.close()
    return session_id
def save_question(
    session_id,
    question,
    category,
    interview_type,
    difficulty,
    question_number
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO interview_questions
        (
            session_id,
            question,
            category,
            interview_type,
            difficulty,
            question_number
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            question,
            category,
            interview_type,
            difficulty,
            question_number
        )
    )
    connection.commit()
    question_id = cursor.lastrowid
    connection.close()
    return question_id
def save_answer(
    question_id,
    answer,
    score,
    feedback,
    strengths,
    weaknesses,
    follow_up_question
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO interview_answers
        (
            question_id,
            answer,
            score,
            feedback,
            strengths,
            weaknesses,
            follow_up_question
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            question_id,
            answer,
            score,
            feedback,
            strengths,
            weaknesses,
            follow_up_question
        )
    )
    connection.commit()
    answer_id = cursor.lastrowid
    connection.close()
    return answer_id
def update_interview_result(
    session_id,
    resume_score,
    ats_score,
    technical_score,
    hr_score,
    overall_score,
    grade
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE interview_sessions
        SET
            resume_score = ?,
            ats_score = ?,
            technical_score = ?,
            hr_score = ?,
            overall_score = ?,
            grade = ?,
            completed_at =
            CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            resume_score,
            ats_score,
            technical_score,
            hr_score,
            overall_score,
            grade,
            session_id
        )
    )
    connection.commit()
    connection.close()
def save_skill_progress(
    user_id,
    session_id,
    skill_name,
    score
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO skill_progress
        (
            user_id,
            session_id,
            skill_name,
            score
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            session_id,
            skill_name,
            score
        )
    )
    connection.commit()
    connection.close()
def save_weak_area(
    user_id,
    session_id,
    skill_name,
    score
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO weak_areas
        (
            user_id,
            session_id,
            skill_name,
            score
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            session_id,
            skill_name,
            score
        )
    )
    connection.commit()
    connection.close()
def save_report(
    user_id,
    session_id,
    file_path,
    share_token
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO reports
        (
            user_id,
            session_id,
            file_path,
            share_token
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            session_id,
            file_path,
            share_token
        )
    )
    connection.commit()
    report_id = cursor.lastrowid
    connection.close()
    return report_id
def get_interview_history(
    user_id
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT *
        FROM interview_sessions
        WHERE user_id = ?
        ORDER BY started_at DESC
        """,
        (
            user_id,
        )
    )
    sessions = cursor.fetchall()
    connection.close()
    return sessions
def get_session_details(
    session_id
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT *
        FROM interview_sessions
        WHERE id = ?
        """,
        (
            session_id,
        )
    )
    session = cursor.fetchone()
    connection.close()
    return session
def get_session_replay(
    session_id
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            q.question,
            q.category,
            q.interview_type,
            q.difficulty,
            a.answer,
            a.score,
            a.feedback,
            a.strengths,
            a.weaknesses,
            a.follow_up_question
        FROM interview_questions q
        LEFT JOIN interview_answers a
        ON q.id = a.question_id
        WHERE q.session_id = ?
        ORDER BY q.question_number
        """,
        (
            session_id,
        )
    )
    replay = cursor.fetchall()
    connection.close()
    return replay
def get_score_history(
    user_id
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            id,
            role,
            mode,
            overall_score,
            technical_score,
            hr_score,
            started_at
        FROM interview_sessions
        WHERE user_id = ?
        AND completed_at IS NOT NULL
        ORDER BY started_at ASC
        """,
        (
            user_id,
        )
    )
    scores = cursor.fetchall()
    connection.close()
    return scores
def get_skill_progress(
    user_id,
    skill_name
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            skill_name,
            score,
            created_at
        FROM skill_progress
        WHERE user_id = ?
        AND skill_name = ?
        ORDER BY created_at ASC
        """,
        (
            user_id,
            skill_name
        )
    )
    progress = cursor.fetchall()
    connection.close()
    return progress
def get_common_weak_areas(
    user_id
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            skill_name,
            COUNT(*) AS occurrence,
            AVG(score) AS average_score
        FROM weak_areas
        WHERE user_id = ?
        GROUP BY skill_name
        ORDER BY occurrence DESC
        """,
        (
            user_id,
        )
    )
    weak_areas = cursor.fetchall()
    connection.close()
    return weak_areas
def get_attempt_count(
    user_id
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT COUNT(*) AS total_attempts
        FROM interview_sessions
        WHERE user_id = ?
        AND completed_at IS NOT NULL
        """,
        (
            user_id,
        )
    )
    result = cursor.fetchone()
    connection.close()
    return result["total_attempts"]
def compare_sessions(
    session_id_1,
    session_id_2
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            id,
            role,
            mode,
            resume_score,
            ats_score,
            technical_score,
            hr_score,
            overall_score,
            grade,
            started_at
        FROM interview_sessions
        WHERE id IN (?, ?)
        ORDER BY id
        """,
        (
            session_id_1,
            session_id_2
        )
    )
    sessions = cursor.fetchall()
    connection.close()
    return sessions