from __future__ import annotations
from enum import Enum

class PresetShadowType(Enum):
    """Represents a preset for a shadow effect."""
    TOP_LEFT_DROP_SHADOW = 'TopLeftDropShadow'  # Represents Top Left Drop Shadow.
    TOP_LEFT_LARGE_DROP_SHADOW = 'TopLeftLargeDropShadow'  # Represents Top Left Large Drop Shadow.
    BACK_LEFT_LONG_PERSPECTIVE_SHADOW = 'BackLeftLongPerspectiveShadow'  # Represents Back Left Long Perspective Shadow
    BACK_RIGHT_LONG_PERSPECTIVE_SHADOW = 'BackRightLongPerspectiveShadow'  # Represents Back Right Long Perspective Shadow
    TOP_LEFT_DOUBLE_DROP_SHADOW = 'TopLeftDoubleDropShadow'  # Represents Top Left Double Drop Shadow.
    BOTTOM_RIGHT_SMALL_DROP_SHADOW = 'BottomRightSmallDropShadow'  # Represents Bottom Right Small Drop Shadow.
    FRONT_LEFT_LONG_PERSPECTIVE_SHADOW = 'FrontLeftLongPerspectiveShadow'  # Represents Front Left Long Perspective Shadow.
    FRONT_RIGHT_LONG_PERSPECTIVE_SHADOW = 'FrontRightLongPerspectiveShadow'  # Represents Front Right Long Perspective Shadow.
    OUTER_BOX_SHADOW_3D = 'OuterBoxShadow3D'  # Represents Outer Box Shadow 3D.
    INNER_BOX_SHADOW_3D = 'InnerBoxShadow3D'  # Represents Inner Box Shadow 3D.
    BACK_CENTER_PERSPECTIVE_SHADOW = 'BackCenterPerspectiveShadow'  # Represents Back Center Perspective Shadow.
    TOP_RIGHT_DROP_SHADOW = 'TopRightDropShadow'  # Represents Top Right Drop Shadow.
    FRONT_BOTTOM_SHADOW = 'FrontBottomShadow'  # Represents Front Bottom Shadow.
    BACK_LEFT_PERSPECTIVE_SHADOW = 'BackLeftPerspectiveShadow'  # Represents Back Left Perspective Shadow.
    BACK_RIGHT_PERSPECTIVE_SHADOW = 'BackRightPerspectiveShadow'  # Represents Back Right Perspective Shadow.
    BOTTOM_LEFT_DROP_SHADOW = 'BottomLeftDropShadow'  # Represents Bottom Left Drop Shadow.
    BOTTOM_RIGHT_DROP_SHADOW = 'BottomRightDropShadow'  # Represents Bottom Right Drop Shadow.
    FRONT_LEFT_PERSPECTIVE_SHADOW = 'FrontLeftPerspectiveShadow'  # Represents Front Left Perspective Shadow.
    FRONT_RIGHT_PERSPECTIVE_SHADOW = 'FrontRightPerspectiveShadow'  # Represents Front Right Perspective Shadow.
    TOP_LEFT_SMALL_DROP_SHADOW = 'TopLeftSmallDropShadow'  # Represents Top Left Small Drop Shadow.
