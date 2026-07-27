#!/usr/bin/env python3

from __future__ import annotations

import html
import os
import secrets
import sqlite3
import time
from collections import defaultdict, deque
from datetime import date
from http import cookies
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from database import (
    LEVELS,
    assign_level,
    authenticate_admin,
    authenticate_learner,
    create_learner,
    get_learner,
    get_learner_progress,
    get_latest_adaptation,
    initialize_database,
    learner_can_access_level,
    list_learners,
    record_exercise_attempt,
    record_adaptation_recommendation,
)
from sequence_1 import SEQUENCE_1


BASE_DIR = Path(__file__).resolve().parent
SESSIONS: dict[str, dict] = {}
LOGIN_FAILURES: dict[tuple[str, str], deque] = defaultdict(deque)
REGISTRATION_ATTEMPTS: dict[str, deque] = defaultdict(deque)
SESSION_TTL_SECONDS = int(os.environ.get("SESSION_TTL_SECONDS", "28800"))
LOGIN_WINDOW_SECONDS = 15 * 60
MAX_LOGIN_FAILURES = 5
REGISTRATION_WINDOW_SECONDS = 60 * 60
MAX_REGISTRATIONS_PER_IP = 10
PRODUCTION = os.environ.get("APP_ENV", "development").lower() == "production"
SECURE_COOKIES = os.environ.get(
    "SECURE_COOKIES", "true" if PRODUCTION else "false"
).lower() == "true"


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def layout(title: str, content: str) -> str:
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} · Compagnon FLE</title>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <header class="site-header">
    <a class="brand" href="/">Compagnon FLE</a>
    <nav><a href="/inscription">Inscription</a><a href="/connexion">Connexion apprenant</a><a href="/administration">Administration</a></nav>
  </header>
  <main>{content}</main>
  <footer><p>Compagnon numérique du manuel FLE</p></footer>
</body>
</html>"""


def session_cookie(token: str, *, clear: bool = False) -> str:
    parts = [f"session={token}", "Path=/", "HttpOnly", "SameSite=Strict"]
    if SECURE_COOKIES:
        parts.append("Secure")
    if clear:
        parts.append("Max-Age=0")
    else:
        parts.append(f"Max-Age={SESSION_TTL_SECONDS}")
    return "; ".join(parts)


def registration_page(message: str = "", error: bool = False) -> str:
    notice = (
        f'<p class="notice {"notice-error" if error else "notice-success"}">{esc(message)}</p>'
        if message
        else ""
    )
    return layout(
        "Inscription",
        f"""<section class="card form-card">
  <p class="eyebrow">Espace apprenant</p>
  <h1>Créer mon inscription</h1>
  <p class="introduction">Après l’inscription, votre compte aura le statut <strong>« En attente d’attribution du niveau »</strong>. Seul un administrateur pourra choisir votre niveau.</p>
  {notice}
  <form method="post" action="/inscription" class="form-grid">
    <label>Prénom<input name="first_name" required maxlength="80" autocomplete="given-name"></label>
    <label>Date de naissance<input type="date" name="birth_date" required></label>
    <label>Classe<input name="class_name" required maxlength="100" placeholder="Ex. CAP 1 EPC"></label>
    <label>Identifiant de connexion<input name="login" required minlength="3" maxlength="80" autocomplete="username"></label>
    <label>Mot de passe<input type="password" name="password" required minlength="12" autocomplete="new-password"></label>
    <label>Confirmer le mot de passe<input type="password" name="confirmation" required minlength="12" autocomplete="new-password"></label>
    <button type="submit">Créer l’inscription</button>
  </form>
</section>""",
    )


def admin_login_page(message: str = "") -> str:
    notice = f'<p class="notice notice-error">{esc(message)}</p>' if message else ""
    return layout(
        "Administration",
        f"""<section class="card form-card compact-card">
  <p class="eyebrow">Accès réservé</p>
  <h1>Administration des inscriptions</h1>
  {notice}
  <form method="post" action="/administration/connexion" class="form-grid">
    <label>Identifiant<input name="login" required autocomplete="username"></label>
    <label>Mot de passe<input type="password" name="password" required autocomplete="current-password"></label>
    <button type="submit">Se connecter</button>
  </form>
