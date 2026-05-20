from datasets import load_dataset
import pandas as pd


def load_nctb() -> pd.DataFrame:
    """
    Loads the NCTB_MCQ dataset from HuggingFace.
    Returns the train split as a pandas DataFrame.
    Dataset: nayemislamzr/NCTB_MCQ (8,480 rows, train split only)
    """
    ds = load_dataset("nayemislamzr/NCTB_MCQ", split="train")
    return ds.to_pandas()


def load_raw_as_dataframe() -> pd.DataFrame:
    """
    Alias for load_nctb(); returns raw df for quick inspection.
    Columns: source, problem, solution, messages
    """
    return load_nctb()
