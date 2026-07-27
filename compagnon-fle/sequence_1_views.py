from __future__ import annotations

import html
import random
from collections.abc import Mapping

from exercise_engine import recommendation_for_percentage
from sequence_1 import SEQUENCE_1, question_by_id


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def question_number(question: Mapping[str, object]) -> int:
    return int(str(question["id"]).rsplit("-", 1)[1])


def _shuffled_choices(question: Mapping[str, object]) -> list[tuple[str, str, str]]:
    """Return choices with fresh visible A-D labels while preserving answer keys."""
    raw_choices = list(question.get("choices", {}).items())
    if question.get("type") == "single_choice" and len(raw_choices) == 3:
        raw_choices.append(("__extra__", "Je ne sais pas encore."))
    random.SystemRandom().shuffle(raw_choices)
    visible_letters = ("A", "B", "C", "D")
    return [
        (visible_letters[index], str(original_key), str(text))
        for index, (original_key, text) in enumerate(raw_choices[:4])
    ]


def _choices(question: Mapping[str, object]) -> str:
    choices = question.get("choices", {})
    question_type = question["type"]
    if question_type == "multiple_choice":
        return "".join(
            f'<label class="choice"><input type="checkbox" name="answer_{esc(letter)}" value="{esc(letter)}"><span><b>{esc(letter)}.</b> {esc(text)}</span></label>'
            for letter, text in choices.items()
        )
    if question_type == "ordering":
        count = len(choices)
        options = "".join(f'<option value="{number}">{number}</option>' for number in range(1, count + 1))
        return "".join(
            f'<label class="order-choice"><select name="position_{esc(letter)}" required><option value="">Position</option>{options}</select><span><b>{esc(letter)}.</b> {esc(text)}</span></label>'
            for letter, text in choices.items()
        )
    if question_type == "manual_response":
        return '<label>Ma réponse<textarea name="answer_text" rows="4" required></textarea></label><p class="manual-note">Cette production sera conservée pour être examinée par l’enseignant.</p>'
    return "".join(
        f'<label class="choice choice-direct"><input type="radio" name="answer" value="{esc(original_key)}" required onchange="this.form.requestSubmit()"><span class="choice-letter">{esc(visible_letter)}</span><span class="choice-text">{esc(text)}</span></label>'
        for visible_letter, original_key, text in _shuffled_choices(question)
    )


def question_page(layout, learner, csrf_token: str, run, question, message: str = "") -> str:
    number = question_number(question)
    progress = round(((number - 1) / run["total_questions"]) * 100)
    notice = f'<p class="notice notice-error">{esc(message)}</p>' if message else ""
    support = str(question.get("support", "")).strip()
    support_block = f'<div class="exercise-support"><strong>Support</strong><p>{esc(support)}</p></div>' if support else ""
    submit_button = "" if question["type"] == "single_choice" else '<button type="submit">Valider ma réponse</button>'
    return layout(
        SEQUENCE_1["title"],
        f"""<section class="sequence-section one-question">
  <div class="section-heading"><div><p class="eyebrow">Niveau {esc(run['level'])}</p><h1>{esc(SEQUENCE_1['title'])}</h1></div><a href="/espace-apprenant">Quitter</a></div>
  <div class="progress-label"><span>Question {number} sur {run['total_questions']}</span><span>{progress} %</span></div>
  <div class="progress-bar" aria-label="Progression"><span style="width:{progress}%"></span></div>
  {notice}
  <form method="post" action="/espace-apprenant/sequence-1" class="exercise-card question-form">
    <input type="hidden" name="csrf_token" value="{esc(csrf_token)}">
    <input type="hidden" name="run_id" value="{run['id']}">
    <input type="hidden" name="question_id" value="{esc(question['id'])}">
    <p class="exercise-number">Question {number} · {esc(question['competency'])}</p>
    <h2>{esc(question['instruction'])}</h2>
    {support_block}
    <div class="answer-options">{_choices(question)}</div>
    <details class="help-box"><summary>As-tu besoin d’aide ?</summary><p>{esc(question['help'])}</p></details>
    {submit_button}
  </form>
</section>""",
    )


def feedback_page(layout, learner, run, question, evaluation) -> str:
    number = question_number(question)
    manual = evaluation["requires_manual_review"]
    correct = evaluation["is_correct"] is True
    if manual:
        title = "Réponse enregistrée"
        detail = "Ton enseignant pourra examiner cette production. Elle n’entre pas encore dans le score automatique."
        css_class = "feedback-manual"
    elif correct:
        title = question["feedback_success"]
        detail = "Tu peux passer à la question suivante."
        css_class = "feedback-correct"
    else:
        title = question["feedback_error"]
        expected = question.get("source_expected_answer") or question.get("correct_answer")
        detail = f"Réponse attendue : {expected}."
        css_class = "feedback-review"
    completed = run["status"] == "completed"
    target = "/espace-apprenant/sequence-1/resultat" if completed else "/espace-apprenant/sequence-1"
    button = "Voir mon résultat" if completed else "Question suivante"
    return layout(
        "Retour sur la réponse",
        f"""<section class="card feedback-screen {css_class}">
  <p class="eyebrow">Question {number} sur {run['total_questions']}</p>
  <h1>{esc(title)}</h1>
  <p class="introduction">{esc(detail)}</p>
  <a class="primary-link" href="{target}">{button}</a>
</section>""",
    )


def result_page(layout, learner, run) -> str:
    evaluated = run["evaluated_count"]
    success = run["success_count"]
    percentage = run["score_percentage"] if run["score_percentage"] is not None else 0
    recommendation = recommendation_for_percentage(percentage)
    provisional = " Résultat automatique provisoire : les productions ouvertes restent à examiner." if run["manual_review_count"] else ""
    return layout(
        "Résultat de la séquence 1",
        f"""<section class="card result-card">
  <p class="eyebrow">Séquence 1 · Niveau {esc(run['level'])}</p>
  <h1>Ma série est terminée</h1>
  <div class="score-circle"><strong>{percentage} %</strong><span>de réussite automatique</span></div>
  <p><strong>{success} bonne(s) réponse(s) sur {evaluated} question(s) corrigée(s) automatiquement.</strong></p>
  <p>{run['manual_review_count']} production(s) à examiner par l’enseignant.{esc(provisional)}</p>
  <div class="recommendation"><strong>Recommandation pédagogique</strong><p>{esc(recommendation['label'])}</p></div>
  <p>Le niveau officiel reste <strong>{esc(run['level'])}</strong>. Seul l’administrateur peut le modifier.</p>
  <div class="result-actions"><a class="primary-link" href="/espace-apprenant/sequence-1?nouvelle=1">Commencer une nouvelle série</a><a href="/espace-apprenant">Retour à mon espace</a></div>
</section>""",
    )


def question_title(exercise_id: str) -> str:
    question = question_by_id(exercise_id)
    if not question:
        return exercise_id
    return f"Question {question_number(question)} — {question['competency']}"