</section>""",
    )


def learner_login_page(message: str = "") -> str:
    notice = f'<p class="notice notice-error">{esc(message)}</p>' if message else ""
    return layout(
        "Connexion apprenant",
        f"""<section class="card form-card compact-card">
  <p class="eyebrow">Espace apprenant</p>
  <h1>Me connecter</h1>
  <p class="introduction">Utilisez l’identifiant et le mot de passe choisis lors de votre inscription.</p>
  {notice}
  <form method="post" action="/connexion/apprenant" class="form-grid">
    <label>Identifiant<input name="login" required autocomplete="username"></label>
    <label>Mot de passe<input type="password" name="password" required autocomplete="current-password"></label>
    <button type="submit">Accéder à mon espace</button>
  </form>
</section>""",
    )


def learner_space_page(learner) -> str:
    if (
        learner["registration_status"] != "level_assigned"
        or not learner["activity_access_enabled"]
        or not learner["assigned_level"]
    ):
        content = """<p class="notice notice-waiting">Votre inscription est enregistrée. Votre niveau doit encore être attribué par un administrateur.</p>"""
        title = "Niveau en attente"
    else:
        level = esc(learner["assigned_level"])
        pilot = ""
        if learner["assigned_level"] == SEQUENCE_1["level"]:
            pilot = f"""<article class="sequence-card">
    <p class="eyebrow">Séquence pilote</p>
    <h2>{esc(SEQUENCE_1['title'])}</h2>
    <p>Quelques exercices tests pour valider le fonctionnement.</p>
    <a class="primary-link" href="/espace-apprenant/sequence-1">Commencer la séquence 1</a>
  </article>"""
        content = f"""<p class="level-badge">Niveau {level}</p>
  <p class="introduction">Votre accès est limité à l’espace correspondant au niveau {level}.</p>
  {pilot}"""
        title = f"Mon espace {level}"
    return layout(
        "Espace apprenant",
        f"""<section class="card form-card compact-card">
  <div class="section-heading"><div><p class="eyebrow">Bonjour {esc(learner['first_name'])}</p><h1>{title}</h1></div><a href="/deconnexion">Se déconnecter</a></div>
  {content}
</section>""",
    )


def normalize_answer(value: str) -> str:
    return " ".join(value.strip().lower().split())


def adaptation_difficulty(success_count: int, exercise_count: int) -> str:
    if exercise_count != 3:
        raise ValueError("La règle pilote attend trois exercices")
    if success_count <= 1:
        return "accessible"
    if success_count == 2:
        return "equivalent"
    return "demanding"


def sequence_page(
    learner, csrf_token: str, answers: dict[str, str] | None = None, adaptation=None
) -> str:
    exercises = []
    for number, exercise in enumerate(SEQUENCE_1["exercises"], start=1):
        answer = (answers or {}).get(exercise["id"], "")
        correction = ""
        if answers is not None:
            accepted = {normalize_answer(item) for item in exercise["accepted_answers"]}
            is_correct = normalize_answer(answer) in accepted
            correction = f"""<div class="exercise-feedback {'feedback-correct' if is_correct else 'feedback-review'}">
      <strong>{'Réponse correcte.' if is_correct else 'À revoir.'}</strong>
      <p><b>Score de cette tentative :</b> {1 if is_correct else 0}/1</p>
      <p><b>Réponse attendue :</b> {esc(exercise['expected_answer'])}</p>
      <p><b>Correction :</b> {esc(exercise['correction'])}</p>
    </div>"""
        exercises.append(
            f"""<article class="exercise-card">
    <p class="exercise-number">Exercice {number}</p>
    <h2>{esc(exercise['title'])}</h2>
    <p><strong>Consigne :</strong> {esc(exercise['instruction'])}</p>
    <div class="exercise-support"><strong>Support :</strong> {esc(exercise['support'])}</div>
    <label>Votre réponse<input name="{esc(exercise['id'])}" value="{esc(answer)}" required></label>
    {correction}
  </article>"""
        )
    adaptation_block = ""
    if adaptation:
        difficulty = adaptation["difficulty"]
        proposed = SEQUENCE_1["adaptive_exercises"][difficulty]
        adaptation_block = f"""<section class="adaptation-card">
    <p class="eyebrow">Prochaine proposition</p>
    <div class="level-separation"><span>Niveau administratif : <strong>{esc(adaptation['official_level'])}</strong></span><span>Difficulté momentanée : <strong>{esc(proposed['label'])}</strong></span></div>
    <p>Résultat de la série : <strong>{adaptation['success_count']}/{adaptation['exercise_count']}</strong></p>
    <h2>{esc(proposed['title'])}</h2>
    <p><strong>Consigne :</strong> {esc(proposed['instruction'])}</p>
    <div class="exercise-support"><strong>Support :</strong> {esc(proposed['support'])}</div>
  </section>"""
    return layout(
        SEQUENCE_1["title"],
        f"""<section class="sequence-section">
  <div class="section-heading"><div><p class="eyebrow">Niveau {esc(SEQUENCE_1['level'])}</p><h1>{esc(SEQUENCE_1['title'])}</h1></div><a href="/espace-apprenant">Retour à mon espace</a></div>
  <form method="post" action="/espace-apprenant/sequence-1" class="exercise-list">
    <input type="hidden" name="csrf_token" value="{esc(csrf_token)}">
    {''.join(exercises)}
    <button type="submit">Vérifier mes réponses</button>
  </form>
  {adaptation_block}
