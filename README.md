# Bengali LLM Evaluation

Research project evaluating zero-shot and few-shot performance of multilingual and Bengali-native LLMs on domain-specific Bengali MCQ tasks (education, agriculture, law).

## Models
| Model | Type | Params |
|-------|------|--------|
| Qwen/Qwen3-8B | Multilingual | 8B |
| deepseek-ai/DeepSeek-R1-Distill-Qwen-7B | Reasoning-distilled | 7B |
| md-nishat-008/TigerLLM-9B-it | Bengali-native | 9B |
| md-nishat-008/TigerLLM-1B-it | Bengali-native | 1B |
| hishab/titulm-llama-3.2-3b-v2.0 | Bengali-native | 3B |

## Setup

```bash
pip install -r requirements.txt
```

## Project Structure

```
src/
  dataloader/     # Dataset loading and preprocessing
  evaluation/     # Prompt building, inference, metrics
notebooks/
  01_nctb_preprocessing.ipynb   # Build train/val/test splits
  02_zero_shot_inference.ipynb  # Run zero-shot evaluation
data/
  processed/      # train.jsonl, val.jsonl, test.jsonl
  results/        # Per-model prediction CSVs and metrics JSONs
```

## Running on Colab / Kaggle

```bash
git clone https://github.com/<your-username>/BengaliLLM.git
cd BengaliLLM
pip install -r requirements.txt
# Open notebooks/02_zero_shot_inference.ipynb
```

## Citation

```
TigerLLM: Raihan & Zampieri, ACL 2025
TituLLMs: Nahin et al., arXiv 2502.11187
BenLLM-Eval: Kabir et al., LREC-COLING 2024
```
