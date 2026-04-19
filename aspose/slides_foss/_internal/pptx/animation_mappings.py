"""
Bidirectional mapping tables between Aspose animation enums and OOXML numeric values.

PresetIDs are scoped by presetClass — entrance, emphasis, path, and exit effects
each have their own numbering. The key for reverse lookup is (presetID, presetClass).
"""

from __future__ import annotations

from ...animation.EffectType import EffectType
from ...animation.EffectSubtype import EffectSubtype
from ...animation.EffectPresetClassType import EffectPresetClassType
from ...animation.EffectTriggerType import EffectTriggerType

# ---------------------------------------------------------------------------
# EffectType -> (presetID, presetClass)
# Values verified against PowerPoint output.
# ---------------------------------------------------------------------------

EFFECT_TYPE_TO_PRESET: dict[EffectType, tuple[int, str]] = {
    # --- Entrance effects (presetClass="entr") ---
    EffectType.APPEAR: (1, 'entr'),
    EffectType.FLY: (2, 'entr'),
    EffectType.BLINDS: (3, 'entr'),
    EffectType.BOX: (4, 'entr'),
    EffectType.CHECKERBOARD: (5, 'entr'),
    EffectType.CIRCLE: (6, 'entr'),
    EffectType.CRAWL: (7, 'entr'),
    EffectType.DIAMOND: (8, 'entr'),
    EffectType.DISSOLVE: (9, 'entr'),
    EffectType.FADE: (10, 'entr'),
    EffectType.FLASH_ONCE: (11, 'entr'),
    EffectType.PEEK: (12, 'entr'),
    EffectType.PLUS: (13, 'entr'),
    EffectType.RANDOM_BARS: (14, 'entr'),
    EffectType.SPIRAL: (15, 'entr'),
    EffectType.SPLIT: (16, 'entr'),
    EffectType.STRETCH: (17, 'entr'),
    EffectType.STRIPS: (18, 'entr'),
    EffectType.SWIVEL: (19, 'entr'),
    EffectType.WEDGE: (20, 'entr'),
    EffectType.WHEEL: (21, 'entr'),
    EffectType.WIPE: (22, 'entr'),
    EffectType.ZOOM: (23, 'entr'),
    EffectType.RANDOM_EFFECTS: (24, 'entr'),
    EffectType.BOOMERANG: (25, 'entr'),
    EffectType.BOUNCE: (26, 'entr'),
    EffectType.COLOR_TYPEWRITER: (27, 'entr'),
    EffectType.CREDITS: (28, 'entr'),
    EffectType.EASE_IN_OUT: (29, 'entr'),
    EffectType.FLOAT: (30, 'entr'),
    EffectType.GROW_AND_TURN: (31, 'entr'),
    EffectType.LIGHT_SPEED: (32, 'entr'),
    EffectType.PINWHEEL: (33, 'entr'),
    EffectType.RISE_UP: (34, 'entr'),
    EffectType.SLING: (35, 'entr'),
    EffectType.SWISH: (36, 'entr'),
    EffectType.THREAD: (37, 'entr'),
    EffectType.WHIP: (38, 'entr'),
    EffectType.ASCEND: (42, 'entr'),
    EffectType.CENTER_REVOLVE: (43, 'entr'),
    EffectType.COMPRESS: (44, 'entr'),
    EffectType.DESCEND: (45, 'entr'),
    EffectType.FADED_SWIVEL: (41, 'entr'),
    EffectType.FADED_ZOOM: (53, 'entr'),
    EffectType.EXPAND: (55, 'entr'),
    EffectType.FOLD: (58, 'entr'),
    EffectType.GLIDE: (49, 'entr'),
    EffectType.MAGNIFY: (51, 'entr'),
    EffectType.SPINNER: (46, 'entr'),
    EffectType.UNFOLD: (59, 'entr'),
    EffectType.CURVE_UP_DOWN: (47, 'entr'),
    EffectType.FLIP: (56, 'entr'),
    EffectType.FLOAT_UP: (39, 'entr'),
    EffectType.FLOAT_DOWN: (40, 'entr'),

    # --- Emphasis effects (presetClass="emph") ---
    EffectType.CHANGE_FILL_COLOR: (1, 'emph'),
    EffectType.CHANGE_FONT: (2, 'emph'),
    EffectType.CHANGE_FONT_COLOR: (3, 'emph'),
    EffectType.CHANGE_FONT_SIZE: (4, 'emph'),
    EffectType.CHANGE_FONT_STYLE: (5, 'emph'),
    EffectType.GROW_SHRINK: (6, 'emph'),
    EffectType.CHANGE_LINE_COLOR: (7, 'emph'),
    EffectType.SPIN: (8, 'emph'),
    EffectType.TRANSPARENCY: (9, 'emph'),
    EffectType.BOLD_FLASH: (10, 'emph'),
    EffectType.BLAST: (14, 'emph'),
    EffectType.BOLD_REVEAL: (15, 'emph'),
    EffectType.BRUSH_ON_COLOR: (16, 'emph'),
    EffectType.BRUSH_ON_UNDERLINE: (18, 'emph'),
    EffectType.COLOR_BLEND: (19, 'emph'),
    EffectType.COLOR_WAVE: (20, 'emph'),
    EffectType.COMPLEMENTARY_COLOR: (21, 'emph'),
    EffectType.COMPLEMENTARY_COLOR2: (22, 'emph'),
    EffectType.CONTRASTING_COLOR: (23, 'emph'),
    EffectType.DARKEN: (24, 'emph'),
    EffectType.DESATURATE: (25, 'emph'),
    EffectType.FLASH_BULB: (26, 'emph'),
    EffectType.FLICKER: (27, 'emph'),
    EffectType.GROW_WITH_COLOR: (28, 'emph'),
    EffectType.LIGHTEN: (30, 'emph'),
    EffectType.STYLE_EMPHASIS: (31, 'emph'),
    EffectType.TEETER: (32, 'emph'),
    EffectType.VERTICAL_GROW: (33, 'emph'),
    EffectType.WAVE: (34, 'emph'),
    EffectType.BLINK: (35, 'emph'),
    EffectType.SHIMMER: (36, 'emph'),

    # --- Path effects (presetClass="path") ---
    EffectType.PATH_CIRCLE: (1, 'path'),
    EffectType.PATH_RIGHT_TRIANGLE: (2, 'path'),
    EffectType.PATH_DIAMOND: (3, 'path'),
    EffectType.PATH_HEXAGON: (4, 'path'),
    EffectType.PATH_5_POINT_STAR: (5, 'path'),
    EffectType.PATH_CRESCENT_MOON: (6, 'path'),
    EffectType.PATH_SQUARE: (7, 'path'),
    EffectType.PATH_TRAPEZOID: (8, 'path'),
    EffectType.PATH_HEART: (9, 'path'),
    EffectType.PATH_OCTAGON: (10, 'path'),
    EffectType.PATH_6_POINT_STAR: (11, 'path'),
    EffectType.PATH_FOOTBALL: (12, 'path'),
    EffectType.PATH_EQUAL_TRIANGLE: (13, 'path'),
    EffectType.PATH_PARALLELOGRAM: (14, 'path'),
    EffectType.PATH_PENTAGON: (15, 'path'),
    EffectType.PATH_4_POINT_STAR: (16, 'path'),
    EffectType.PATH_8_POINT_STAR: (17, 'path'),
    EffectType.PATH_TEARDROP: (18, 'path'),
    EffectType.PATH_POINTY_STAR: (19, 'path'),
    EffectType.PATH_CURVED_SQUARE: (20, 'path'),
    EffectType.PATH_CURVED_X: (21, 'path'),
    EffectType.PATH_VERTICAL_FIGURE8: (22, 'path'),
    EffectType.PATH_CURVY_STAR: (23, 'path'),
    EffectType.PATH_LOOPDE_LOOP: (24, 'path'),
    EffectType.PATH_BUZZSAW: (25, 'path'),
    EffectType.PATH_HORIZONTAL_FIGURE8: (26, 'path'),
    EffectType.PATH_PEANUT: (27, 'path'),
    EffectType.PATH_FIGURE_8_FOUR: (28, 'path'),
    EffectType.PATH_NEUTRON: (29, 'path'),
    EffectType.PATH_SWOOSH: (30, 'path'),
    EffectType.PATH_BEAN: (31, 'path'),
    EffectType.PATH_PLUS: (32, 'path'),
    EffectType.PATH_INVERTED_TRIANGLE: (33, 'path'),
    EffectType.PATH_INVERTED_SQUARE: (34, 'path'),
    EffectType.PATH_LEFT: (35, 'path'),
    EffectType.PATH_TURN_RIGHT: (36, 'path'),
    EffectType.PATH_ARC_DOWN: (37, 'path'),
    EffectType.PATH_ZIGZAG: (38, 'path'),
    EffectType.PATH_S_CURVE2: (39, 'path'),
    EffectType.PATH_SINE_WAVE: (40, 'path'),
    EffectType.PATH_BOUNCE_LEFT: (41, 'path'),
    EffectType.PATH_DOWN: (42, 'path'),
    EffectType.PATH_TURN_UP: (43, 'path'),
    EffectType.PATH_ARC_UP: (44, 'path'),
    EffectType.PATH_HEARTBEAT: (45, 'path'),
    EffectType.PATH_SPIRAL_RIGHT: (46, 'path'),
    EffectType.PATH_WAVE: (47, 'path'),
    EffectType.PATH_CURVY_LEFT: (48, 'path'),
    EffectType.PATH_DIAGONAL_DOWN_RIGHT: (49, 'path'),
    EffectType.PATH_TURN_DOWN: (50, 'path'),
    EffectType.PATH_ARC_LEFT: (51, 'path'),
    EffectType.PATH_FUNNEL: (52, 'path'),
    EffectType.PATH_SPRING: (53, 'path'),
    EffectType.PATH_BOUNCE_RIGHT: (54, 'path'),
    EffectType.PATH_SPIRAL_LEFT: (55, 'path'),
    EffectType.PATH_DIAGONAL_UP_RIGHT: (56, 'path'),
    EffectType.PATH_TURN_UP_RIGHT: (57, 'path'),
    EffectType.PATH_ARC_RIGHT: (58, 'path'),
    EffectType.PATH_S_CURVE1: (59, 'path'),
    EffectType.PATH_DECAYING_WAVE: (60, 'path'),
    EffectType.PATH_CURVY_RIGHT: (61, 'path'),
    EffectType.PATH_STAIRS_DOWN: (62, 'path'),
    EffectType.PATH_RIGHT: (63, 'path'),
    EffectType.PATH_UP: (64, 'path'),
    EffectType.PATH_USER: (0, 'path'),

    # --- Media effects ---
    EffectType.MEDIA_PLAY: (1, 'mediacall'),
    EffectType.MEDIA_PAUSE: (2, 'mediacall'),
    EffectType.MEDIA_STOP: (3, 'mediacall'),

    # --- OLE effects ---
    EffectType.OLE_OBJECT_SHOW: (1, 'verb'),
    EffectType.OLE_OBJECT_EDIT: (2, 'verb'),
    EffectType.OLE_OBJECT_OPEN: (3, 'verb'),
}