</section>""",
    )


def admin_page(session: dict, message: str = "", error: bool = False) -> str:
    rows = []
    for learner in list_learners():
        options = ['<option value="">Choisir…</option>']
        for level in LEVELS:
            selected = " selected" if learner["assigned_level"] == level else ""
            options.append(f'<option value="{level}"{selected}>{level}</option>')
        current = learner["assigned_level"] or "En attente d’attribution du niveau"
        status = (
            "Niveau attribué"
            if learner["registration_status"] == "level_assigned"
            else "En attente d’attribution du niveau"
        )
        rows.append(
            f"""<tr>
  <td><strong>{esc(learner['first_name'])}</strong><br><small>{esc(learner['login'])}</small></td>
  <td>{esc(learner['birth_date'])}</td>
  <td>{esc(learner['class_name'])}</td>
  <td>{esc(status)}</td>
  <td><span class="level-badge">{esc(current)}</span></td>
  <td>
    <form method="post" action="/administration/niveau" class="inline-form">
      <input type="hidden" name="csrf_token" value="{esc(session['csrf'])}">
      <input type="hidden" name="learner_id" value="{learner['id']}">
      <select name="level" required>{''.join(options)}</select>
      <button type="submit">Attribuer</button>
    </form>
    <a class="detail-link" href="/administration/apprenant?id={learner['id']}">Voir la fiche</a>
  </td>
</tr>"""
        )
    body = "".join(rows) or '<tr><td colspan="6" class="empty">Aucune inscription.</td></tr>'
    notice = (
        f'<p class="notice {"notice-error" if error else "notice-success"}">{esc(message)}</p>'
        if message
        else ""
    )
    return layout(
        "Inscriptions",
        f"""<section class="admin-section">
  <div class="section-heading"><div><p class="eyebrow">Administration</p><h1>Inscriptions</h1></div><a href="/administration/deconnexion">Se déconnecter</a></div>
  {notice}
  <div class="table-wrapper"><table>
    <thead><tr><th>Apprenant</th><th>Naissance</th><th>Classe</th><th>Statut</th><th>Niveau actuel</th><th>Attribution manuelle</th></tr></thead>
    <tbody>{body}</tbody>
  </table></div>
</section>""",
    )


def learner_detail_page(session: dict, learner, message: str = "", error: bool = False) -> str:
    status = (
        "Niveau attribué"
        if learner["registration_status"] == "level_assigned"
        else "En attente d’attribution du niveau"
    )
    access = (
        f"Autorisé pour les activités du niveau {esc(learner['assigned_level'])}"
        if learner["activity_access_enabled"] and learner["assigned_level"]
        else "Accès aux activités en attente"
    )
    options = ['<option value="">Choisir…</option>']
    for level in LEVELS:
        selected = " selected" if learner["assigned_level"] == level else ""
        options.append(f'<option value="{level}"{selected}>{level}</option>')
    notice = (
        f'<p class="notice {"notice-error" if error else "notice-success"}">{esc(message)}</p>'
        if message
        else ""
    )
    return layout(
        "Fiche apprenant",
        f"""<section class="admin-section learner-sheet">
  <div class="section-heading"><div><p class="eyebrow">Fiche apprenant</p><h1>{esc(learner['first_name'])}</h1></div><a href="/administration">Retour aux inscriptions</a></div>
  {notice}
  <dl class="profile-grid">
    <div><dt>Identifiant</dt><dd>{esc(learner['login'])}</dd></div>
    <div><dt>Date de naissance</dt><dd>{esc(learner['birth_date'])}</dd></div>
    <div><dt>Classe</dt><dd>{esc(learner['class_name'])}</dd></div>
    <div><dt>Inscription</dt><dd>{esc(learner['created_at'])}</dd></div>
    <div><dt>Statut</dt><dd>{esc(status)}</dd></div>
    <div><dt>Accès</dt><dd>{access}</dd></div>
  </dl>
    <form method="post" action="/administration/niveau" class="level-form">
    <input type="hidden" name="csrf_token" value="{esc(session['csrf'])}">
    <input type="hidden" name="learner_id" value="{learner['id']}">
    <input type="hidden" name="return_to" value="detail">
    <label>Niveau attribué<select name="level" required>{''.join(options)}</select></label>
    <button type="submit">Attribuer le niveau et autoriser l’accès</button>
  </form>
  <p><a class="primary-link" href="/administration/apprenant/suivi?id={learner['id']}">Consulter le suivi</a></p>
