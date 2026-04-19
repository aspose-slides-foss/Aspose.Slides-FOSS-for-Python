from __future__ import annotations
from abc import ABC, abstractmethod

class IChartDataWorksheet(ABC):
    """Represents worksheet associated with"""
    @property
    def name(self) -> str:
        """Gets the name. Read-only ."""
        ...

    @property
    def index(self) -> int:
        """Gets the index. Read-only ."""
        ...
