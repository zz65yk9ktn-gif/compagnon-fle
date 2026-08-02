from __future__ import annotations

import hashlib
import hmac
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = Path(
    os.environ.get("DATABASE_PATH", str(DATA_DIR / "compagnon_fle.sqlite3"))
).expanduser()
LEVELS = ("A0", "A1", "A2", "B1", "B2")
PASSWORD_ITERATIONS = 310_000
SCHEMA_VERSION = 3
ROLES = ("learner", "teacher", "admin")
STAFF_ROLES = ("teacher", "admin")
ROLE_PERMISSIONS = {
    "learner": frozenset({"access_own_space", "submit_answers"}),
    "teacher": frozenset({"view_learners", "view_progress", "assign_levels"}),
    "admin": frozenset({"view_learners", "view_progress", "assign_levels", "manage_users"}),
}


def connect() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 10000")
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA synchronous = NORMAL")
    return connection


def initialize_database() -> None:
    with connect() as database:
        database.executescript(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                description TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS app_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

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
                run_id INTEGER NULL,
                requires_manual_review INTEGER NOT NULL DEFAULT 0
                    CHECK (requires_manual_review IN (0, 1)),
                attempted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (learner_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (run_id) REFERENCES exercise_runs(id) ON DELETE SET NULL
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
            CREATE INDEX IF NOT EXISTS idx_attempts_run ON exercise_attempts(run_id);
            CREATE INDEX IF NOT EXISTS idx_runs_completed ON exercise_runs(status, completed_at);
            """
        )
        user_sql_row = database.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'users'"
        ).fetchone()
        user_sql = user_sql_row["sql"] if user_sql_row else ""
        user_columns = {row["name"] for row in database.execute("PRAGMA table_info(users)")}
        needs_user_migration = (
            "teacher" not in user_sql
            or "is_active" not in user_columns
            or "disabled_at" not in user_columns
        )
        if needs_user_migration:
            database.execute("PRAGMA foreign_keys = OFF")
            database.execute(
                """
                CREATE TABLE users_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('learner', 'teacher', 'admin')),
                    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
                    disabled_at TEXT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            active_expr = "is_active" if "is_active" in user_columns else "1"
            disabled_expr = "disabled_at" if "disabled_at" in user_columns else "NULL"
            database.execute(
                f"""
                INSERT INTO users_new
                    (id, login, password_hash, role, is_active, disabled_at, created_at, updated_at)
                SELECT id, login, password_hash, role, {active_expr}, {disabled_expr},
                       created_at, updated_at
                FROM users
                """
            )
            database.execute("DROP TABLE users")
            database.execute("ALTER TABLE users_new RENAME TO users")
            database.execute("PRAGMA foreign_keys = ON")
            database.execute("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)")
            database.execute("CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active, role)")

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
            "INSERT OR IGNORE INTO schema_migrations(version, description) VALUES (?, ?)",
            (1, "Schéma initial : utilisateurs, profils, niveaux et exercices"),
        )
        database.execute(
            "INSERT OR IGNORE INTO schema_migrations(version, description) VALUES (?, ?)",
            (2, "Versionnement, métadonnées et index de robustesse"),
        )
        database.execute(
            "INSERT OR IGNORE INTO schema_migrations(version, description) VALUES (?, ?)",
            (3, "Rôles administrateur, enseignant et apprenant ; activation des comptes"),
        )
        database.execute(
            """
            INSERT INTO app_metadata(key, value, updated_at)
            VALUES ('schema_version', ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value, updated_at = CURRENT_TIMESTAMP
            """,
            (str(SCHEMA_VERSION),),
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


def database_health_report() -> dict[str, object]:
    """Return a compact, non-destructive integrity and schema report."""
    initialize_database()
    with connect() as database:
        integrity = database.execute("PRAGMA integrity_check").fetchone()[0]
        foreign_keys = database.execute("PRAGMA foreign_key_check").fetchall()
        version_row = database.execute(
            "SELECT value FROM app_metadata WHERE key = 'schema_version'"
        ).fetchone()
        tables = {
            row["name"]
            for row in database.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
            )
        }
        expected_tables = {
            "schema_migrations", "app_metadata", "users", "learner_profiles",
            "level_assignments", "exercise_attempts",
            "adaptation_recommendations", "exercise_runs",
        }
        missing_tables = sorted(expected_tables - tables)
        migrations = [
            dict(row)
            for row in database.execute(
                "SELECT version, applied_at, description FROM schema_migrations ORDER BY version"
            )
        ]
    return {
        "ok": integrity == "ok" and not foreign_keys and not missing_tables,
        "integrity_check": integrity,
        "foreign_key_errors": [tuple(row) for row in foreign_keys],
        "schema_version": int(version_row["value"]) if version_row else None,
        "expected_schema_version": SCHEMA_VERSION,
        "missing_tables": missing_tables,
        "migrations": migrations,
    }