</section>""",
    )


def exercise_label(exercise_id: str) -> str:
    for exercise in SEQUENCE_1["exercises"]:
        if exercise["id"] == exercise_id:
            return exercise["title"]
    return exercise_id


def sequence_label(sequence_slug: str) -> str:
    return SEQUENCE_1["title"] if sequence_slug == SEQUENCE_1["slug"] else sequence_slug


def learner_progress_page(learner) -> str:
    progress = get_learner_progress(learner["id"])
    summary = progress["summary"]
    attempts_count = summary["attempt_count"]
    success_rate = round((summary["success_count"] / attempts_count) * 100) if attempts_count else 0

    sequence_rows = "".join(
        f"""<tr><td>{esc(sequence_label(row['sequence_slug']))}</td><td>{esc(row['level'])}</td><td>{row['attempt_count']}</td><td>{row['success_count']}/{row['attempt_count']}</td><td>{esc(row['last_attempt_at'])}</td></tr>"""
        for row in progress["sequences"]
    ) or '<tr><td colspan="5" class="empty">Aucune séquence travaillée.</td></tr>'

    attempt_rows = "".join(
        f"""<tr><td>{esc(exercise_label(row['exercise_id']))}</td><td>{esc(row['answer_text'])}</td><td>{'Réussite' if row['is_correct'] else 'Erreur'}</td><td>{esc(row['score']) if row['score'] is not None else '—'}/1</td><td>{esc(row['attempted_at'])}</td></tr>"""
        for row in progress["attempts"]
    ) or '<tr><td colspan="5" class="empty">Aucun exercice réalisé.</td></tr>'

    difficulty_items = "".join(
        f"""<li><strong>{esc(exercise_label(row['exercise_id']))}</strong> — réponse « {esc(row['answer_text'])} » <small>({esc(row['attempted_at'])})</small></li>"""
        for row in progress["difficulties"]
    ) or "<li>Aucune difficulté enregistrée pour le moment.</li>"

    latest_adaptation = progress["latest_adaptation"]
    if latest_adaptation:
        proposed = SEQUENCE_1["adaptive_exercises"][latest_adaptation["difficulty"]]
        adaptation_summary = f"""<div class="adaptation-summary">
    <span>Niveau administratif : <strong>{esc(latest_adaptation['official_level'])}</strong></span>
    <span>Difficulté momentanée : <strong>{esc(proposed['label'])}</strong></span>
    <span>Dernier résultat : <strong>{latest_adaptation['success_count']}/{latest_adaptation['exercise_count']}</strong></span>
  </div>"""
    else:
        adaptation_summary = '<p class="notice notice-waiting">Aucune adaptation proposée pour le moment.</p>'

    return layout(
        "Suivi apprenant",
        f"""<section class="admin-section progress-section">
  <div class="section-heading"><div><p class="eyebrow">Suivi apprenant</p><h1>{esc(learner['first_name'])}</h1></div><a href="/administration/apprenant?id={learner['id']}">Retour à la fiche</a></div>
  <div class="progress-summary">
    <div><span>Niveau attribué</span><strong>{esc(learner['assigned_level'] or 'En attente')}</strong></div>
    <div><span>Séquences travaillées</span><strong>{summary['sequence_count']}</strong></div>
    <div><span>Exercices réalisés</span><strong>{summary['exercise_count']}</strong></div>
    <div><span>Taux de réussite</span><strong>{success_rate} %</strong></div>
  </div>
  <h2>Dernière adaptation</h2>
  {adaptation_summary}
  <h2>Séquences travaillées</h2>
  <div class="table-wrapper"><table><thead><tr><th>Séquence</th><th>Niveau</th><th>Tentatives</th><th>Réussites</th><th>Dernière activité</th></tr></thead><tbody>{sequence_rows}</tbody></table></div>
  <h2>Exercices réalisés</h2>
  <div class="table-wrapper"><table><thead><tr><th>Exercice</th><th>Réponse donnée</th><th>Résultat</th><th>Score</th><th>Date</th></tr></thead><tbody>{attempt_rows}</tbody></table></div>
  <section class="difficulty-list"><h2>Dernières difficultés observées</h2><ul>{difficulty_items}</ul></section>
