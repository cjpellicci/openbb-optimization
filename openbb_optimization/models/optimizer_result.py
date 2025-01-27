"""Optimizer Result Standard Model."""

from typing import List
from pydantic import Field
from openbb_core.provider.abstract.data import Data

class AllocationData(Data):
    """Individual allocation data for a symbol."""
    
    symbol: str = Field(description="The security's symbol")
    weight: float = Field(description="Portfolio weight allocation")
    excess_return: float = Field(description="Expected return contribution in excess of risk-free rate")
    volatility: float = Field(description="Individual volatility")
    sharpe_ratio: float = Field(description="Individual Sharpe ratio")
    
class PortfolioStatsData(Data):
    """Overall portfolio statistics"""
    
    excess_return: float = Field(description="Portfolio's expected return in excess of risk-free rate")
    volatility: float = Field(description="Portfolio volatility")
    sharpe_ratio: float = Field(description="Portfolio Sharpe ratio")

class OptimizerResult(Data):
    """
    Final output model for an optimized portfolio.
    """

    allocations: List[AllocationData] = Field(
        default_factory=list,
        description="List of allocation data for each symbol"
    )
    
    stats: PortfolioStatsData = Field(
        default_factory=PortfolioStatsData,
        description="Overall portfolio metrics"
    )
