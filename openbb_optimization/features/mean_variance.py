"""OpenBB wrapper around PyPortfolioOpt mean-variance optimization model"""

import pandas as pd
from pypfopt import expected_returns, risk_models
from pypfopt.efficient_frontier import EfficientFrontier

from openbb_optimization.models.optimizer_query_params import OptimizerQueryParams
from openbb_optimization.models.optimizer_result import (
    PerSymbolAllocation,
    PortfolioStats,
    OptimizerResult,
)

async def _mpt_optimize(
    df: pd.DataFrame, params: OptimizerQueryParams
) -> OptimizerResult:
    """Calculates returns and risk from price data and runs mean-variance optimizer on returns."""
    # Convert to daily returns

    # Calculate expected returns and covariance
    mu = expected_returns.mean_historical_return(df, frequency=252)
    s = risk_models.sample_cov(df, frequency=252)

    # Build the efficient frontier
    ef = EfficientFrontier(mu, s, weight_bounds=(0, params.max_weight))
    max_sharpe = ef.max_sharpe(risk_free_rate=params.risk_free_rate)
    weights = max_sharpe

    # Performance metrics
    portfolio_ret, portfolio_risk, portfolio_sharpe = ef.portfolio_performance(
        verbose=False, risk_free_rate=params.risk_free_rate
    )

    # Construct the allocations dict
    allocations = {}
    for symbol, w in weights.items():
        if w > 0:
            allocations[symbol] = PerSymbolAllocation(weight=w)

    # Build final result
    stats = PortfolioStats(
        expected_return=portfolio_ret,
        volatility=portfolio_risk,
        sharpe_ratio=portfolio_sharpe,
    )
    return OptimizerResult(allocations=allocations, stats=stats)
