import re
from .utils import ANSWER_PATTERNS, BENGALI_TO_LETTER, bengali_to_letter


def parse_question(problem: str) -> str | None:
    """
    Extracts the question text from problem string.
    Question text appears before the first Bengali MCQ label 'ক:'.
    """
    match = re.split(r"\s*ক\s*:", problem, maxsplit=1)
    if len(match) < 2:
        return None
    return match[0].strip()


def parse_choices(problem: str) -> dict | None:
    """
    Extracts A/B/C/D choices from the problem string.
    Splits on Bengali labels ক/খ/গ/ঘ followed by colon.
    Returns dict like {"A": "...", "B": "...", "C": "...", "D": "..."} or None.
    """
    # Split on Bengali label boundaries: ক:, খ:, গ:, ঘ:
    parts = re.split(r"\s*([কখগঘ])\s*:", problem)
    # parts = [question_text, label1, choice1, label2, choice2, ...]
    # After split: index 0 = question, then pairs of (label, text)
    labels = parts[1::2]
    texts  = parts[2::2]

    if len(labels) != 4 or len(texts) != 4:
        return None

    choices = {}
    for label, text in zip(labels, texts):
        eng = bengali_to_letter(label)
        if eng is None:
            return None
        choices[eng] = text.strip()

    return choices if len(choices) == 4 else None


def extract_answer(solution: str) -> str | None:
    """
    Extracts the correct answer letter (A/B/C/D) from the solution text.
    Tries multiple regex patterns; returns first match or None.
    """
    for pattern in ANSWER_PATTERNS:
        match = re.search(pattern, solution)
        if match:
            bengali_label = match.group(1)
            return bengali_to_letter(bengali_label)
    return None
