"""
This is a placeholder for a custom provider integration if needed.
If you're fetching data from a brand-new API, define a Fetcher class here.
"""

from openbb_core.provider.abstract.provider import Provider

provider = Provider(
    name="optimization",
    website="",
    description="A dummy or placeholder provider for my optimizer extension",
    fetcher_dict={}
)