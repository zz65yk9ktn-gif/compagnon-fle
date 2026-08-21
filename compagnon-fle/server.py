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
    MAX_PASSWORD_LENGTH,
    assign_level,
    authenticate_staff,
    authenticate_learner,
    change_user_password,
    create_learner,
    get_learner,
    get_active_learner_by_login,
    get_learner_progress,
    get_active_exercise_run,
    get_exercise_run,
    advance_exercise_run,
    initialize_database,
    learner_can_access_level,
    list_learners,
    record_exercise_attempt,
    start_exercise_run,
)
from exercise_engine import evaluate_answer, recommendation_for_percentage, validate_question_bank
from sequence_1 import SEQUENCE_1
from sequences import SEQUENCES, sequence_by_slug
from sequence_views import feedback_page, question_page, question_title, result_page
from support import SUPPORT_METHODOLOGY
from support_grammar import SUPPORT_GRAMMAR
from support_conjugation import SUPPORT_CONJUGATION
from support_cohesion import SUPPORT_COHESION
from support_vocabulary import SUPPORT_VOCABULARY
from support_writing import SUPPORT_WRITING


validate_question_bank(SEQUENCE_1)


BASE_DIR = Path(__file__).resolve().parent
SESSIONS: dict[str, dict] = {}
LOGIN_FAILURES: dict[tuple[str, str], deque] = defaultdict(deque)
REGISTRATION_ATTEMPTS: dict[str, deque] = defaultdict(deque)
SESSION_TTL_SECONDS = int(os.environ.get("SESSION_TTL_SECONDS", "28800"))
LOGIN_WINDOW_SECONDS = 15 * 60
MAX_LOGIN_FAILURES = 5
REGISTRATION_WINDOW_SECONDS = 60 * 60
MAX_REGISTRATIONS_PER_IP = 10
MAX_POST_BODY_BYTES = int(os.environ.get("MAX_POST_BODY_BYTES", "20000"))
MAX_ACTIVE_SESSIONS = int(os.environ.get("MAX_ACTIVE_SESSIONS", "2000"))
COMMON_LEARNER_PASSWORD = os.environ.get("COMMON_LEARNER_PASSWORD", "Compagnon2026")
PRODUCTION = os.environ.get("APP_ENV", "development").lower() == "production"
SECURE_COOKIES = os.environ.get(
    "SECURE_COOKIES", "true" if PRODUCTION else "false"
).lower() == "true"

SUPPORT_SEQUENCES = {
    SUPPORT_METHODOLOGY["slug"]: SUPPORT_METHODOLOGY,
    SUPPORT_GRAMMAR["slug"]: SUPPORT_GRAMMAR,
    SUPPORT_CONJUGATION["slug"]: SUPPORT_CONJUGATION,
    SUPPORT_COHESION["slug"]: SUPPORT_COHESION,
    SUPPORT_VOCABULARY["slug"]: SUPPORT_VOCABULARY,
    SUPPORT_WRITING["slug"]: SUPPORT_WRITING,
}


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def purge_expired_sessions() -> None:
    now = time.time()
    expired = [token for token, session in SESSIONS.items() if session.get("expires_at", 0) <= now]
    for token in expired:
        SESSIONS.pop(token, None)
    if len(SESSIONS) > MAX_ACTIVE_SESSIONS:
        oldest = sorted(SESSIONS.items(), key=lambda item: item[1].get("expires_at", 0))
        for token, _session in oldest[: len(SESSIONS) - MAX_ACTIVE_SESSIONS]:
            SESSIONS.pop(token, None)


def invalidate_user_sessions(*, learner_id: int | None = None, staff_id: int | None = None) -> None:
    for token, session in list(SESSIONS.items()):
        if learner_id is not None and session.get("learner_id") == learner_id:
            SESSIONS.pop(token, None)
        elif staff_id is not None and session.get("admin_id") == staff_id:
            SESSIONS.pop(token, None)


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


