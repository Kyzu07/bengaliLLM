import re

# Bengali MCQ label to English mapping
BENGALI_TO_LETTER = {"ক": "A", "খ": "B", "গ": "C", "ঘ": "D"}

# Regex patterns to extract the correct answer label from solution text
# Covers: "সঠিক উত্তর হলো 'গ'", "উত্তর: ক", "\boxed{গ: ...}", "সঠিক উত্তর: খ"
ANSWER_PATTERNS = [
    r"\\boxed\{([কখগঘ])",                        # \boxed{গ: ...}
    r"সঠিক উত্তর[:\s]+হলো[:\s'\"]*([কখগঘ])",   # সঠিক উত্তর হলো 'গ'
    r"সঠিক উত্তর[:\s'\"]*([কখগঘ])",             # সঠিক উত্তর: গ
    r"উত্তর[:\s'\"]+([কখগঘ])",                  # উত্তর: ক
    r"সুতরাং[,\s]+সঠিক উত্তর[:\s'\"]*([কখগঘ])", # সুতরাং, সঠিক উত্তর হলো 'গ'
    r"([কখগঘ])[:\s]+(?:সঠিক|সর্বশেষ উত্তর)",   # গ: সঠিক
]


def bengali_to_letter(label: str) -> str | None:
    """Maps Bengali MCQ label (ক/খ/গ/ঘ) to English letter (A/B/C/D)."""
    return BENGALI_TO_LETTER.get(label.strip())


def bengali_char_ratio(text: str) -> float:
    """Returns fraction of Bengali Unicode characters in the text."""
    if not text:
        return 0.0
    bengali_chars = sum(1 for c in text if "\u0980" <= c <= "\u09FF")
    return bengali_chars / len(text)
