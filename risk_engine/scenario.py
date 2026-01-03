import pandas as pd

def uniform_shock_pnl(weights: dict, shock_return: float) -> float:
    """
    Approximate portfolio P&L for a uniform shock to all assets.
    shock_return: e.g. -0.05 for -5%
    """
    w = pd.Series(weights)
    # If all assets move by the same shock, portfolio return ≈ weighted sum
    return float((w * shock_return).sum())
