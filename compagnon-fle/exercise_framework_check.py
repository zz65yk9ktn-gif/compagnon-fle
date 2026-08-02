#!/usr/bin/env python3
from __future__ import annotations

from exercise_engine import evaluate_answer, validate_question_bank
from sequences import SEQUENCES


def check() -> None:
    for sequence in SEQUENCES.values():
        validate_question_bank(sequence)

    single = {"type": "single_choice", "choices": {"A": "Oui", "B": "Non"}, "correct_answer": "A"}
    assert evaluate_answer(single, {"answer": "A"})["is_correct"] is True
    assert evaluate_answer(single, {"answer": "B"})["is_correct"] is False

    multiple = {"type": "multiple_choice", "choices": {"A": "Un", "B": "Deux", "C": "Trois"}, "correct_answer": "A+C"}
    assert evaluate_answer(multiple, {"answer_A": "A", "answer_C": "C"})["is_correct"] is True

    ordering = {"type": "ordering", "choices": {"A": "Un", "B": "Deux", "C": "Trois"}, "correct_answer": "B-A-C"}
    assert evaluate_answer(ordering, {"position_A": "2", "position_B": "1", "position_C": "3"})["is_correct"] is True

    manual = {"type": "manual_response", "choices": {}, "correct_answer": ""}
    result = evaluate_answer(manual, {"answer_text": "Ma production"})
    assert result["requires_manual_review"] is True
    assert result["score"] is None

    print("Cadre technique des exercices : OK")


if __name__ == "__main__":
    check()
