import pandas as pd


def compute_metrics(df: pd.DataFrame) -> dict:
    """
    Computes evaluation metrics from a results DataFrame.
    Required columns: answer (gold), prediction (model output), domain.
    Returns dict with overall and per-domain accuracy + invalid response rate.
    """
    total = len(df)
    valid_mask = df["prediction"].notna()
    valid_df   = df[valid_mask]

    overall_acc    = (valid_df["prediction"] == valid_df["answer"]).mean()
    invalid_rate   = 1 - valid_mask.mean()

    # Per-domain accuracy (only over valid predictions)
    domain_acc = (
        valid_df.groupby("domain")
        .apply(lambda g: (g["prediction"] == g["answer"]).mean())
        .to_dict()
    )

    return {
        "total":          total,
        "valid":          valid_mask.sum(),
        "invalid":        (~valid_mask).sum(),
        "invalid_rate":   round(invalid_rate, 4),
        "overall_acc":    round(overall_acc, 4),
        "domain_acc":     {k: round(v, 4) for k, v in domain_acc.items()},
    }
