"""OpenBB wrapper around PyPortfolioOpt mean-variance optimization model"""

import pandas as pd
from pypfopt import expected_returns, risk_models
from pypfopt.efficient_frontier import EfficientFrontier

from openbb_optimization.models.optimizer_query_params import OptimizerQueryParams
from openbb_optimization.models.optimizer_result import (
    AllocationData,
    PortfolioStatsData,
    OptimizerResult,
)

async def _mpt_optimize(
    df: pd.DataFrame, params: OptimizerQueryParams
) -> OptimizerResult:
    """
    Run mean-variance optimization on price data.
    
    Parameters
    ----------
    df : pd.DataFrame
        Price data for all assets
    params : OptimizerQueryParams
        Optimization parameters
        
    Returns
    -------
    OptimizerResult
        Optimization results including allocations and portfolio stats
    """
    # Calculate expected returns and covariance matrix
    mu = expected_returns.mean_historical_return(df, frequency=252)
    s = risk_models.sample_cov(df, frequency=252)

    # Build the efficient frontier
    ef = EfficientFrontier(mu, s, weight_bounds=(0, params.max_weight))
    max_sharpe = ef.max_sharpe(risk_free_rate=params.risk_free_rate)
    weights = max_sharpe

    # Performance metrics
    portfolio_ret, portfolio_risk, portfolio_sharpe = max_sharpe.portfolio_performance(
        verbose=False, risk_free_rate=params.risk_free_rate
    )

    # Construct the allocations list
    allocations = []
    for symbol, weight in weights.items():
        if weight > 0:
            # Calculate return in excess of risk-free rate
            excess_return = mu[symbol] - params.risk_free_rate
            # Calculate volatility
            volatility = s[symbol][symbol] ** 0.5
            
            allocations.append(
                AllocationData(
                    symbol=symbol,
                    weight=weight,
                    excess_return=excess_return,
                    volatility=volatility,
                    sharpe_ratio=excess_return / volatility
                )
            )
            
    # Build final result
    stats = PortfolioStatsData(
        expected_return=portfolio_ret,
        volatility=portfolio_risk,
        sharpe_ratio=portfolio_sharpe,
    )
    
    return OptimizerResult(allocations=allocations, stats=stats)
