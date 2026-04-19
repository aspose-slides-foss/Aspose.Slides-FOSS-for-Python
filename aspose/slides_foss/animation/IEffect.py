from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .AfterAnimationType import AfterAnimationType
    from .AnimateTextType import AnimateTextType
    from .EffectPresetClassType import EffectPresetClassType
    from .EffectSubtype import EffectSubtype
    from .EffectType import EffectType
    from ..IAudio import IAudio
    from .IBehaviorCollection import IBehaviorCollection
    from ..IColorFormat import IColorFormat
    from .ISequence import ISequence
    from ..IShape import IShape
    from .ITextAnimation import ITextAnimation
    from .ITiming import ITiming

class IEffect(ABC):
    """Represents animation effect."""
    @property
    @abstractmethod
    def sequence(self) -> ISequence:
        """Returns a sequence for an effect. Read-only ."""
        ...
    @property
    @abstractmethod
    def text_animation(self) -> ITextAnimation:
        """Returns text animation. Read-only ."""
        ...
    @property
    @abstractmethod
    def preset_class_type(self) -> EffectPresetClassType:
        """Defines class of effect. Read/write ."""
        ...
    @preset_class_type.setter
    @abstractmethod
    def preset_class_type(self, value: EffectPresetClassType):
        ...
    @property
    @abstractmethod
    def type(self) -> EffectType:
        """Defines type of effect. Read/write ."""
        ...
    @type.setter
    @abstractmethod
    def type(self, value: EffectType):
        ...
    @property
    @abstractmethod
    def subtype(self) -> EffectSubtype:
        """Defines subtype of effect. Read/write ."""
        ...
    @subtype.setter
    @abstractmethod
    def subtype(self, value: EffectSubtype):
        ...
    @property
    @abstractmethod
    def behaviors(self) -> IBehaviorCollection:
        """Returns collection of behavior for effect. Read/write ."""
        ...
    @behaviors.setter
    @abstractmethod
    def behaviors(self, value: IBehaviorCollection):
        ...
    @property
    @abstractmethod
    def timing(self) -> ITiming:
        """Defines timing value for effect. Read/write ."""
        ...
    @timing.setter
    @abstractmethod
    def timing(self, value: ITiming):
        ...
    @property
    @abstractmethod
    def target_shape(self) -> IShape:
        """Returns target shape for effect. Read-only ."""
        ...
    @property
    @abstractmethod
    def sound(self) -> IAudio:
        """Defined embedded sound for effect. Read/write ."""
        ...
    @sound.setter
    @abstractmethod
    def sound(self, value: IAudio):
        ...
    @property
    @abstractmethod
    def stop_previous_sound(self) -> bool:
        """This attribute specifies if the animation effect stops the previous sound. Read/write ."""
        ...
    @stop_previous_sound.setter
    @abstractmethod
    def stop_previous_sound(self, value: bool):
        ...
    @property
    @abstractmethod
    def after_animation_type(self) -> AfterAnimationType:
        """Defined an after animation type for effect. Read/write ."""
        ...
    @after_animation_type.setter
    @abstractmethod
    def after_animation_type(self, value: AfterAnimationType):
        ...
    @property
    @abstractmethod
    def after_animation_color(self) -> IColorFormat:
        """Defined an after animation color for effect. Read/write ."""
        ...
    @after_animation_color.setter
    @abstractmethod
    def after_animation_color(self, value: IColorFormat):
        ...
    @property
    @abstractmethod
    def animate_text_type(self) -> AnimateTextType:
        """Defines an animate text type for effect. The shape text can be animated by letter, by word or all at once. Read/write ."""
        ...
    @animate_text_type.setter
    @abstractmethod
    def animate_text_type(self, value: AnimateTextType):
        ...
    @property
    @abstractmethod
    def delay_between_text_parts(self) -> float:
        """Defines a delay between animated text parts (words or letters). A positive value specifies the percentage of effect duration. A negative value specifies the delay in seconds. Read/write ."""
        ...
    @delay_between_text_parts.setter
    @abstractmethod
    def delay_between_text_parts(self, value: float):
        ...