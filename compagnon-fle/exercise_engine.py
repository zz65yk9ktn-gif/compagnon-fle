from __future__ import annotations

from collections.abc import Mapping


RESULT_THRESHOLDS = (
    (0, 29, "too_difficult", "Niveau probablement trop difficile"),
    (30, 59, "fragile", "Compétences fragiles : nouvelle série au même niveau avec plus d’aide"),
    (60, 79, "partial", "Acquisition partielle : nouvelle série au même niveau"),
    (80, 94, "mastered", "Niveau globalement maîtrisé : consolidation ou niveau suivant"),
    (95, 100, "excellent", "Très bonne maîtrise : réévaluation possible au niveau supérieur"),
)


def normalize_text(value: object) -> str:
    return " ".join(str(value or "").strip().lower().split())


def recommendation_for_percentage(percentage: int) -> dict[str, object]:
    bounded = max(0, min(100, int(percentage)))
    for minimum, maximum, code, label in RESULT_THRESHOLDS:
        if minimum <= bounded <= maximum:
            return {"code": code, "label": label, "percentage": bounded}
    raise ValueError("Pourcentage hors seuils")


def evaluate_answer(question: Mapping[str, object], data: Mapping[str, str]):
    question_type = question["type"]
    expected = str(question.get("correct_answer", ""))

    if question_type == "manual_response":
        answer_text = str(data.get("answer_text", "")).strip()
        if not answer_text:
            raise ValueError("Une réponse ou une note de réalisation est nécessaire")
        return {
            "answer_text": answer_text,
            "is_correct": None,
            "score": None,
            "requires_manual_review": True,
        }

    if question_type == "multiple_choice":
        selected = sorted(
            letter
            for letter in ("A", "B", "C", "D")
            if data.get(f"answer_{letter}") == letter
        )
        if not selected:
            raise ValueError("Choisissez au moins une réponse")
        answer_text = "+".join(selected)
        is_correct = answer_text == expected
    elif question_type == "ordering":
        positions = {}
        for letter in question.get("choices", {}):
            value = data.get(f"position_{letter}", "")
            if not value.isdigit():
                raise ValueError("Attribuez une position à chaque élément")
            positions[letter] = int(value)
        if sorted(positions.values()) != list(range(1, len(positions) + 1)):
            raise ValueError("Chaque position doit être utilisée une seule fois")
        answer_text = "-".join(
            letter for letter, _ in sorted(positions.items(), key=lambda item: item[1])
        )
        is_correct = answer_text == expected
    else:
        answer_text = str(data.get("answer", "")).strip().upper()
        if not answer_text:
            raise ValueError("Choisissez une réponse")
        is_correct = normalize_text(answer_text) == normalize_text(expected)

    return {
        "answer_text": answer_text,
        "is_correct": is_correct,
        "score": 1.0 if is_correct else 0.0,
        "requires_manual_review": False,
    }


def validate_question_bank(sequence: Mapping[str, object]) -> None:
    required = {
        "id", "sequence", "level", "type", "instruction", "support",
        "choices", "correct_answer", "feedback_success", "feedback_error",
        "competency", "difficulty", "help", "source_group",
    }
    levels = sequence.get("levels", {})
    all_ids = []
    for level in ("A0", "A1", "A2", "B1", "B2"):
        questions = levels.get(level, [])
        if len(questions) != 10:
            raise ValueError(f"Le niveau {level} doit contenir dix questions")
        expected_ids = [f"S1-{level}-{number:03d}" for number in range(1, 11)]
        if [question.get("id") for question in questions] != expected_ids:
            raise ValueError(f"Identifiants invalides pour le niveau {level}")
        for index, question in enumerate(questions, start=1):
            missing = required - set(question)
            if missing:
                raise ValueError(f"Champs manquants pour {question.get('id')}: {missing}")
            source = question["source_group"]
            if index <= 5 and source != "reference_001_005":
                raise ValueError(f"Source principale invalide pour {question['id']}")
            if index >= 6 and source != "complement_006_010":
                raise ValueError(f"Source complémentaire invalide pour {question['id']}")
            all_ids.append(question["id"])
    if len(all_ids) != 50 or len(set(all_ids)) != 50:
        raise ValueError("La banque doit contenir cinquante identifiants uniques")
