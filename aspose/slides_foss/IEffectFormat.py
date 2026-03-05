from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IEffectParamSource import IEffectParamSource

if TYPE_CHECKING:
    from .effects.IBlur import IBlur
    from .effects.IFillOverlay import IFillOverlay
    from .effects.IGlow import IGlow
    from .effects.IInnerShadow import IInnerShadow
    from .effects.IOuterShadow import IOuterShadow
    from .effects.IPresetShadow import IPresetShadow
    from .effects.IReflection import IReflection
    from .effects.ISoftEdge import ISoftEdge

class IEffectFormat(IEffectParamSource, ABC):
    """Represents effect properties of shape."""
    @property
    def is_no_effects(self) -> bool:
        """Returns true if all effects are disabled (as just created, default EffectFormat object). Read-only ."""
        ...

    @property
    def blur_effect(self) -> IBlur:
        """Blur effect. Read/write ."""
        ...

    @blur_effect.setter
    def blur_effect(self, value: IBlur):
        ...

    @property
    def fill_overlay_effect(self) -> IFillOverlay:
        """Fill overlay effect. Read/write ."""
        ...

    @fill_overlay_effect.setter
    def fill_overlay_effect(self, value: IFillOverlay):
        ...

    @property
    def glow_effect(self) -> IGlow:
        """Glow effect. Read/write ."""
        ...

    @glow_effect.setter
    def glow_effect(self, value: IGlow):
        ...

    @property
    def inner_shadow_effect(self) -> IInnerShadow:
        """Inner shadow. Read/write ."""
        ...

    @inner_shadow_effect.setter
    def inner_shadow_effect(self, value: IInnerShadow):
        ...

    @property
    def outer_shadow_effect(self) -> IOuterShadow:
        """Outer shadow. Read/write ."""
        ...

    @outer_shadow_effect.setter
    def outer_shadow_effect(self, value: IOuterShadow):
        ...

    @property
    def preset_shadow_effect(self) -> IPresetShadow:
        """Preset shadow. Read/write ."""
        ...

    @preset_shadow_effect.setter
    def preset_shadow_effect(self, value: IPresetShadow):
        ...

    @property
    def reflection_effect(self) -> IReflection:
        """Reflection. Read/write ."""
        ...

    @reflection_effect.setter
    def reflection_effect(self, value: IReflection):
        ...

    @property
    def soft_edge_effect(self) -> ISoftEdge:
        """Soft edge. Read/write ."""
        ...

    @soft_edge_effect.setter
    def soft_edge_effect(self, value: ISoftEdge):
        ...

    @property
    def as_i_effect_param_source(self) -> IEffectParamSource:
        """Allows to get base IEffectParamSource interface. Read-only ."""
        ...
    def set_blur_effect(self, radius, grow) -> None:
        ...
    def enable_fill_overlay_effect(self) -> None:
        ...
    def enable_glow_effect(self) -> None:
        ...
    def enable_inner_shadow_effect(self) -> None:
        ...
    def enable_outer_shadow_effect(self) -> None:
        ...
    def enable_preset_shadow_effect(self) -> None:
        ...
    def enable_reflection_effect(self) -> None:
        ...
    def enable_soft_edge_effect(self) -> None:
        ...
    def disable_blur_effect(self) -> None:
        ...
    def disable_fill_overlay_effect(self) -> None:
        ...
    def disable_glow_effect(self) -> None:
        ...
    def disable_inner_shadow_effect(self) -> None:
        ...
    def disable_outer_shadow_effect(self) -> None:
        ...
    def disable_preset_shadow_effect(self) -> None:
        ...
    def disable_reflection_effect(self) -> None:
        ...
    def disable_soft_edge_effect(self) -> None:
        ...


