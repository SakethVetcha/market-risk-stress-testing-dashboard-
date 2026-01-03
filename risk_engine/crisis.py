import pandas as pd
from .portfolio import portfolio_returns, summary_stats
from .var import historical_var, historical_es

def crisis_metrics(returns_df: pd.DataFrame,
                   weights: dict,
                   start_crisis: str,
                   end_crisis: str,
                   alpha: float = 0.95) -> dict:
    """
    Compute portfolio stats and VaR/ES within a crisis window.
    """
    crisis_rets = returns_df.loc[start_crisis:end_crisis]
    port_ret_crisis = portfolio_returns(crisis_rets, weights)

    stats_crisis = summary_stats(port_ret_crisis)
    h_var_c = historical_var(port_ret_crisis, alpha)
    h_es_c = historical_es(port_ret_crisis, alpha)

    stats_crisis.update({
        "hist_var": h_var_c,
        "hist_es": h_es_c,
        "n_days": len(port_ret_crisis),
    })
    return stats_crisis
