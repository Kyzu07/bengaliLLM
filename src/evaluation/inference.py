import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def load_model_and_tokenizer(model_id: str):
    """
    Loads model and tokenizer from HuggingFace.
    Uses bfloat16 and auto device map for multi-GPU / MPS / CPU fallback.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
    model.eval()
    return model, tokenizer


def generate_response(
    messages:       list[dict],
    model,
    tokenizer,
    temperature:    float = 0.0,
    max_new_tokens: int   = 32,
) -> str:
    """
    Applies chat template, runs generation, and returns decoded new tokens only.
    temperature=0 → greedy decoding (do_sample=False).
    """
    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True,
    ).to(model.device)

    do_sample = temperature > 0.0

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature if do_sample else None,
            do_sample=do_sample,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Decode only newly generated tokens (strip prompt)
    new_ids = output_ids[0][inputs["input_ids"].shape[-1]:]
    return tokenizer.decode(new_ids, skip_special_tokens=True)
