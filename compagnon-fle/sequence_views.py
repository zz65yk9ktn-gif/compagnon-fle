from __future__ import annotations

import html
import random
from collections.abc import Mapping

from exercise_engine import recommendation_for_percentage
from sequences import question_by_id_any


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def question_number(question: Mapping[str, object]) -> int:
    return int(str(question["id"]).rsplit("-", 1)[1])


def _shuffled_choices(question: Mapping[str, object]) -> list[tuple[str, str, str]]:
    raw_choices = list(question.get("choices", {}).items())
    while len(raw_choices) < 4:
        raw_choices.append((f"__extra_{len(raw_choices)}", "Je ne sais pas encore."))
    random.SystemRandom().shuffle(raw_choices)
    return [
        (visible, str(original), str(text))
        for visible, (original, text) in zip(("A", "B", "C", "D"), raw_choices[:4])
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
        f'<label class="choice choice-direct"><input type="radio" name="answer" value="{esc(original_key)}" required><span class="choice-letter">{esc(visible_letter)}</span><span class="choice-text">{esc(text)}</span></label>'
        for visible_letter, original_key, text in _shuffled_choices(question)
    )


def question_page(layout, learner, csrf_token: str, run, sequence, question, message: str = "") -> str:
    number = run["current_index"] + 1
    progress = round((run["current_index"] / run["total_questions"]) * 100)
    notice = f'<p class="notice notice-error" role="alert" aria-live="assertive">{esc(message)}</p>' if message else ""
    support = str(question.get("support", "")).strip()
    support_block = f'<div class="exercise-support"><strong>Support</strong><p>{esc(support)}</p></div>' if support else ""
    submit_button = '<button type="submit">Valider ma réponse</button>'
    path = f'/espace-apprenant/{sequence["slug"]}/demarrer'
    return layout(
        sequence["title"],
        f"""<section class="sequence-section one-question">
  <div class="section-heading"><div><p class="eyebrow">Niveau {esc(run['level'])}</p><h1>{esc(sequence['title'])}</h1></div><a href="/espace-apprenant/{sequence['slug']}/accueil">Retour à la séquence</a></div>
  <div class="progress-label"><span>Question {number} sur {run['total_questions']}</span><span>{progress} %</span></div>
  <div class="progress-bar" aria-label="Progression"><span style="width:{progress}%"></span></div>
  {notice}
  <form method="post" action="{path}" class="exercise-card question-form">
    <input type="hidden" name="csrf_token" value="{esc(csrf_token)}">
    <input type="hidden" name="run_id" value="{run['id']}">
    <input type="hidden" name="question_id" value="{esc(question['id'])}">
    <p class="exercise-number">Question {number} · {esc(question['competency'])}</p>
    <h2>{esc(question['instruction'])}</h2>
    {support_block}
    <div class="answer-options" role="group" aria-label="Réponses proposées">{_choices(question)}</div>
    <details class="help-box"><summary>As-tu besoin d’aide ?</summary><p>{esc(question['help'])}</p></details>
    {submit_button}
  </form>
</section>""",
    )


def feedback_page(layout, learner, run, sequence, question, evaluation) -> str:
    number = run["current_index"]
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
        expected_key = str(question.get("correct_answer", ""))
        expected_text = question.get("choices", {}).get(expected_key, expected_key)
        detail = f"Réponse attendue : {expected_text}."
        css_class = "feedback-review"
    completed = run["status"] == "completed"
    base = f'/espace-apprenant/{sequence["slug"]}'
    target = f"{base}/resultat" if completed else base
    button = "Voir mon résultat" if completed else "Question suivante"
    return layout(
        "Retour sur la réponse",
        f"""<section class="card feedback-screen {css_class}" aria-live="polite" tabindex="-1">
  <p class="eyebrow">Question {number} sur {run['total_questions']}</p>
  <h1>{esc(title)}</h1>
  <p class="introduction">{esc(detail)}</p>
  <a class="primary-link" href="{target}">{button}</a>
</section>""",
    )


def result_page(layout, learner, run, sequence) -> str:
    evaluated = run["evaluated_count"]
    success = run["success_count"]
    percentage = run["score_percentage"] if run["score_percentage"] is not None else 0
    recommendation = recommendation_for_percentage(percentage)
    provisional = " Résultat automatique provisoire : les productions ouvertes restent à examiner." if run["manual_review_count"] else ""
    base = f'/espace-apprenant/{sequence["slug"]}'
    return layout(
        f"Résultat · {sequence['title']}",
        f"""<section class="card result-card" aria-live="polite" tabindex="-1">
  <p class="eyebrow">{esc(sequence['title'])} · Niveau {esc(run['level'])}</p>
  <h1>Ma série est terminée</h1>
  <div class="score-circle"><strong>{percentage} %</strong><span>de réussite automatique</span></div>
  <p><strong>{success} bonne(s) réponse(s) sur {evaluated} question(s) corrigée(s) automatiquement.</strong></p>
  <p>{run['manual_review_count']} production(s) à examiner par l’enseignant.{esc(provisional)}</p>
  <div class="recommendation"><strong>Recommandation pédagogique</strong><p>{esc(recommendation['label'])}</p></div>
  <p>Le niveau officiel reste <strong>{esc(run['level'])}</strong>. Seul l’administrateur peut le modifier.</p>
  <div class="result-actions"><a class="primary-link" href="{base}?nouvelle=1">Commencer une nouvelle série</a><a href="/espace-apprenant">Retour à mon espace</a></div>
</section>""",
    )


def question_title(exercise_id: str) -> str:
    question = question_by_id_any(exercise_id)
    if not question:
        return exercise_id
    return f"{exercise_id} — {question['competency']}"
