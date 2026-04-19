from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .slideshow.ITransitionValueBase import ITransitionValueBase
    from .slideshow.TransitionSpeed import TransitionSpeed
    from .slideshow.TransitionType import TransitionType

class ISlideShowTransition(ABC):
    """Represents slide show transition."""
    @property
    @abstractmethod
    def advance_on_click(self) -> bool:
        """Specifies whether a mouse click will advance the slide or not. If this attribute is not specified then a value of true is assumed. Read-write ."""
        ...

    @advance_on_click.setter
    @abstractmethod
    def advance_on_click(self, value: bool):
        ...

    @property
    @abstractmethod
    def advance_after(self) -> bool:
        """This attribute specifies if the slideshow will move to the next slide after a certain time. Read/write ."""
        ...

    @advance_after.setter
    @abstractmethod
    def advance_after(self, value: bool):
        ...

    @property
    @abstractmethod
    def advance_after_time(self) -> int:
        """Specifies the time, in milliseconds, after which the transition should start. This setting may be used in conjunction with the advClick attribute. If this attribute is not specified then it is assumed that no auto-advance will occur. Read-write ."""
        ...

    @advance_after_time.setter
    @abstractmethod
    def advance_after_time(self, value: int):
        ...

    @property
    @abstractmethod
    def speed(self) -> TransitionSpeed:
        """Specifies the transition speed that is to be used when transitioning from the current slide to the next. Read-write ."""
        ...

    @speed.setter
    @abstractmethod
    def speed(self, value: TransitionSpeed):
        ...

    @property
    @abstractmethod
    def value(self) -> ITransitionValueBase:
        """Slide show transition value. Read-only ."""
        ...

    @property
    @abstractmethod
    def type(self) -> TransitionType:
        """Type of transition. Read-write ."""
        ...

    @type.setter
    @abstractmethod
    def type(self, value: TransitionType):
        ...

    @property
    @abstractmethod
    def duration(self) -> int:
        """Gets or sets the duration of the slide transition effect in milliseconds. Read/write ."""
        ...

    @duration.setter
    @abstractmethod
    def duration(self, value: int):
        ...

