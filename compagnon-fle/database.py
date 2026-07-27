from __future__ import annotations

import hashlib
import hmac
import os
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = Path(
    os.environ.get("DATABASE_PATH", str(DATA_DIR / "compagnon_fle.sqlite3"))
).expanduser()
LEVELS = ("A0", "A1", "A2", "B1", "B2")
PASSWORD_ITERATIONS = 310_000


def connect() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 10000")
    return connection


def initialize_database() -> None:
    with connect() as database:
        database.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('learner', 'admin')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS learner_profiles (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                class_name TEXT NOT NULL,
                registration_status TEXT NOT NULL DEFAULT 'pending_level'
                    CHECK (registration_status IN ('pending_level', 'level_assigned')),
                activity_access_enabled INTEGER NOT NULL DEFAULT 0
                    CHECK (activity_access_enabled IN (0, 1)),
                assigned_level TEXT NULL
                    CHECK (assigned_level IS NULL OR assigned_level IN ('A0', 'A1', 'A2', 'B1', 'B2')),
                level_assigned_at TEXT NULL,
                level_assigned_by INTEGER NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (level_assigned_by) REFERENCES users(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS level_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                learner_id INTEGER NOT NULL,
                level TEXT NOT NULL CHECK (level IN ('A0', 'A1', 'A2', 'B1', 'B2')),
                assigned_by INTEGER NOT NULL,
                assigned_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (learner_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS exercise_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                learner_id INTEGER NOT NULL,
                sequence_slug TEXT NOT NULL,
                exercise_id TEXT NOT NULL,
                level TEXT NOT NULL CHECK (level IN ('A0', 'A1', 'A2', 'B1', 'B2')),
                answer_text TEXT NOT NULL,
                is_correct INTEGER NOT NULL CHECK (is_correct IN (0, 1)),
                score REAL NULL,
                attempted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (learner_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS adaptation_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                learner_id INTEGER NOT NULL,
                sequence_slug TEXT NOT NULL,
                official_level TEXT NOT NULL
                    CHECK (official_level IN ('A0', 'A1', 'A2', 'B1', 'B2')),
                success_count INTEGER NOT NULL,
                exercise_count INTEGER NOT NULL,
                difficulty TEXT NOT NULL
                    CHECK (difficulty IN ('accessible', 'equivalent', 'demanding')),
                recommended_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (learner_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS exercise_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                learner_id INTEGER NOT NULL,
                sequence_slug TEXT NOT NULL,
                level TEXT NOT NULL CHECK (level IN ('A0', 'A1', 'A2', 'B1', 'B2')),
                current_index INTEGER NOT NULL DEFAULT 0,
                total_questions INTEGER NOT NULL,
                success_count INTEGER NOT NULL DEFAULT 0,
                evaluated_count INTEGER NOT NULL DEFAULT 0,
                manual_review_count INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'in_progress'
                    CHECK (status IN ('in_progress', 'completed')),
                score_percentage INTEGER NULL,
                recommendation_code TEXT NULL,
                started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT NULL,
                FOREIGN KEY (learner_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
            CREATE INDEX IF NOT EXISTS idx_profiles_class ON learner_profiles(class_name);
            CREATE INDEX IF NOT EXISTS idx_assignments_learner ON level_assignments(learner_id);
            CREATE INDEX IF NOT EXISTS idx_attempts_learner ON exercise_attempts(learner_id);
            CREATE INDEX IF NOT EXISTS idx_attempts_exercise ON exercise_attempts(sequence_slug, exercise_id);
            CREATE INDEX IF NOT EXISTS idx_adaptations_learner ON adaptation_recommendations(learner_id);
            CREATE INDEX IF NOT EXISTS idx_runs_learner ON exercise_runs(learner_id, sequence_slug, status);
            """
        )
        profile_columns = {
            row["name"] for row in database.execute("PRAGMA table_info(learner_profiles)")
        }
        if "registration_status" not in profile_columns:
            database.execute(
                """
                ALTER TABLE learner_profiles
                ADD COLUMN registration_status TEXT NOT NULL DEFAULT 'pending_level'
                    CHECK (registration_status IN ('pending_level', 'level_assigned'))
                """
            )
        if "activity_access_enabled" not in profile_columns:
            database.execute(
                """
                ALTER TABLE learner_profiles
                ADD COLUMN activity_access_enabled INTEGER NOT NULL DEFAULT 0
                    CHECK (activity_access_enabled IN (0, 1))
                """
            )
        attempt_columns = {
            row["name"] for row in database.execute("PRAGMA table_info(exercise_attempts)")
        }
        if "run_id" not in attempt_columns:
            database.execute("ALTER TABLE exercise_attempts ADD COLUMN run_id INTEGER NULL")
        if "requires_manual_review" not in attempt_columns:
            database.execute(
                "ALTER TABLE exercise_attempts ADD COLUMN requires_manual_review INTEGER NOT NULL DEFAULT 0"
            )
        database.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_attempts_run_exercise "
            "ON exercise_attempts(run_id, exercise_id) WHERE run_id IS NOT NULL"
        )
        database.execute(
            """
            UPDATE learner_profiles
            SET registration_status = 'level_assigned',
                activity_access_enabled = 1
            WHERE assigned_level IS NOT NULL
              AND (registration_status != 'level_assigned' OR activity_access_enabled != 1)
            """
        )


def normalize_login(login: str) -> str:
    return login.strip().lower()


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS
    )
    return f"pbkdf2_sha256${PASSWORD_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations, salt_hex, digest_hex = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        candidate = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations),
        )
        return hmac.compare_digest(candidate.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


def create_learner(
    *, first_name: str, birth_date: str, class_name: str, login: str, password: str
) -> int:
    with connect() as database:
        cursor = database.execute(
            "INSERT INTO users (login, password_hash, role) VALUES (?, ?, 'learner')",
            (normalize_login(login), hash_password(password)),
        )
        user_id = int(cursor.lastrowid)
        database.execute(
            """
            INSERT INTO learner_profiles
                (user_id, first_name, birth_date, class_name, registration_status,
                 activity_access_enabled, assigned_level)
            VALUES (?, ?, ?, ?, 'pending_level', 0, NULL)
            """,
            (user_id, first_name.strip(), birth_date, class_name.strip()),
        )
        return user_id


def create_admin(login: str, password: str) -> int:
    with connect() as database:
        cursor = database.execute(
            "INSERT INTO users (login, password_hash, role) VALUES (?, ?, 'admin')",
            (normalize_login(login), hash_password(password)),
        )
        return int(cursor.lastrowid)


def authenticate_admin(login: str, password: str):
    with connect() as database:
        user = database.execute(
            "SELECT id, login, password_hash, role FROM users WHERE login = ?",
            (normalize_login(login),),
        ).fetchone()
    if not user or user["role"] != "admin":
        return None
    return user if verify_password(password, user["password_hash"]) else None


def authenticate_learner(login: str, password: str):
    with connect() as database:
        user = database.execute(
            """
            SELECT
                users.id,
                users.login,
                users.password_hash,
                users.role,
                learner_profiles.first_name,
                learner_profiles.registration_status,
                learner_profiles.activity_access_enabled,
                learner_profiles.assigned_level
            FROM users
            JOIN learner_profiles ON learner_profiles.user_id = users.id
            WHERE users.login = ? AND users.role = 'learner'
            """,
            (normalize_login(login),),
        ).fetchone()
    if not user:
        return None
    return user if verify_password(password, user["password_hash"]) else None


def list_learners():
    with connect() as database:
        return database.execute(
            """
            SELECT
                users.id,
                users.login,
                users.created_at,
                learner_profiles.first_name,
                learner_profiles.birth_date,
                learner_profiles.class_name,
                learner_profiles.registration_status,
                learner_profiles.activity_access_enabled,
                learner_profiles.assigned_level,
                learner_profiles.level_assigned_at
            FROM users
            JOIN learner_profiles ON learner_profiles.user_id = users.id
            WHERE users.role = 'learner'
            ORDER BY users.created_at DESC, users.id DESC
            """
        ).fetchall()


def get_learner(learner_id: int):
    with connect() as database:
        return database.execute(
            """
            SELECT
                users.id,
                users.login,
                users.created_at,
                learner_profiles.first_name,
                learner_profiles.birth_date,
                learner_profiles.class_name,
                learner_profiles.registration_status,
                learner_profiles.activity_access_enabled,
                learner_profiles.assigned_level,
                learner_profiles.level_assigned_at
            FROM users
            JOIN learner_profiles ON learner_profiles.user_id = users.id
            WHERE users.id = ? AND users.role = 'learner'
            """,
            (learner_id,),
        ).fetchone()


def learner_can_access_level(learner_id: int, level: str) -> bool:
    if level not in LEVELS:
        return False
    with connect() as database:
        access = database.execute(
            """
            SELECT 1
            FROM learner_profiles
            WHERE user_id = ?
              AND registration_status = 'level_assigned'
              AND activity_access_enabled = 1
              AND assigned_level = ?
            """,
            (learner_id, level),
        ).fetchone()
    return access is not None


def record_exercise_attempt(
    *,
    learner_id: int,
    sequence_slug: str,
    exercise_id: str,
    level: str,
    answer_text: str,
    is_correct: bool | None,
    score: float | None,
    run_id: int | None = None,
    requires_manual_review: bool = False,
) -> int:
    if level not in LEVELS:
        raise ValueError("Niveau invalide")
    with connect() as database:
        cursor = database.execute(
            """
            INSERT INTO exercise_attempts
                (learner_id, sequence_slug, exercise_id, level, answer_text, is_correct,
                 score, run_id, requires_manual_review)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                learner_id,
                sequence_slug,
                exercise_id,
                level,
                answer_text,
                int(is_correct is True),
                score,
                run_id,
                int(requires_manual_review),
            ),
        )
        return int(cursor.lastrowid)


def list_exercise_attempts(learner_id: int):
    with connect() as database:
        return database.execute(
            """
            SELECT id, learner_id, sequence_slug, exercise_id, level,
                   answer_text, is_correct, score, requires_manual_review, attempted_at
            FROM exercise_attempts
            WHERE learner_id = ?
            ORDER BY attempted_at DESC, id DESC
            """,
            (learner_id,),
        ).fetchall()


def record_adaptation_recommendation(
    *,
    learner_id: int,
    sequence_slug: str,
    official_level: str,
    success_count: int,
    exercise_count: int,
    difficulty: str,
) -> int:
    if official_level not in LEVELS:
        raise ValueError("Niveau officiel invalide")
    if difficulty not in ("accessible", "equivalent", "demanding"):
        raise ValueError("Difficulté invalide")
    with connect() as database:
        cursor = database.execute(
            """
            INSERT INTO adaptation_recommendations
                (learner_id, sequence_slug, official_level, success_count,
                 exercise_count, difficulty)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                learner_id,
                sequence_slug,
                official_level,
                success_count,
                exercise_count,
                difficulty,
            ),
        )
        return int(cursor.lastrowid)


def get_latest_adaptation(learner_id: int, sequence_slug: str):
    with connect() as database:
        return database.execute(
            """
            SELECT official_level, success_count, exercise_count,
                   difficulty, recommended_at
            FROM adaptation_recommendations
            WHERE learner_id = ? AND sequence_slug = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (learner_id, sequence_slug),
        ).fetchone()


def get_learner_progress(learner_id: int):
    with connect() as database:
        summary = database.execute(
            """
            SELECT
                COUNT(*) AS attempt_count,
                COUNT(DISTINCT sequence_slug) AS sequence_count,
                COUNT(DISTINCT sequence_slug || ':' || exercise_id) AS exercise_count,
                COALESCE(SUM(CASE WHEN requires_manual_review = 0 THEN is_correct ELSE 0 END), 0) AS success_count,
                COALESCE(SUM(CASE WHEN requires_manual_review = 0 THEN 1 ELSE 0 END), 0) AS evaluated_count,
                COALESCE(SUM(CASE WHEN requires_manual_review = 1 THEN 1 ELSE 0 END), 0) AS manual_review_count
            FROM exercise_attempts
            WHERE learner_id = ?
            """,
            (learner_id,),
        ).fetchone()
        sequences = database.execute(
            """
            SELECT sequence_slug, level, COUNT(*) AS attempt_count,
                   COALESCE(SUM(CASE WHEN requires_manual_review = 0 THEN is_correct ELSE 0 END), 0) AS success_count,
                   COALESCE(SUM(CASE WHEN requires_manual_review = 0 THEN 1 ELSE 0 END), 0) AS evaluated_count,
                   COALESCE(SUM(CASE WHEN requires_manual_review = 1 THEN 1 ELSE 0 END), 0) AS manual_review_count,
                   MAX(attempted_at) AS last_attempt_at
            FROM exercise_attempts
            WHERE learner_id = ?
            GROUP BY sequence_slug, level
            ORDER BY last_attempt_at DESC
            """,
            (learner_id,),
        ).fetchall()
        attempts = database.execute(
            """
            SELECT sequence_slug, exercise_id, level, answer_text,
                   is_correct, score, requires_manual_review, attempted_at
            FROM exercise_attempts
            WHERE learner_id = ?
            ORDER BY attempted_at DESC, id DESC
            """,
            (learner_id,),
        ).fetchall()
        difficulties = database.execute(
            """
            SELECT sequence_slug, exercise_id, level, answer_text, attempted_at
            FROM exercise_attempts
            WHERE learner_id = ? AND is_correct = 0 AND requires_manual_review = 0
            ORDER BY attempted_at DESC, id DESC
            LIMIT 5
            """,
            (learner_id,),
        ).fetchall()
        latest_adaptation = database.execute(
            """
            SELECT sequence_slug, official_level, success_count, exercise_count,
                   difficulty, recommended_at
            FROM adaptation_recommendations
            WHERE learner_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (learner_id,),
        ).fetchone()
        latest_run = database.execute(
            """
            SELECT id, sequence_slug, level, total_questions, success_count,
                   evaluated_count, manual_review_count, score_percentage,
                   recommendation_code, status, started_at, completed_at
            FROM exercise_runs
            WHERE learner_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (learner_id,),
        ).fetchone()
    return {
        "summary": summary,
        "sequences": sequences,
        "attempts": attempts,
        "difficulties": difficulties,
        "latest_adaptation": latest_adaptation,
        "latest_run": latest_run,
    }


def start_exercise_run(
    *, learner_id: int, sequence_slug: str, level: str, total_questions: int
) -> int:
    if level not in LEVELS:
        raise ValueError("Niveau invalide")
    with connect() as database:
        database.execute(
            """
            UPDATE exercise_runs
            SET status = 'completed', completed_at = CURRENT_TIMESTAMP
            WHERE learner_id = ? AND sequence_slug = ? AND status = 'in_progress'
            """,
            (learner_id, sequence_slug),
        )
        cursor = database.execute(
            """
            INSERT INTO exercise_runs
                (learner_id, sequence_slug, level, total_questions)
            VALUES (?, ?, ?, ?)
            """,
            (learner_id, sequence_slug, level, total_questions),
        )
        return int(cursor.lastrowid)


def get_exercise_run(run_id: int, learner_id: int):
    with connect() as database:
        return database.execute(
            """
            SELECT id, learner_id, sequence_slug, level, current_index,
                   total_questions, success_count, evaluated_count,
                   manual_review_count, status, score_percentage,
                   recommendation_code, started_at, completed_at
            FROM exercise_runs
            WHERE id = ? AND learner_id = ?
            """,
            (run_id, learner_id),
        ).fetchone()


def get_active_exercise_run(learner_id: int, sequence_slug: str, level: str):
    with connect() as database:
        return database.execute(
            """
            SELECT id, learner_id, sequence_slug, level, current_index,
                   total_questions, success_count, evaluated_count,
                   manual_review_count, status, score_percentage,
                   recommendation_code, started_at, completed_at
            FROM exercise_runs
            WHERE learner_id = ? AND sequence_slug = ? AND level = ?
              AND status = 'in_progress'
            ORDER BY id DESC
            LIMIT 1
            """,
            (learner_id, sequence_slug, level),
        ).fetchone()


def advance_exercise_run(
    *, run_id: int, learner_id: int, is_correct: bool | None,
    requires_manual_review: bool, score_percentage: int | None = None,
    recommendation_code: str | None = None,
) -> bool:
    with connect() as database:
        run = database.execute(
            """
            SELECT current_index, total_questions, status
            FROM exercise_runs WHERE id = ? AND learner_id = ?
            """,
            (run_id, learner_id),
        ).fetchone()
        if not run or run["status"] != "in_progress":
            return False
        next_index = run["current_index"] + 1
        completed = next_index >= run["total_questions"]
        database.execute(
            """
            UPDATE exercise_runs
            SET current_index = ?,
                success_count = success_count + ?,
                evaluated_count = evaluated_count + ?,
                manual_review_count = manual_review_count + ?,
                status = ?,
                score_percentage = CASE WHEN ? THEN ? ELSE score_percentage END,
                recommendation_code = CASE WHEN ? THEN ? ELSE recommendation_code END,
                completed_at = CASE WHEN ? THEN CURRENT_TIMESTAMP ELSE completed_at END
            WHERE id = ? AND learner_id = ?
            """,
            (
                next_index,
                int(is_correct is True),
                int(is_correct is not None),
                int(requires_manual_review),
                "completed" if completed else "in_progress",
                int(completed), score_percentage,
                int(completed), recommendation_code,
                int(completed), run_id, learner_id,
            ),
        )
        return True


def get_run_attempts(run_id: int, learner_id: int):
    with connect() as database:
        return database.execute(
            """
            SELECT exercise_id, answer_text, is_correct, score,
                   requires_manual_review, attempted_at
            FROM exercise_attempts
            WHERE run_id = ? AND learner_id = ?
            ORDER BY id
            """,
            (run_id, learner_id),
        ).fetchall()


def assign_level(*, learner_id: int, level: str, admin_id: int) -> bool:
    if level not in LEVELS:
        return False
    with connect() as database:
        learner = database.execute(
            "SELECT user_id FROM learner_profiles WHERE user_id = ?", (learner_id,)
        ).fetchone()
        admin = database.execute(
            "SELECT id FROM users WHERE id = ? AND role = 'admin'", (admin_id,)
        ).fetchone()
        if not learner or not admin:
            return False
        database.execute(
            """
            UPDATE learner_profiles
            SET assigned_level = ?,
                registration_status = 'level_assigned',
                activity_access_enabled = 1,
                level_assigned_at = CURRENT_TIMESTAMP,
                level_assigned_by = ?
            WHERE user_id = ?
            """,
            (level, admin_id, learner_id),
        )
        database.execute(
            """
            INSERT INTO level_assignments (learner_id, level, assigned_by)
            VALUES (?, ?, ?)
            """,
            (learner_id, level, admin_id),
        )
        return True
