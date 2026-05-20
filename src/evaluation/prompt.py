SYSTEM_PROMPT = "তুমি একজন বাংলা ভাষার সহকারী।"

INSTRUCTION = (
    "নিচের বহুনির্বাচনী প্রশ্নটি পড়ো এবং সঠিক উত্তরের "
    "অক্ষরটি (A, B, C বা D) শুধুমাত্র লেখো।"
)


def build_prompt(row: dict, use_system_prompt: bool = True) -> list[dict]:
    """
    Builds a chat-format prompt (list of message dicts) from a dataset row.
    row must have: question (str), choices (dict with A/B/C/D keys).
    Returns messages list ready for tokenizer.apply_chat_template().
    """
    choices = row["choices"]
    user_content = (
        f"{INSTRUCTION}\n\n"
        f"প্রশ্ন: {row['question']}\n\n"
        f"A: {choices['A']}\n"
        f"B: {choices['B']}\n"
        f"C: {choices['C']}\n"
        f"D: {choices['D']}\n\n"
        f"উত্তর:"
    )

    messages = []
    if use_system_prompt:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    messages.append({"role": "user", "content": user_content})

    return messages
