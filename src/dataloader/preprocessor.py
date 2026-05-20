import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split

from .parser import parse_question, parse_choices, extract_answer
from .utils import bengali_char_ratio

# Minimum Bengali character ratio to consider a question valid
MIN_BENGALI_RATIO = 0.10


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies parsers to each row to extract question, choices, and answer.
    Adds id, domain, and source columns. LaTeX kept as-is.
    """
    df = df.copy()

    df["question"] = df["problem"].apply(parse_question)
    df["choices"]  = df["problem"].apply(parse_choices)
    df["answer"]   = df["solution"].apply(extract_answer)

    df["domain"] = "education"
    df["source"] = "NCTB_MCQ"
    df["id"]     = ["edu_{:04d}".format(i) for i in range(len(df))]

    return df


def validate(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Drops invalid rows and returns cleaned df + a report dict with drop counts.
    Checks: missing question, missing choices, missing answer, low Bengali ratio.
    """
    initial = len(df)
    report  = {}

    df = df[df["question"].notna()];              report["missing_question"] = initial - len(df)
    df = df[df["choices"].notna()];               report["missing_choices"]  = report["missing_question"] + initial - len(df) - report["missing_question"]
    df = df[df["answer"].notna()];                report["missing_answer"]   = initial - len(df) - sum(report.values())

    # Drop rows where question has too few Bengali characters (likely corrupt)
    low_ratio_mask        = df["question"].apply(bengali_char_ratio) < MIN_BENGALI_RATIO
    report["low_bengali"] = low_ratio_mask.sum()
    df = df[~low_ratio_mask]

    report["total_dropped"] = initial - len(df)
    report["remaining"]     = len(df)

    return df.reset_index(drop=True), report


def split_and_export(df: pd.DataFrame, out_dir: str,
                     train_ratio: float = 0.70,
                     val_ratio:   float = 0.15,
                     test_ratio:  float = 0.15,
                     seed: int = 42) -> dict:
    """
    Splits df into train/val/test (70/15/15) and saves as .jsonl files.
    Returns dict with split sizes and output file paths.
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "Ratios must sum to 1."

    # Columns to keep in final output
    keep_cols = ["id", "domain", "question", "choices", "answer", "source"]
    df = df[keep_cols]

    # First split off test set, then split remainder into train/val
    train_val, test = train_test_split(df, test_size=test_ratio, random_state=seed)
    val_size_adjusted = val_ratio / (train_ratio + val_ratio)
    train, val = train_test_split(train_val, test_size=val_size_adjusted, random_state=seed)

    os.makedirs(out_dir, exist_ok=True)

    paths = {}
    for split_name, split_df in [("train", train), ("val", val), ("test", test)]:
        path = os.path.join(out_dir, f"{split_name}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for _, row in split_df.iterrows():
                f.write(json.dumps(row.to_dict(), ensure_ascii=False) + "\n")
        paths[split_name] = path

    return {
        "train": len(train), "val": len(val), "test": len(test),
        "paths": paths
    }