def backup_database(destination: str | Path) -> Path:
    """Create a consistent SQLite backup using the native backup API."""
    initialize_database()
    target = Path(destination).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    with connect() as source, sqlite3.connect(target) as backup:
        source.backup(backup)
    return target


def database_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


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


def create_staff_user(*, login: str, password: str, role: str) -> int:
    if role not in STAFF_ROLES:
        raise ValueError("Rôle de personnel invalide")
    with connect() as database:
        cursor = database.execute(
            "INSERT INTO users (login, password_hash, role) VALUES (?, ?, ?)",
            (normalize_login(login), hash_password(password), role),
        )
        return int(cursor.lastrowid)


def create_admin(login: str, password: str) -> int:
    return create_staff_user(login=login, password=password, role="admin")


def create_teacher(login: str, password: str) -> int:
    return create_staff_user(login=login, password=password, role="teacher")


def authenticate_user(login: str, password: str, *, allowed_roles=ROLES):
    with connect() as database:
        user = database.execute(
            "SELECT id, login, password_hash, role, is_active FROM users WHERE login = ?",
            (normalize_login(login),),
        ).fetchone()
    if not user or not user["is_active"] or user["role"] not in allowed_roles:
        return None
    return user if verify_password(password, user["password_hash"]) else None


def authenticate_admin(login: str, password: str):
    return authenticate_user(login, password, allowed_roles=("admin",))


def authenticate_staff(login: str, password: str):
    return authenticate_user(login, password, allowed_roles=STAFF_ROLES)


def authenticate_teacher(login: str, password: str):
    return authenticate_user(login, password, allowed_roles=("teacher",))


def authenticate_learner(login: str, password: str):
    user = authenticate_user(login, password, allowed_roles=("learner",))
    if not user:
        return None
    with connect() as database:
        return database.execute(
            """
            SELECT users.id, users.login, users.password_hash, users.role, users.is_active,
                   learner_profiles.first_name, learner_profiles.registration_status,
                   learner_profiles.activity_access_enabled, learner_profiles.assigned_level
            FROM users
            JOIN learner_profiles ON learner_profiles.user_id = users.id
            WHERE users.id = ?
            """,
            (user["id"],),
        ).fetchone()



def reset_learner_password(*, learner_id: int, new_password: str, actor_id: int) -> bool:
    if len(new_password) < 12 or not any(c.isalpha() for c in new_password) or not any(c.isdigit() for c in new_password):
        return False
    with connect() as database:
        actor = database.execute(
            "SELECT role, is_active FROM users WHERE id = ?", (actor_id,)
        ).fetchone()
        learner = database.execute(
            "SELECT role, is_active FROM users WHERE id = ?", (learner_id,)
        ).fetchone()
        if (
            not actor
            or not actor["is_active"]
            or actor["role"] not in STAFF_ROLES
            or not learner
            or not learner["is_active"]
            or learner["role"] != "learner"
        ):
            return False
        database.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (hash_password(new_password), learner_id),
        )
        return True

def role_has_permission(role: str, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, frozenset())


def set_user_active(*, user_id: int, active: bool, actor_id: int) -> bool:
    with connect() as database:
        actor = database.execute(
            "SELECT role, is_active FROM users WHERE id = ?", (actor_id,)
        ).fetchone()
        target = database.execute(
            "SELECT role FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if (
            not actor
            or not actor["is_active"]
            or not role_has_permission(actor["role"], "manage_users")
            or not target
            or user_id == actor_id
        ):
            return False
        database.execute(
            """
            UPDATE users
            SET is_active = ?,
                disabled_at = CASE WHEN ? = 1 THEN NULL ELSE CURRENT_TIMESTAMP END,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (1 if active else 0, 1 if active else 0, user_id),
        )
        return True


def list_staff_users():
    with connect() as database:
        return database.execute(
            """
            SELECT id, login, role, is_active, disabled_at, created_at, updated_at
            FROM users
            WHERE role IN ('teacher', 'admin')
            ORDER BY role, login
            """
        ).fetchall()

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
        staff = database.execute(
            "SELECT id, role, is_active FROM users WHERE id = ?", (admin_id,)
        ).fetchone()
        if (
            not learner
            or not staff
            or not staff["is_active"]
            or not role_has_permission(staff["role"], "assign_levels")
        ):
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
