"""Optimizer Query Params Data Model"""

from typing import List, Optional
from pydantic import Field
from openbb_core.provider.abstract.query_params import QueryParams


class OptimizerQueryParams(QueryParams):
    """
    Query parameters for the portfolio optimizer.

    This defines which assets to optimize, as well as
    optional parameters like risk-free rate and date range.
    """

    symbols: List[str] = Field(
        ..., description="List of asset symbols to include in the portfolio."
    )
    start_date: Optional[str] = Field(
        None, description="Start date for historical data (YYYY-MM-DD)."
    )
    end_date: Optional[str] = Field(
        None, description="End date for historical data (YYYY-MM-DD)."
    )
    risk_free_rate: float = Field(
        0.0, description="Risk-free ratte assumption, e.g. 0.02 for 2%"
    )
    max_weight: float = Field(
        1.0, description="Max portfolio weight per asset, e.g. 0.50 for 50%"
    )
