# Model registry: model_id -> inference config
# temperature=0 for deterministic MCQ; DeepSeek-R1 needs 0.6 per official docs
# use_system_prompt=False for DeepSeek-R1 series (all instructions in user turn)

MODEL_CONFIGS = {
    "Qwen/Qwen3-8B": {
        "temperature": 0.0,
        "use_system_prompt": True,
        "max_new_tokens": 32,
    },
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B": {
        "temperature": 0.6,
        "use_system_prompt": False,
        "max_new_tokens": 512,   # R1 outputs a reasoning chain before the answer
    },
    "md-nishat-008/TigerLLM-9B-it": {
        "temperature": 0.0,
        "use_system_prompt": True,
        "max_new_tokens": 32,
    },
    "md-nishat-008/TigerLLM-1B-it": {
        "temperature": 0.0,
        "use_system_prompt": True,
        "max_new_tokens": 32,
    },
    "hishab/titulm-llama-3.2-3b-v2.0": {
        "temperature": 0.0,
        "use_system_prompt": True,
        "max_new_tokens": 32,
    },
}
