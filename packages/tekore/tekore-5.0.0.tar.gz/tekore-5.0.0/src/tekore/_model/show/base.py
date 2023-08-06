from typing import List, Optional

from ..base import Item
from ..member import Copyright, Image


class Show(Item):
    """Show base."""

    available_markets: List[str]
    copyrights: List[Copyright]
    description: str
    explicit: bool
    external_urls: dict
    images: List[Image]
    is_externally_hosted: Optional[bool]
    languages: List[str]
    media_type: str
    name: str
    publisher: str
    total_episodes: Optional[int] = None
    html_description: str = None
