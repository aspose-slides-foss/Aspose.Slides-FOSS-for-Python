from __future__ import annotations
from .IBehaviorFactory import IBehaviorFactory
from .IColorEffect import IColorEffect
from .ICommandEffect import ICommandEffect
from .IFilterEffect import IFilterEffect
from .IMotionEffect import IMotionEffect
from .IPropertyEffect import IPropertyEffect
from .IRotationEffect import IRotationEffect
from .IScaleEffect import IScaleEffect
from .ISetEffect import ISetEffect


class BehaviorFactory(IBehaviorFactory):
    """Factory for creating behavior effect instances."""

    def __init__(self):
        ...

    def create_color_effect(self) -> IColorEffect:
        from .ColorEffect import ColorEffect
        return ColorEffect()

    def create_command_effect(self) -> ICommandEffect:
        from .CommandEffect import CommandEffect
        return CommandEffect()

    def create_filter_effect(self) -> IFilterEffect:
        from .FilterEffect import FilterEffect
        return FilterEffect()

    def create_motion_effect(self) -> IMotionEffect:
        from .MotionEffect import MotionEffect
        return MotionEffect()

    def create_property_effect(self) -> IPropertyEffect:
        from .PropertyEffect import PropertyEffect
        return PropertyEffect()

    def create_rotation_effect(self) -> IRotationEffect:
        from .RotationEffect import RotationEffect
        return RotationEffect()

    def create_scale_effect(self) -> IScaleEffect:
        from .ScaleEffect import ScaleEffect
        return ScaleEffect()

    def create_set_effect(self) -> ISetEffect:
        from .SetEffect import SetEffect
        return SetEffect()