def dashboard_path_for_role(role: str) -> str:
    return "/espace-apprenant" if role == "learner" else "/administration"


def sequence_overview_page(learner, sequence, active_run=None) -> str:
    level = learner["assigned_level"]
    total = len(sequence["levels"][level])
    if active_run:
        action = f"Reprendre à la question {active_run['current_index'] + 1} sur {active_run['total_questions']}"
    else:
        action = f"Commencer les {total} questions"
    return layout(
        sequence["title"],
        f"""<section class="card sequence-overview">
  <div class="section-heading"><div><p class="eyebrow">{'Soutien · niveau commun' if sequence.get('track') == 'support' else f'Niveau {esc(level)}'}</p><h1>{esc(sequence['title'])}</h1></div><a href="/espace-apprenant">Retour au tableau de bord</a></div>
  <p class="introduction">Cette série comporte {total} questions. La progression est enregistrée automatiquement.</p>
  <a class="primary-link" href="/espace-apprenant/{esc(sequence['slug'])}/demarrer">{esc(action)}</a>
</section>""",
    )


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
    <button type="submit">Créer l’inscription</button>
  </form>
</section>""",
    )


def admin_login_page(message: str = "") -> str:
    notice = f'<p class="notice notice-error" role="alert">{esc(message)}</p>' if message else ""
    return layout(
        "Administration",
        f"""<section class="card form-card compact-card">
  <p class="eyebrow">Accès réservé</p>
  <h1>Administration des inscriptions</h1>
  {notice}
  <form method="post" action="/administration/connexion" class="form-grid">
    <label>Identifiant<input name="login" required autocomplete="username"></label>
    <label>Mot de passe<input type="password" name="password" required maxlength="{MAX_PASSWORD_LENGTH}" autocomplete="current-password"></label>
    <button type="submit">Se connecter</button>
  </form>
  <p class="form-help"><a href="/mot-de-passe-oublie?compte=administration">Mot de passe oublié ?</a></p>
</section>""",
    )


def learner_login_page(message: str = "") -> str:
    notice = f'<p class="notice notice-error" role="alert">{esc(message)}</p>' if message else ""
    return layout(
        "Connexion apprenant",
        f"""<section class="card form-card compact-card">
  <p class="eyebrow">Espace apprenant</p>
  <h1>Me connecter</h1>
  <p class="introduction">Utilisez votre identifiant et le mot de passe commun donné par votre enseignant.</p>
  {notice}
  <form method="post" action="/connexion/apprenant" class="form-grid">
    <label>Identifiant<input name="login" required autocomplete="username"></label>
    <label>Mot de passe<input type="password" name="password" required maxlength="{MAX_PASSWORD_LENGTH}" autocomplete="current-password"></label>
    <button type="submit">Accéder à mon espace</button>
  </form>
  <p class="form-help"><a href="/mot-de-passe-oublie">Mot de passe oublié ?</a></p>
</section>""",
    )


def forgot_password_page(*, staff: bool = False, message: str = "") -> str:
    if staff:
        body = """<p class="notice notice-waiting">Pour protéger l’administration, aucun compte personnel ne peut réinitialiser un accès administrateur. Contactez le responsable du déploiement.</p>
  <p class="form-help"><a href="/administration">Retour à la connexion administration</a></p>"""
    else:
        body = """<p class="notice notice-waiting">Le mot de passe est le même pour tous les élèves. Demandez-le simplement à votre enseignant.</p>
  <p class="form-help"><a href="/connexion">Retour à la connexion apprenant</a></p>"""
    return layout(
        "Mot de passe oublié",
        f"""<section class="card form-card compact-card">
  <p class="eyebrow">Récupération du compte</p><h1>Mot de passe oublié</h1>{body}
