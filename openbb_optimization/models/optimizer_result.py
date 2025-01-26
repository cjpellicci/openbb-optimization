"""Results model to combine asset weights and portfolio-level
stats into one JSON-structured result object"""

from typing import Dict, Optional
from pydantic import BaseModel, Field
from openbb_core.provider.abstract.data import Data


class PerTickerAllocation(BaseModel):
    """Per-asset level data"""

    weight: float = Field(..., description="Portfolio weight in [0,1].")
    expected_return: Optional[float] = None
    risk: Optional[float] = None


class PortfolioStats(BaseModel):
    """Portfolio-level metrics"""

    expected_return: Optional[float] = None
    volatility: Optional[float] = None
    sharpe_ratio: Optional[float] = None


class OptimizerResult(Data):
    """
    Final output model for an optimized portfolio.
    """

    allocations: Dict[str, PerTickerAllocation] = Field(
        default_factory=dict,
        description="Mapping from ticker -> sub-model with weight, returns, etc.",
    )

    stats: PortfolioStats = Field(
        default_factory=PortfolioStats,
        description="Overall portfolio metrics (expected return, volatility, etc.)",
    )
