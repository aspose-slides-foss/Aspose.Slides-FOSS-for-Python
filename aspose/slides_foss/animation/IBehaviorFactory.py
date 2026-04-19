from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IColorEffect import IColorEffect
    from .ICommandEffect import ICommandEffect
    from .IFilterEffect import IFilterEffect
    from .IMotionEffect import IMotionEffect
    from .IPropertyEffect import IPropertyEffect
    from .IRotationEffect import IRotationEffect
    from .IScaleEffect import IScaleEffect
    from .ISetEffect import ISetEffect

class IBehaviorFactory(ABC):
    """Allows to create animation effects"""
    @abstractmethod
    def create_color_effect(self) -> IColorEffect:
        ...
    @abstractmethod
    def create_command_effect(self) -> ICommandEffect:
        ...
    @abstractmethod
    def create_filter_effect(self) -> IFilterEffect:
        ...
    @abstractmethod
    def create_motion_effect(self) -> IMotionEffect:
        ...
    @abstractmethod
    def create_property_effect(self) -> IPropertyEffect:
        ...
    @abstractmethod
    def create_rotation_effect(self) -> IRotationEffect:
        ...
    @abstractmethod
    def create_scale_effect(self) -> IScaleEffect:
        ...
    @abstractmethod
    def create_set_effect(self) -> ISetEffect:
        ...