# Reverse: (presetID, presetClass) -> EffectType
PRESET_TO_EFFECT_TYPE: dict[tuple[int, str], EffectType] = {
    v: k for k, v in EFFECT_TYPE_TO_PRESET.items()
}

# ---------------------------------------------------------------------------
# EffectSubtype <-> OOXML presetSubtype
# ---------------------------------------------------------------------------

EFFECT_SUBTYPE_TO_PRESET_SUBTYPE: dict[EffectSubtype, int] = {
    EffectSubtype.NONE: 0,
    EffectSubtype.ACROSS: 10,
    EffectSubtype.BOTTOM: 4,
    EffectSubtype.BOTTOM_LEFT: 12,
    EffectSubtype.BOTTOM_RIGHT: 3,
    EffectSubtype.CENTER: 16,
    EffectSubtype.CLOCKWISE: 12,
    EffectSubtype.COUNTER_CLOCKWISE: 16,
    EffectSubtype.DOWN: 4,
    EffectSubtype.DOWN_LEFT: 12,
    EffectSubtype.DOWN_RIGHT: 3,
    EffectSubtype.FONT_ALL_CAPS: 5,
    EffectSubtype.FONT_BOLD: 1,
    EffectSubtype.FONT_ITALIC: 2,
    EffectSubtype.FONT_SHADOW: 4,
    EffectSubtype.FONT_STRIKETHROUGH: 6,
    EffectSubtype.FONT_UNDERLINE: 3,
    EffectSubtype.GRADUAL: 9,
    EffectSubtype.GRADUAL_AND_CYCLE_CLOCKWISE: 10,
    EffectSubtype.GRADUAL_AND_CYCLE_COUNTER_CLOCKWISE: 11,
    EffectSubtype.HORIZONTAL: 10,
    EffectSubtype.HORIZONTAL_IN: 26,
    EffectSubtype.HORIZONTAL_OUT: 42,
    EffectSubtype.IN: 16,
    EffectSubtype.IN_BOTTOM: 36,
    EffectSubtype.IN_CENTER: 528,
    EffectSubtype.IN_SLIGHTLY: 528,
    EffectSubtype.INSTANT: 8,
    EffectSubtype.LEFT: 8,
    EffectSubtype.OBJECT_CENTER: 16,
    EffectSubtype.ORDINAL_MASK: 0,
    EffectSubtype.OUT: 32,
    EffectSubtype.OUT_BOTTOM: 36,
    EffectSubtype.OUT_CENTER: 532,
    EffectSubtype.OUT_SLIGHTLY: 532,
    EffectSubtype.RIGHT: 2,
    EffectSubtype.SLIGHTLY: 528,
    EffectSubtype.SLIDE_CENTER: 16,
    EffectSubtype.TOP: 1,
    EffectSubtype.TOP_LEFT: 6,
    EffectSubtype.TOP_RIGHT: 9,
    EffectSubtype.UP: 1,
    EffectSubtype.UP_LEFT: 6,
    EffectSubtype.UP_RIGHT: 9,
    EffectSubtype.VERTICAL: 5,
    EffectSubtype.VERTICAL_IN: 21,
    EffectSubtype.VERTICAL_OUT: 37,
    EffectSubtype.WHEEL1: 1,
    EffectSubtype.WHEEL2: 2,
    EffectSubtype.WHEEL3: 3,
    EffectSubtype.WHEEL4: 4,
    EffectSubtype.WHEEL8: 8,
}

