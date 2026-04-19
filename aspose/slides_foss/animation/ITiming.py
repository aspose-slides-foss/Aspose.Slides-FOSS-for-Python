from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .EffectRestartType import EffectRestartType
    from .EffectTriggerType import EffectTriggerType

class ITiming(ABC):
    """Represents animation timing."""
    @property
    @abstractmethod
    def accelerate(self) -> float:
        """Describes the percentage of duration accelerate behavior effect. Read/write ."""
        ...
    @accelerate.setter
    @abstractmethod
    def accelerate(self, value: float):
        ...
    @property
    @abstractmethod
    def decelerate(self) -> float:
        """Describes the percentage of duration decelerate behavior effect. Read/write ."""
        ...
    @decelerate.setter
    @abstractmethod
    def decelerate(self, value: float):
        ...
    @property
    @abstractmethod
    def auto_reverse(self) -> bool:
        """Describes whether to automatically play the animation in reverse after playing it in the forward direction. Read/write ."""
        ...
    @auto_reverse.setter
    @abstractmethod
    def auto_reverse(self, value: bool):
        ...
    @property
    @abstractmethod
    def duration(self) -> float:
        """Describes the duration of animation effect. Read/write ."""
        ...
    @duration.setter
    @abstractmethod
    def duration(self, value: float):
        ...
    @property
    @abstractmethod
    def repeat_count(self) -> float:
        """Describes the number of times the effect should repeat. Read/write ."""
        ...
    @repeat_count.setter
    @abstractmethod
    def repeat_count(self, value: float):
        ...
    @property
    @abstractmethod
    def repeat_until_end_slide(self) -> bool:
        """This attribute specifies if the effect will repeat until the end of the slide. Read/write ."""
        ...
    @repeat_until_end_slide.setter
    @abstractmethod
    def repeat_until_end_slide(self, value: bool):
        ...
    @property
    @abstractmethod
    def repeat_until_next_click(self) -> bool:
        """This attribute specifies if the effect will repeat until the next click. Read/write ."""
        ...
    @repeat_until_next_click.setter
    @abstractmethod
    def repeat_until_next_click(self, value: bool):
        ...
    @property
    @abstractmethod
    def repeat_duration(self) -> float:
        """Describes the number of times the effect should repeat. Read/write ."""
        ...
    @repeat_duration.setter
    @abstractmethod
    def repeat_duration(self, value: float):
        ...
    @property
    @abstractmethod
    def restart(self) -> EffectRestartType:
        """Specifies if a effect is to restart after complete. Read/write ."""
        ...
    @restart.setter
    @abstractmethod
    def restart(self, value: EffectRestartType):
        ...
    @property
    @abstractmethod
    def speed(self) -> float:
        """Specifies the percentage by which to speed up (or slow down) the timing. Read/write ."""
        ...
    @speed.setter
    @abstractmethod
    def speed(self, value: float):
        ...
    @property
    @abstractmethod
    def trigger_delay_time(self) -> float:
        """Describes delay time after trigger. Read/write ."""
        ...
    @trigger_delay_time.setter
    @abstractmethod
    def trigger_delay_time(self, value: float):
        ...
    @property
    @abstractmethod
    def trigger_type(self) -> EffectTriggerType:
        """Describes trigger type. Read/write ."""
        ...
    @trigger_type.setter
    @abstractmethod
    def trigger_type(self, value: EffectTriggerType):
        ...
    @property
    @abstractmethod
    def rewind(self) -> bool:
        """This attribute specifies if the effect will rewind when done playing. Read/write ."""
        ...
    @rewind.setter
    @abstractmethod
    def rewind(self, value: bool):
        ...