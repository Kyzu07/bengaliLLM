import re

# For standard models: grab the first standalone A/B/C/D in the output
_DIRECT_PATTERN = re.compile(r"\b([A-D])\b")

# For DeepSeek-R1: answer often appears after </think> or at the very end
_THINK_END_PATTERN = re.compile(r"</think>.*?\b([A-D])\b", re.DOTALL)


def extract_prediction(output: str, is_reasoning_model: bool = False) -> str | None:
    """
    Extracts A/B/C/D prediction from raw model output string.
    For reasoning models (DeepSeek-R1), looks after the </think> tag first.
    Returns letter string or None if not found.
    """
    if is_reasoning_model:
        match = _THINK_END_PATTERN.search(output)
        if match:
            return match.group(1)

    match = _DIRECT_PATTERN.search(output)
    return match.group(1) if match else None