PRESET_SUBTYPE_TO_EFFECT_SUBTYPE: dict[int, EffectSubtype] = {
    0: EffectSubtype.NONE,
    1: EffectSubtype.TOP,
    2: EffectSubtype.RIGHT,
    3: EffectSubtype.BOTTOM_RIGHT,
    4: EffectSubtype.BOTTOM,
    5: EffectSubtype.VERTICAL,
    6: EffectSubtype.TOP_LEFT,
    8: EffectSubtype.LEFT,
    9: EffectSubtype.TOP_RIGHT,
    10: EffectSubtype.HORIZONTAL,
    12: EffectSubtype.BOTTOM_LEFT,
    16: EffectSubtype.IN,
    21: EffectSubtype.VERTICAL_IN,
    26: EffectSubtype.HORIZONTAL_IN,
    32: EffectSubtype.OUT,
    36: EffectSubtype.OUT_BOTTOM,
    37: EffectSubtype.VERTICAL_OUT,
    42: EffectSubtype.HORIZONTAL_OUT,
    528: EffectSubtype.IN_SLIGHTLY,
    532: EffectSubtype.OUT_SLIGHTLY,
}

# ---------------------------------------------------------------------------
# EffectPresetClassType <-> OOXML presetClass string
# ---------------------------------------------------------------------------

