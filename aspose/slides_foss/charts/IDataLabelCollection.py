from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
from .IChartComponent import IChartComponent

if TYPE_CHECKING:
    from ..ISlideComponent import ISlideComponent
    from ..IPresentationComponent import IPresentationComponent
    from ..IBaseSlide import IBaseSlide
    from .IChart import IChart
    from .IChartLinesFormat import IChartLinesFormat
    from .IChartSeries import IChartSeries
    from .IDataLabel import IDataLabel
    from .IDataLabelFormat import IDataLabelFormat
    from ..IPresentation import IPresentation

class IDataLabelCollection(IChartComponent, ABC):
    """Represents a series labels."""
    @property
    def default_data_label_format(self) -> IDataLabelFormat:
        """Returns default format of all data labels in the collection. Read-only ."""
        ...

    @property
    def leader_lines_format(self) -> IChartLinesFormat:
        """Represents data labels leader lines format. Read-only ."""
        ...

    @property
    def is_visible(self) -> bool:
        """False means that data label is not visible by default (and so all Show*-flags (ShowValue, ...) of the DefaultDataLabelFormat property are false). Read-only ."""
        ...

    @property
    def count_of_visible_data_labels(self) -> int:
        """Gets the number of visible data labels in the collection. Read-only ."""
        ...

    @property
    def count(self) -> int:
        """Gets the number of all data labels in the collection. Read-only ."""
        ...

    @property
    def parent_series(self) -> IChartSeries:
        """Returns parent chart series. Read-only ."""
        ...

    @property
    def chart(self) -> IChart:
        ...

    @property
    def slide(self) -> IBaseSlide:
        ...

    @property
    def presentation(self) -> IPresentation:
        ...

    def hide(self) -> None:
        ...

    def index_of(self, value) -> int:
        ...

    def __getitem__(self, index: int) -> IDataLabel:
        ...