</section>""",
    )


def change_password_page(session: dict, message: str = "", error: bool = False) -> str:
    notice = (
        f'<p class="notice {"notice-error" if error else "notice-success"}" role="{"alert" if error else "status"}">{esc(message)}</p>'
        if message else ""
    )
    required = (
        '<p class="notice notice-waiting">Le mot de passe temporaire doit être remplacé avant de continuer.</p>'
        if session.get("must_change_password") else ""
    )
    back = "/espace-apprenant" if session["role"] == "learner" else "/administration"
    return layout(
        "Changer mon mot de passe",
        f"""<section class="card form-card compact-card">
  <p class="eyebrow">Sécurité du compte</p><h1>Changer mon mot de passe</h1>
  {required}{notice}
  <form method="post" action="/mot-de-passe" class="form-grid">
    <input type="hidden" name="csrf_token" value="{esc(session['csrf'])}">
    <label>Mot de passe actuel<input type="password" name="current_password" required maxlength="{MAX_PASSWORD_LENGTH}" autocomplete="current-password"></label>
    <label>Nouveau mot de passe<input type="password" name="new_password" required minlength="12" maxlength="{MAX_PASSWORD_LENGTH}" autocomplete="new-password" aria-describedby="password-rules"></label>
    <label>Confirmer le nouveau mot de passe<input type="password" name="confirmation" required minlength="12" maxlength="{MAX_PASSWORD_LENGTH}" autocomplete="new-password" aria-describedby="password-rules"></label>
    <p class="password-rules" id="password-rules">Entre 12 et {MAX_PASSWORD_LENGTH} caractères, avec au moins une lettre et un chiffre.</p>
    <button type="submit">Enregistrer le nouveau mot de passe</button>
  </form>
  {'' if session.get('must_change_password') else f'<p class="form-help"><a href="{back}">Retour</a></p>'}
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
        sequence_cards = []
        for number, sequence in SEQUENCES.items():
            if learner["assigned_level"] not in sequence["levels"]:
                continue
            count = len(sequence["levels"][learner["assigned_level"]])
            sequence_cards.append(f"""<article class="sequence-card">
    <p class="eyebrow">Séquence {number} · {count} questions</p>
    <h2>{esc(sequence['title'])}</h2>
    <p>Une question à la fois, avec un retour après chaque réponse.</p>
    <a class="primary-link" href="/espace-apprenant/{sequence['slug']}/accueil">Commencer la séquence {number}</a>
  </article>""")
        pilot = '<div class="sequence-grid">' + "".join(sequence_cards) + "</div>"
        content = f"""<p class="level-badge">Niveau {level}</p>
  <p class="introduction">Votre accès est limité à l’espace correspondant au niveau {level}.</p>
  {pilot}
  <section class="support-area">
    <p class="eyebrow">Soutien en français · niveau commun</p>
    <h2>Mes séries de soutien</h2>
    <div class="sequence-grid">
      <article class="sequence-card"><h3>Méthodologie</h3><p>40 questions pour comprendre les consignes et lire les documents.</p><a class="primary-link" href="/espace-apprenant/sequence-soutien-methodologie/accueil">Commencer</a></article>
      <article class="sequence-card"><h3>Grammaire</h3><p>72 questions sur la phrase, le verbe, le sujet et les accords.</p><a class="primary-link" href="/espace-apprenant/sequence-soutien-grammaire/accueil">Commencer</a></article>
      <article class="sequence-card"><h3>Conjugaison et temps</h3><p>56 questions sur le présent, le passé et le futur.</p><a class="primary-link" href="/espace-apprenant/sequence-soutien-conjugaison/accueil">Commencer</a></article>
      <article class="sequence-card"><h3>Cohésion et liens logiques</h3><p>56 questions pour relier les phrases et construire un paragraphe.</p><a class="primary-link" href="/espace-apprenant/sequence-soutien-cohesion/accueil">Commencer</a></article>
      <article class="sequence-card"><h3>Vocabulaire</h3><p>64 questions sur les familles de mots et le lexique utile.</p><a class="primary-link" href="/espace-apprenant/sequence-soutien-vocabulaire/accueil">Commencer</a></article>
      <article class="sequence-card"><h3>Écriture et communication</h3><p>64 questions pour écrire des messages clairs et adaptés.</p><a class="primary-link" href="/espace-apprenant/sequence-soutien-ecriture/accueil">Commencer</a></article>
    </div>
  </section>"""
        title = f"Mon espace {level}"
    return layout(
        "Espace apprenant",
        f"""<section class="card form-card compact-card">
  <div class="section-heading"><div><p class="eyebrow">Bonjour {esc(learner['first_name'])}</p><h1>{title}</h1></div><div class="account-links"><a href="/deconnexion">Se déconnecter</a></div></div>
  {content}
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
  <div class="section-heading"><div><p class="eyebrow">Administration</p><h1>Inscriptions</h1></div><div class="account-links"><a href="/mot-de-passe">Changer mon mot de passe</a><a href="/administration/deconnexion">Se déconnecter</a></div></div>
  {notice}
  <h2>Inscriptions</h2>
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
  <form method="post" action="/administration/mot-de-passe" class="level-form">
    <input type="hidden" name="csrf_token" value="{esc(session['csrf'])}">
    <input type="hidden" name="learner_id" value="{learner['id']}">
    <button type="submit">Rappeler le mot de passe commun</button>
  </form>
  <p><a class="primary-link" href="/administration/apprenant/suivi?id={learner['id']}">Consulter le suivi</a></p>
</section>""",
    )