</section>""",
    )


class AppHandler(SimpleHTTPRequestHandler):
    server_version = "CompagnonFLE"
    sys_version = ""

    def translate_path(self, path: str) -> str:
        parsed = urlparse(path).path
        return str(BASE_DIR / parsed.lstrip("/"))

    def send_html(self, document: str, status: int = 200, cookie: str | None = None):
        payload = document.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "same-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(payload)

    def redirect(self, location: str, cookie: str | None = None):
        self.send_response(303)
        self.send_header("Location", location)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()

    def form_data(self) -> dict[str, str]:
        length = int(self.headers.get("Content-Length", "0"))
        if length > 20_000:
            return {}
        parsed = parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True)
        return {key: values[0] for key, values in parsed.items()}

    def current_session(self):
        jar = cookies.SimpleCookie(self.headers.get("Cookie", ""))
        token = jar.get("session")
        session = SESSIONS.get(token.value) if token else None
        if session and session.get("expires_at", 0) <= time.time():
            SESSIONS.pop(token.value, None)
            return None
        return session

    def client_identifier(self) -> str:
        return self.client_address[0]

    def rate_limited(self, store, key, maximum: int, window_seconds: int) -> bool:
        now = time.time()
        attempts = store[key]
        while attempts and attempts[0] <= now - window_seconds:
            attempts.popleft()
        return len(attempts) >= maximum

    def record_rate_event(self, store, key) -> None:
        store[key].append(time.time())

    def current_admin_session(self):
        session = self.current_session()
        return session if session and session.get("role") == "admin" else None

    def current_learner_session(self):
        session = self.current_session()
        return session if session and session.get("role") == "learner" else None

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            return self.send_html("OK")
        if path == "/":
            return super().do_GET() if (BASE_DIR / "index.html").exists() else self.send_error(404)
        if path == "/inscription":
            return self.send_html(registration_page())
        if path == "/connexion":
            session = self.current_learner_session()
            return self.redirect("/espace-apprenant") if session else self.send_html(learner_login_page())
        if path == "/espace-apprenant":
            session = self.current_learner_session()
            if not session:
                return self.send_html(learner_login_page("Connectez-vous pour accéder à votre espace."), 401)
            learner = get_learner(session["learner_id"])
            if not learner:
                return self.send_html(learner_login_page("Ce compte n’est plus disponible."), 401)
            return self.send_html(learner_space_page(learner))
        if path == "/espace-apprenant/sequence-1":
            session = self.current_learner_session()
            if not session:
                return self.send_html(learner_login_page("Connectez-vous pour accéder à cette séquence."), 401)
            learner = get_learner(session["learner_id"])
            if not learner or not learner_can_access_level(learner["id"], SEQUENCE_1["level"]):
                return self.send_error(403, "Cette séquence ne correspond pas à votre niveau")
            return self.send_html(sequence_page(learner, session["csrf"]))
        if path == "/deconnexion":
            jar = cookies.SimpleCookie(self.headers.get("Cookie", ""))
            if jar.get("session"):
                SESSIONS.pop(jar["session"].value, None)
            return self.redirect(
                "/connexion", session_cookie("", clear=True)
            )
        if path == "/administration":
            session = self.current_admin_session()
            return self.send_html(admin_page(session) if session else admin_login_page())
        if path == "/administration/apprenant":
            session = self.current_admin_session()
            if not session:
                return self.send_html(admin_login_page("Connectez-vous pour consulter cette fiche."), 401)
            try:
                learner_id = int(parse_qs(urlparse(self.path).query).get("id", [""])[0])
            except ValueError:
                return self.send_error(400, "Apprenant invalide")
            learner = get_learner(learner_id)
            return self.send_html(learner_detail_page(session, learner)) if learner else self.send_error(404)
        if path == "/administration/apprenant/suivi":
            session = self.current_admin_session()
            if not session:
                return self.send_html(admin_login_page("Connectez-vous pour consulter ce suivi."), 401)
            try:
                learner_id = int(parse_qs(urlparse(self.path).query).get("id", [""])[0])
            except ValueError:
                return self.send_error(400, "Apprenant invalide")
            learner = get_learner(learner_id)
            return self.send_html(learner_progress_page(learner)) if learner else self.send_error(404)
        if path == "/administration/deconnexion":
            jar = cookies.SimpleCookie(self.headers.get("Cookie", ""))
            if jar.get("session"):
                SESSIONS.pop(jar["session"].value, None)
            return self.redirect(
                "/administration", session_cookie("", clear=True)
            )
        if path in ("/styles.css",):
            return super().do_GET()
        self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        data = self.form_data()
        if path == "/inscription":
            return self.handle_registration(data)
        if path == "/administration/connexion":
            return self.handle_admin_login(data)
        if path == "/administration/niveau":
            return self.handle_level_assignment(data)
        if path == "/connexion/apprenant":
            return self.handle_learner_login(data)
        if path == "/espace-apprenant/sequence-1":
            return self.handle_sequence_submission(data)
        self.send_error(404)

    def handle_registration(self, data: dict[str, str]):
        client = self.client_identifier()
        if self.rate_limited(
            REGISTRATION_ATTEMPTS, client, MAX_REGISTRATIONS_PER_IP, REGISTRATION_WINDOW_SECONDS
        ):
            return self.send_html(
                registration_page("Trop d’inscriptions ont été tentées. Réessayez plus tard.", True),
                429,
            )
        self.record_rate_event(REGISTRATION_ATTEMPTS, client)
        required = ("first_name", "birth_date", "class_name", "login", "password", "confirmation")
        if any(not data.get(field, "").strip() for field in required):
            return self.send_html(registration_page("Tous les champs sont obligatoires.", True), 400)
        if (
            len(data["password"]) < 12
            or not any(character.isalpha() for character in data["password"])
            or not any(character.isdigit() for character in data["password"])
        ):
            return self.send_html(
                registration_page(
                    "Le mot de passe doit contenir au moins 12 caractères, avec des lettres et des chiffres.",
                    True,
                ),
                400,
            )
        if data["password"] != data["confirmation"]:
            return self.send_html(registration_page("Les mots de passe ne correspondent pas.", True), 400)
        try:
            born = date.fromisoformat(data["birth_date"])
            if born >= date.today():
                raise ValueError
        except ValueError:
            return self.send_html(registration_page("La date de naissance n’est pas valide.", True), 400)
        try:
            create_learner(
                first_name=data["first_name"], birth_date=data["birth_date"],
                class_name=data["class_name"], login=data["login"], password=data["password"]
            )
        except sqlite3.IntegrityError:
            return self.send_html(registration_page("Cet identifiant de connexion existe déjà.", True), 409)
        return self.send_html(
            registration_page(
                "Inscription enregistrée. Votre compte est en attente d’attribution du niveau."
            )
        )

    def handle_admin_login(self, data: dict[str, str]):
        rate_key = (self.client_identifier(), "admin")
        if self.rate_limited(LOGIN_FAILURES, rate_key, MAX_LOGIN_FAILURES, LOGIN_WINDOW_SECONDS):
            return self.send_html(admin_login_page("Trop de tentatives. Réessayez dans 15 minutes."), 429)
        admin = authenticate_admin(data.get("login", ""), data.get("password", ""))
        if not admin:
            self.record_rate_event(LOGIN_FAILURES, rate_key)
            return self.send_html(admin_login_page("Identifiant ou mot de passe incorrect."), 401)
        LOGIN_FAILURES.pop(rate_key, None)
        token = secrets.token_urlsafe(32)
        SESSIONS[token] = {
            "role": "admin",
            "admin_id": admin["id"],
            "csrf": secrets.token_urlsafe(24),
            "expires_at": time.time() + SESSION_TTL_SECONDS,
        }
        return self.redirect(
            "/administration",
            session_cookie(token),
        )

    def handle_learner_login(self, data: dict[str, str]):
        rate_key = (self.client_identifier(), "learner")
        if self.rate_limited(LOGIN_FAILURES, rate_key, MAX_LOGIN_FAILURES, LOGIN_WINDOW_SECONDS):
            return self.send_html(
                learner_login_page("Trop de tentatives. Réessayez dans 15 minutes."), 429
            )
        learner = authenticate_learner(data.get("login", ""), data.get("password", ""))
        if not learner:
            self.record_rate_event(LOGIN_FAILURES, rate_key)
            return self.send_html(
                learner_login_page("Identifiant ou mot de passe incorrect."), 401
            )
        LOGIN_FAILURES.pop(rate_key, None)
        token = secrets.token_urlsafe(32)
        SESSIONS[token] = {
            "role": "learner",
            "learner_id": learner["id"],
            "csrf": secrets.token_urlsafe(24),
            "expires_at": time.time() + SESSION_TTL_SECONDS,
        }
        return self.redirect(
            "/espace-apprenant",
            session_cookie(token),
        )

    def handle_sequence_submission(self, data: dict[str, str]):
        session = self.current_learner_session()
        if not session:
            return self.send_html(learner_login_page("Connectez-vous pour accéder à cette séquence."), 401)
        if not secrets.compare_digest(data.get("csrf_token", ""), session["csrf"]):
            return self.send_error(403, "Requête non autorisée")
        learner = get_learner(session["learner_id"])
        if not learner or not learner_can_access_level(learner["id"], SEQUENCE_1["level"]):
            return self.send_error(403, "Cette séquence ne correspond pas à votre niveau")
        answers = {
            exercise["id"]: data.get(exercise["id"], "")
            for exercise in SEQUENCE_1["exercises"]
        }
        for exercise in SEQUENCE_1["exercises"]:
            answer = answers[exercise["id"]]
            accepted = {normalize_answer(item) for item in exercise["accepted_answers"]}
            is_correct = normalize_answer(answer) in accepted
            record_exercise_attempt(
                learner_id=learner["id"],
                sequence_slug=SEQUENCE_1["slug"],
                exercise_id=exercise["id"],
                level=SEQUENCE_1["level"],
                answer_text=answer,
                is_correct=is_correct,
                score=1.0 if is_correct else 0.0,
            )
        success_count = sum(
            normalize_answer(answers[exercise["id"]])
            in {normalize_answer(item) for item in exercise["accepted_answers"]}
            for exercise in SEQUENCE_1["exercises"]
        )
        exercise_count = len(SEQUENCE_1["exercises"])
        difficulty = adaptation_difficulty(success_count, exercise_count)
        record_adaptation_recommendation(
            learner_id=learner["id"],
            sequence_slug=SEQUENCE_1["slug"],
            official_level=learner["assigned_level"],
            success_count=success_count,
            exercise_count=exercise_count,
            difficulty=difficulty,
        )
        adaptation = get_latest_adaptation(learner["id"], SEQUENCE_1["slug"])
        return self.send_html(sequence_page(learner, session["csrf"], answers, adaptation))

    def handle_level_assignment(self, data: dict[str, str]):
        session = self.current_admin_session()
        if not session:
            return self.send_html(admin_login_page("Votre session a expiré."), 401)
        if not secrets.compare_digest(data.get("csrf_token", ""), session["csrf"]):
            return self.send_html(admin_page(session, "Requête non autorisée.", True), 403)
        try:
            learner_id = int(data.get("learner_id", ""))
        except ValueError:
            return self.send_html(admin_page(session, "Apprenant invalide.", True), 400)
        if not assign_level(learner_id=learner_id, level=data.get("level", ""), admin_id=session["admin_id"]):
            return self.send_html(admin_page(session, "Attribution impossible.", True), 400)
        if data.get("return_to") == "detail":
            learner = get_learner(learner_id)
            return self.send_html(
                learner_detail_page(
                    session,
                    learner,
                    "Niveau attribué. L’accès aux activités correspondantes est autorisé.",
                )
            )
        return self.send_html(admin_page(session, "Niveau attribué et historisé."))


def main() -> None:
    initialize_database()
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), AppHandler)
    print(f"Compagnon FLE : http://{host}:{port}")
    print("Pour arrêter l’application, appuyez sur Ctrl+C.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nApplication arrêtée.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
