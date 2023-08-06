"""
Data models for type hints

A polygon is either a bounding box or a list of vertices
"""
from datetime import datetime
from typing import List, NewType, Optional, Tuple, Union

Polygon = NewType("Polygon", Union[List[float], List[List[float]]])  # type: ignore
TimeInterval = NewType("TimeInterval", Tuple[Optional[datetime], Optional[datetime]])