def exercise_label(exercise_id: str) -> str:
    return question_title(exercise_id)


def sequence_label(sequence_slug: str) -> str:
    sequence = sequence_by_slug(sequence_slug)
    return sequence["title"] if sequence else sequence_slug


def learner_progress_page(learner) -> str:
    progress = get_learner_progress(learner["id"])
    summary = progress["summary"]
    attempts_count = summary["attempt_count"]
    evaluated_count = summary["evaluated_count"]
    success_rate = round((summary["success_count"] / evaluated_count) * 100) if evaluated_count else 0

    sequence_rows = "".join(
        f"""<tr><td>{esc(sequence_label(row['sequence_slug']))}</td><td>{esc(row['level'])}</td><td>{row['attempt_count']}</td><td>{row['success_count']}/{row['evaluated_count']}</td><td>{esc(row['last_attempt_at'])}</td></tr>"""
        for row in progress["sequences"]
    ) or '<tr><td colspan="5" class="empty">Aucune séquence travaillée.</td></tr>'

    attempt_rows = "".join(
        f"""<tr><td>{esc(exercise_label(row['exercise_id']))}</td><td>{esc(row['answer_text'])}</td><td>{'À examiner' if row['requires_manual_review'] else ('Réussite' if row['is_correct'] else 'Erreur')}</td><td>{(str(row['score']) + '/1') if row['score'] is not None else '—'}</td><td>{esc(row['attempted_at'])}</td></tr>"""
        for row in progress["attempts"]
    ) or '<tr><td colspan="5" class="empty">Aucun exercice réalisé.</td></tr>'

    difficulty_items = "".join(
        f"""<li><strong>{esc(exercise_label(row['exercise_id']))}</strong> — réponse « {esc(row['answer_text'])} » <small>({esc(row['attempted_at'])})</small></li>"""
        for row in progress["difficulties"]
    ) or "<li>Aucune difficulté enregistrée pour le moment.</li>"

    latest_run = progress["latest_run"]
    if latest_run and latest_run["status"] == "completed":
        recommendation = recommendation_for_percentage(latest_run["score_percentage"] or 0)
        adaptation_summary = f"""<div class="adaptation-summary">
    <span>Niveau administratif : <strong>{esc(latest_run['level'])}</strong></span>
    <span>Résultat automatique : <strong>{latest_run['score_percentage']} %</strong></span>
    <span>À examiner : <strong>{latest_run['manual_review_count']}</strong></span>
    <span>Recommandation : <strong>{esc(recommendation['label'])}</strong></span>
  </div>"""
    else:
        adaptation_summary = '<p class="notice notice-waiting">Aucune série terminée pour le moment.</p>'

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
  <h2>Dernier résultat et recommandation</h2>
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

    def send_security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "same-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("X-Permitted-Cross-Domain-Policies", "none")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; object-src 'none'")
        if SECURE_COOKIES:
            self.send_header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")

    def send_html(self, document: str, status: int = 200, cookie: str | None = None):
        payload = document.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_security_headers()
        self.send_header("Cache-Control", "no-store")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(payload)

    def redirect(self, location: str, cookie: str | None = None):
        self.send_response(303)
        self.send_header("Location", location)
        self.send_header("Cache-Control", "no-store")
        self.send_security_headers()
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()

    def form_data(self) -> dict[str, str]:
        content_type = self.headers.get("Content-Type", "")
        if not content_type.startswith("application/x-www-form-urlencoded"):
            raise ValueError("Type de formulaire non autorisé")
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("Taille de requête invalide") from exc
        if length < 0 or length > MAX_POST_BODY_BYTES:
            raise ValueError("Requête trop volumineuse")
        parsed = parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True)
        return {key: values[0] for key, values in parsed.items()}

    def current_session(self):
        purge_expired_sessions()
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
        return session if session and session.get("role") in {"admin", "teacher"} else None

    def current_learner_session(self):
        session = self.current_session()
        return session if session and session.get("role") == "learner" else None

    def password_change_required(self, session) -> bool:
        return bool(session and session.get("must_change_password"))

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            return self.send_html("OK")
        if path == "/":
            return super().do_GET() if (BASE_DIR / "index.html").exists() else self.send_error(404)
        if path == "/tableau-de-bord":
            session = self.current_session()
            return self.redirect(dashboard_path_for_role(session["role"])) if session else self.redirect("/connexion")
        if path == "/inscription":
            return self.send_html(registration_page())
        if path == "/connexion":
            session = self.current_learner_session()
            if session:
                return self.redirect("/mot-de-passe" if self.password_change_required(session) else "/espace-apprenant")
            return self.send_html(learner_login_page())
        if path == "/mot-de-passe-oublie":
            staff = parse_qs(urlparse(self.path).query).get("compte") == ["administration"]
            return self.send_html(forgot_password_page(staff=staff))
        if path == "/mot-de-passe":
            session = self.current_session()
            if not session:
                return self.redirect("/connexion")
            if session.get("role") == "learner":
                return self.redirect("/espace-apprenant")
            return self.send_html(change_password_page(session))
        if path == "/espace-apprenant":
            session = self.current_learner_session()
            if not session:
                return self.send_html(learner_login_page("Connectez-vous pour accéder à votre espace."), 401)
            if self.password_change_required(session):
                return self.redirect("/mot-de-passe")
            learner = get_learner(session["learner_id"])
            if not learner:
                return self.send_html(learner_login_page("Ce compte n’est plus disponible."), 401)
            return self.send_html(learner_space_page(learner))
        if path.startswith("/espace-apprenant/sequence-"):
            clean_path = path.rstrip("/")
            parts = clean_path.split("/")
            explicit_action = parts[-1] if parts[-1] in {"accueil", "demarrer", "resultat"} else None
            action = explicit_action or "accueil"
            slug = parts[-2] if explicit_action else parts[-1]
            sequence = sequence_by_slug(slug) or SUPPORT_SEQUENCES.get(slug)
            if sequence and not explicit_action:
                return self.redirect(f"/espace-apprenant/{sequence['slug']}/accueil")
            if sequence:
                session = self.current_learner_session()
                if not session:
                    message = "Connectez-vous pour voir ce résultat." if action == "resultat" else "Connectez-vous pour accéder à cette séquence."
                    return self.send_html(learner_login_page(message), 401)
                if self.password_change_required(session):
                    return self.redirect("/mot-de-passe")
                learner = get_learner(session["learner_id"])
                if not learner or not learner["assigned_level"] or not learner_can_access_level(learner["id"], learner["assigned_level"]):
                    return self.send_error(403, "Cette séquence ne correspond pas à votre niveau")
                level = learner["assigned_level"]
                if level not in sequence["levels"]:
                    return self.send_error(403, "Cette séquence ne correspond pas à votre niveau")
                if action == "accueil":
                    active = get_active_exercise_run(learner["id"], sequence["slug"], level)
                    return self.send_html(sequence_overview_page(learner, sequence, active))
                if action == "resultat":
                    progress = get_learner_progress(learner["id"])
                    run = progress["latest_run"] if progress else None
                    if not run or run["sequence_slug"] != sequence["slug"] or run["status"] != "completed":
                        return self.redirect(f"/espace-apprenant/{sequence['slug']}/accueil")
                    return self.send_html(result_page(layout, learner, run, sequence))
                query = parse_qs(urlparse(self.path).query)
                run = None if query.get("nouvelle") == ["1"] else get_active_exercise_run(learner["id"], sequence["slug"], level)
                if not run:
                    run_id = start_exercise_run(
                        learner_id=learner["id"], sequence_slug=sequence["slug"],
                        level=level, total_questions=len(sequence["levels"][level]),
                    )
                    run = get_exercise_run(run_id, learner["id"])
                if run["level"] != level:
                    return self.send_error(403, "Le niveau de cette série ne correspond plus au niveau attribué")
                question = sequence["levels"][level][run["current_index"]]
                return self.send_html(question_page(layout, learner, session["csrf"], run, sequence, question))
        if path == "/deconnexion":
            jar = cookies.SimpleCookie(self.headers.get("Cookie", ""))
            if jar.get("session"):
                SESSIONS.pop(jar["session"].value, None)
            return self.redirect(
                "/connexion", session_cookie("", clear=True)
            )
        if path == "/administration":
            session = self.current_admin_session()
            if self.password_change_required(session):
                return self.redirect("/mot-de-passe")
            return self.send_html(admin_page(session) if session else admin_login_page())
        if path == "/administration/apprenant":
            session = self.current_admin_session()
            if not session:
                return self.send_html(admin_login_page("Connectez-vous pour consulter cette fiche."), 401)
            if self.password_change_required(session):
                return self.redirect("/mot-de-passe")
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
            if self.password_change_required(session):
                return self.redirect("/mot-de-passe")
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
        try:
            data = self.form_data()
        except (UnicodeDecodeError, ValueError) as error:
            return self.send_error(413 if "volumineuse" in str(error) else 400, str(error))
        if path == "/inscription":
            return self.handle_registration(data)
        if path == "/mot-de-passe-oublie":
            return self.handle_forgot_password(data)
        if path == "/mot-de-passe":
            return self.handle_change_password(data)
        if path == "/administration/connexion":
            return self.handle_admin_login(data)
        if path == "/administration/niveau":
            return self.handle_level_assignment(data)
        if path == "/administration/mot-de-passe":
            return self.handle_password_reset(data)
        if path == "/connexion/apprenant":
            return self.handle_learner_login(data)
        if path.startswith("/espace-apprenant/sequence-"):
            parts = path.rstrip("/").split("/")
            slug = parts[-2] if parts[-1] == "demarrer" else parts[-1]
            sequence = sequence_by_slug(slug) or SUPPORT_SEQUENCES.get(slug)
            if sequence:
                return self.handle_sequence_submission(data, sequence)
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
        required = ("first_name", "birth_date", "class_name", "login")
        if any(not data.get(field, "").strip() for field in required):
            return self.send_html(registration_page("Tous les champs sont obligatoires.", True), 400)
        try:
            born = date.fromisoformat(data["birth_date"])
            if born >= date.today():
                raise ValueError
        except ValueError:
            return self.send_html(registration_page("La date de naissance n’est pas valide.", True), 400)
        try:
            create_learner(
                first_name=data["first_name"], birth_date=data["birth_date"],
                class_name=data["class_name"], login=data["login"], password=COMMON_LEARNER_PASSWORD
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
        staff = authenticate_staff(data.get("login", ""), data.get("password", ""))
        if not staff:
            self.record_rate_event(LOGIN_FAILURES, rate_key)
            return self.send_html(admin_login_page("Identifiant ou mot de passe incorrect."), 401)
        LOGIN_FAILURES.pop(rate_key, None)
        purge_expired_sessions()
        token = secrets.token_urlsafe(32)
        SESSIONS[token] = {
            "role": staff["role"],
            "admin_id": staff["id"],
            "must_change_password": bool(staff["must_change_password"]),
            "csrf": secrets.token_urlsafe(24),
            "expires_at": time.time() + SESSION_TTL_SECONDS,
        }
        return self.redirect(
            "/mot-de-passe" if staff["must_change_password"] else "/administration",
            session_cookie(token),
        )

    def handle_learner_login(self, data: dict[str, str]):
        normalized_login = data.get("login", "").strip().lower()
        rate_key = (self.client_identifier(), f"learner:{normalized_login}")
        if self.rate_limited(LOGIN_FAILURES, rate_key, MAX_LOGIN_FAILURES, LOGIN_WINDOW_SECONDS):
            return self.send_html(
                learner_login_page("Trop de tentatives. Réessayez dans 15 minutes."), 429
            )
        learner = authenticate_learner(data.get("login", ""), data.get("password", ""))
        if not learner and secrets.compare_digest(data.get("password", ""), COMMON_LEARNER_PASSWORD):
            learner = get_active_learner_by_login(data.get("login", ""))
        if not learner:
            self.record_rate_event(LOGIN_FAILURES, rate_key)
            return self.send_html(
                learner_login_page("Identifiant ou mot de passe incorrect."), 401
            )
        LOGIN_FAILURES.pop(rate_key, None)
        purge_expired_sessions()
        token = secrets.token_urlsafe(32)
        SESSIONS[token] = {
            "role": "learner",
            "learner_id": learner["id"],
            "must_change_password": False,
            "csrf": secrets.token_urlsafe(24),
            "expires_at": time.time() + SESSION_TTL_SECONDS,
        }
        return self.redirect(
            "/espace-apprenant",
            session_cookie(token),
        )

    def handle_sequence_submission(self, data: dict[str, str], sequence):
        session = self.current_learner_session()
        if not session:
            return self.send_html(learner_login_page("Connectez-vous pour accéder à cette séquence."), 401)
        if not secrets.compare_digest(data.get("csrf_token", ""), session["csrf"]):
            return self.send_error(403, "Requête non autorisée")
        learner = get_learner(session["learner_id"])
        if not learner or not learner["assigned_level"] or not learner_can_access_level(learner["id"], learner["assigned_level"]):
            return self.send_error(403, "Cette séquence ne correspond pas à votre niveau")
        try:
            run_id = int(data.get("run_id", ""))
        except ValueError:
            return self.send_error(400, "Série invalide")
        run = get_exercise_run(run_id, learner["id"])
        if not run or run["learner_id"] != learner["id"] or run["status"] != "in_progress":
            return self.send_error(409, "Cette série n’est plus active")
        level = learner["assigned_level"]
        if run["level"] != level or run["current_index"] >= run["total_questions"]:
            return self.send_error(409, "Progression incohérente")
        if run["sequence_slug"] != sequence["slug"]:
            return self.send_error(409, "Cette série ne correspond pas à la séquence demandée")
        question = sequence["levels"][level][run["current_index"]]
        if data.get("question_id") != question["id"]:
            return self.send_error(409, "Cette question a déjà été traitée")
        try:
            evaluation = evaluate_answer(question, data)
        except ValueError as error:
            return self.send_html(question_page(layout, learner, session["csrf"], run, sequence, question, str(error)), 400)
        try:
            record_exercise_attempt(
                learner_id=learner["id"], sequence_slug=sequence["slug"],
                exercise_id=question["id"], level=level,
                answer_text=evaluation["answer_text"], is_correct=evaluation["is_correct"],
                score=evaluation["score"], run_id=run_id,
                requires_manual_review=evaluation["requires_manual_review"],
            )
        except sqlite3.IntegrityError:
            return self.send_error(409, "Cette question a déjà été traitée")
        next_index = run["current_index"] + 1
        predicted_success = run["success_count"] + int(evaluation["is_correct"] is True)
        predicted_evaluated = run["evaluated_count"] + int(evaluation["is_correct"] is not None)
        completed = next_index >= run["total_questions"]
        score_percentage = round((predicted_success / predicted_evaluated) * 100) if completed and predicted_evaluated else None
        recommendation_code = recommendation_for_percentage(score_percentage)["code"] if score_percentage is not None else None
        advance_exercise_run(
            run_id=run_id, learner_id=learner["id"], is_correct=evaluation["is_correct"],
            requires_manual_review=evaluation["requires_manual_review"],
            score_percentage=score_percentage, recommendation_code=recommendation_code,
        )
        updated_run = get_exercise_run(run_id, learner["id"])
        return self.send_html(feedback_page(layout, learner, updated_run, sequence, question, evaluation))

    def handle_password_reset(self, data: dict[str, str]):
        session = self.current_admin_session()
        if not session:
            return self.send_html(admin_login_page("Votre session a expiré."), 401)
        if self.password_change_required(session):
            return self.redirect("/mot-de-passe")
        if not secrets.compare_digest(data.get("csrf_token", ""), session["csrf"]):
            return self.send_html(admin_page(session, "Requête non autorisée.", True), 403)
        try:
            learner_id = int(data.get("learner_id", ""))
        except ValueError:
            return self.send_html(admin_page(session, "Apprenant invalide.", True), 400)
        learner = get_learner(learner_id)
        if not learner:
            return self.send_html(admin_page(session, "Apprenant invalide.", True), 404)
        return self.send_html(
            learner_detail_page(
                session, learner,
                f"Mot de passe commun des élèves : {COMMON_LEARNER_PASSWORD}"
            )
        )

    def handle_forgot_password(self, data: dict[str, str]):
        return self.send_html(forgot_password_page())

    def handle_change_password(self, data: dict[str, str]):
        session = self.current_session()
        if not session:
            return self.redirect("/connexion")
        if not secrets.compare_digest(data.get("csrf_token", ""), session["csrf"]):
            return self.send_html(change_password_page(session, "Requête non autorisée.", True), 403)
        new_password = data.get("new_password", "")
        if new_password != data.get("confirmation", ""):
            return self.send_html(change_password_page(session, "Les nouveaux mots de passe ne correspondent pas.", True), 400)
        if len(new_password) < 12 or len(new_password) > MAX_PASSWORD_LENGTH or not any(c.isalpha() for c in new_password) or not any(c.isdigit() for c in new_password):
            return self.send_html(change_password_page(session, f"Le nouveau mot de passe doit contenir entre 12 et {MAX_PASSWORD_LENGTH} caractères, avec des lettres et des chiffres.", True), 400)
        user_id = session.get("learner_id") or session.get("admin_id")
        if not change_user_password(
            user_id=user_id,
            current_password=data.get("current_password", ""),
            new_password=new_password,
        ):
            return self.send_html(change_password_page(session, "Mot de passe actuel incorrect ou nouveau mot de passe inchangé.", True), 401)
        role = session["role"]
        if role == "learner":
            invalidate_user_sessions(learner_id=user_id)
            destination = "/connexion"
        else:
            invalidate_user_sessions(staff_id=user_id)
            destination = "/administration"
        return self.redirect(destination, session_cookie("", clear=True))

    def handle_level_assignment(self, data: dict[str, str]):
        session = self.current_admin_session()
        if not session:
            return self.send_html(admin_login_page("Votre session a expiré."), 401)
        if self.password_change_required(session):
            return self.redirect("/mot-de-passe")
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
    host = os.environ.get("HOST", "0.0.0.0")
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
