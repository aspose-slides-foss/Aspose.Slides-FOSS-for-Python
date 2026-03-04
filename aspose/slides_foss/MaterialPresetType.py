from __future__ import annotations
from enum import Enum

class MaterialPresetType(Enum):
    """Constants which define material of shape."""
    NOT_DEFINED = 'NotDefined'
    CLEAR = 'Clear'
    DK_EDGE = 'DkEdge'
    FLAT = 'Flat'
    LEGACY_MATTE = 'LegacyMatte'
    LEGACY_METAL = 'LegacyMetal'
    LEGACY_PLASTIC = 'LegacyPlastic'
    LEGACY_WIREFRAME = 'LegacyWireframe'
    MATTE = 'Matte'
    METAL = 'Metal'
    PLASTIC = 'Plastic'
    POWDER = 'Powder'
    SOFT_EDGE = 'SoftEdge'
    SOFTMETAL = 'Softmetal'
    TRANSLUCENT_POWDER = 'TranslucentPowder'
    WARM_MATTE = 'WarmMatte'
