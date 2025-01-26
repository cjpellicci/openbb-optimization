"""OpenBB wrapper around PyPortfolioOpt mean-variance optimization model"""

import pandas as pd
from pypfopt import expected_returns, risk_models
from pypfopt.efficient_frontier import EfficientFrontier

from openbb_optimization.models.optimizer_query_params import OptimizerQueryParams
from openbb_optimization.models.optimizer_result import (
    PerTickerAllocation,
    PortfolioStats,
    OptimizerResult,
)

async def _mpt_optimize(
    df: pd.DataFrame, params: OptimizerQueryParams
) -> OptimizerResult:
    """Calculates returns and risk from price data and runs mean-variance optimizer on returns."""
    # Convert to daily returns
    returns = df.pct_change().dropna()

    # Calculate expected returns and covariance
    mu = expected_returns.mean_historical_return(returns, frequency=252)
    s = risk_models.sample_cov(returns, frequency=252)

    # Build the efficient frontier
    ef = EfficientFrontier(mu, s, weight_bounds=(0, params.max_weight()))
    ef.max_sharpe(risk_free_rate=params.risk_free_rate)
    weights = ef.max_sharpe()

    # Performance metrics
    portfolio_ret, portfolio_risk, portfolio_sharpe = ef.portfolio_performance(
        verbose=False, risk_free_rate=params.risk_free_rate
    )

    # Construct the allocations dict
    allocations = {}
    for ticker, w in weights.items():
        if w > 0:
            allocations[ticker] = PerTickerAllocation(weight=w)

    # Build final result
    stats = PortfolioStats(
        expected_return=portfolio_ret,
        volatility=portfolio_risk,
        sharpe_ratio=portfolio_sharpe,
    )
    return OptimizerResult(allocations=allocations, stats=stats)