PRESET_CLASS_MAP: dict[str, EffectPresetClassType] = {
    'entr': EffectPresetClassType.ENTRANCE,
    'exit': EffectPresetClassType.EXIT,
    'emph': EffectPresetClassType.EMPHASIS,
    'path': EffectPresetClassType.PATH,
    'mediacall': EffectPresetClassType.MEDIA_CALL,
    'verb': EffectPresetClassType.OLE_ACTION_VERBS,
}

PRESET_CLASS_MAP_REV: dict[EffectPresetClassType, str] = {
    v: k for k, v in PRESET_CLASS_MAP.items()
}

# ---------------------------------------------------------------------------
# EffectTriggerType <-> OOXML nodeType string
# ---------------------------------------------------------------------------

NODE_TYPE_TO_TRIGGER: dict[str, EffectTriggerType] = {
    'clickEffect': EffectTriggerType.ON_CLICK,
    'withEffect': EffectTriggerType.WITH_PREVIOUS,
    'afterEffect': EffectTriggerType.AFTER_PREVIOUS,
}

TRIGGER_TO_NODE_TYPE: dict[EffectTriggerType, str] = {
    v: k for k, v in NODE_TYPE_TO_TRIGGER.items()
}


def infer_preset_class(effect_type: EffectType) -> EffectPresetClassType:
    """Infer the preset class from the effect type mapping."""
    entry = EFFECT_TYPE_TO_PRESET.get(effect_type)
    if entry is not None:
        return PRESET_CLASS_MAP.get(entry[1], EffectPresetClassType.ENTRANCE)
    return EffectPresetClassType.ENTRANCE
