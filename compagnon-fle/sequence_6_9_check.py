#!/usr/bin/env python3
from __future__ import annotations

from exercise_engine import evaluate_answer, validate_question_bank
from sequences import SEQUENCES


def correct_submission(question):
    expected = str(question["correct_answer"])
    if question["type"] == "single_choice":
        return {"answer": expected}
    if question["type"] == "multiple_choice":
        keys = [key.strip() for key in expected.replace(",", "+").split("+") if key.strip()]
        return {f"answer_{key}": key for key in keys}
    if question["type"] == "ordering":
        return {
            f"position_{key}": str(index)
            for index, key in enumerate(expected.split("-"), start=1)
        }
    return {"answer_text": "Réponse de contrôle technique"}


def main() -> None:
    checked = 0
    for number in range(6, 10):
        sequence = SEQUENCES[number]
        validate_question_bank(sequence)
        assert sequence["slug"] == f"sequence-{number}"
        for level, questions in sequence["levels"].items():
            assert len(questions) == 5, (number, level, len(questions))
            for question in questions:
                result = evaluate_answer(question, correct_submission(question))
                if question["type"] == "manual_response":
                    assert result["requires_manual_review"] is True
                else:
                    assert result["is_correct"] is True, question["id"]
                checked += 1
    assert checked == 100, checked
    print("SEQUENCES_6_9_CHECK_OK")


if __name__ == "__main__":
    main()
