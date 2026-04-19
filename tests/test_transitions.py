"""Tests for slide transition functionality."""
import pytest

from aspose.slides_foss import Presentation, ShapeType
from aspose.slides_foss.export import SaveFormat
from aspose.slides_foss.slideshow import (
    TransitionType,
    TransitionSpeed,
    TransitionMorphType,
    TransitionInOutDirectionType,
    TransitionSideDirectionType,
    TransitionEightDirectionType,
    TransitionCornerDirectionType,
    TransitionCornerAndCenterDirectionType,
    TransitionLeftRightDirectionType,
    TransitionPattern,
    TransitionShredPattern,
    EmptyTransition,
    OptionalBlackTransition,
    SideDirectionTransition,
    EightDirectionTransition,
    CornerDirectionTransition,
    OrientationTransition,
    InOutTransition,
    SplitTransition,
    WheelTransition,
    MorphTransition,
    GlitterTransition,
    FlyThroughTransition,
    ShredTransition,
    RevealTransition,
    RippleTransition,
    LeftRightDirectionTransition,
)
from aspose.slides_foss.Orientation import Orientation


# ---- Basic transition type and round-trip ----

class TestTransitionType:
    """Test setting and reading transition types."""

    def test_default_is_none(self):
        pres = Presentation()
        slide = pres.slides[0]
        assert slide.slide_show_transition.type == TransitionType.NONE
        pres.dispose()

    def test_set_circle(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.CIRCLE
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.type == TransitionType.CIRCLE
        assert isinstance(pres2.slides[0].slide_show_transition.value, EmptyTransition)
        pres2.dispose()

    def test_set_dissolve(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.DISSOLVE
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.type == TransitionType.DISSOLVE
        pres2.dispose()

    def test_set_none_clears_transition(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.CIRCLE
        pres.slides[0].slide_show_transition.type = TransitionType.NONE
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.type == TransitionType.NONE
        assert pres2.slides[0].slide_show_transition.value is None
        pres2.dispose()

    def test_change_type_replaces_value(self):
        pres = Presentation()
        slide = pres.slides[0]
        slide.slide_show_transition.type = TransitionType.FADE
        assert isinstance(slide.slide_show_transition.value, OptionalBlackTransition)
        slide.slide_show_transition.type = TransitionType.WIPE
        assert isinstance(slide.slide_show_transition.value, SideDirectionTransition)
        pres.dispose()


# ---- Timing properties ----

class TestTransitionTiming:
    """Test advance_on_click, advance_after, advance_after_time, speed, duration."""

    def test_advance_on_click_default(self):
        pres = Presentation()
        assert pres.slides[0].slide_show_transition.advance_on_click is True
        pres.dispose()

    def test_advance_on_click_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.FADE
        pres.slides[0].slide_show_transition.advance_on_click = False
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.advance_on_click is False
        pres2.dispose()

    def test_advance_after_time_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.COMB
        pres.slides[0].slide_show_transition.advance_after_time = 5000
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.advance_after_time == 5000
        assert pres2.slides[0].slide_show_transition.advance_after is True
        pres2.dispose()

    def test_advance_after_flag(self, tmp_pptx):
        pres = Presentation()
        t = pres.slides[0].slide_show_transition
        assert t.advance_after is False
        t.advance_after = True
        assert t.advance_after is True
        t.advance_after = False
        assert t.advance_after is False
        pres.dispose()

    def test_speed_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.FADE
        pres.slides[0].slide_show_transition.speed = TransitionSpeed.SLOW
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.speed == TransitionSpeed.SLOW
        pres2.dispose()

    def test_speed_default_is_fast(self):
        pres = Presentation()
        assert pres.slides[0].slide_show_transition.speed == TransitionSpeed.FAST
        pres.dispose()


# ---- Standard transition value types ----

class TestOptionalBlackTransition:
    """Test Cut and Fade transitions with from_black property."""

    def test_fade_from_black_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.FADE
        pres.slides[0].slide_show_transition.value.from_black = True
        pres2 = tmp_pptx(pres)
        val = pres2.slides[0].slide_show_transition.value
        assert isinstance(val, OptionalBlackTransition)
        assert val.from_black is True
        pres2.dispose()

    def test_cut_from_black_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.CUT
        pres.slides[0].slide_show_transition.value.from_black = True
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.value.from_black is True
        pres2.dispose()

    def test_from_black_default_false(self):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.FADE
        assert pres.slides[0].slide_show_transition.value.from_black is False
        pres.dispose()


class TestSideDirectionTransition:
    """Test Push and Wipe transitions with side direction."""

    def test_push_direction_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.PUSH
        pres.slides[0].slide_show_transition.value.direction = TransitionSideDirectionType.RIGHT
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.value.direction == TransitionSideDirectionType.RIGHT
        pres2.dispose()

    def test_wipe_direction_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.WIPE
        pres.slides[0].slide_show_transition.value.direction = TransitionSideDirectionType.UP
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.value.direction == TransitionSideDirectionType.UP
        pres2.dispose()


class TestEightDirectionTransition:
    """Test Cover and Pull transitions with eight directions."""

    def test_cover_direction_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.COVER
        pres.slides[0].slide_show_transition.value.direction = TransitionEightDirectionType.RIGHT_UP
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.value.direction == TransitionEightDirectionType.RIGHT_UP
        pres2.dispose()


class TestCornerDirectionTransition:
    """Test Strips transition with corner directions."""

    def test_strips_direction_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.STRIPS
        pres.slides[0].slide_show_transition.value.direction = TransitionCornerDirectionType.RIGHT_DOWN
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.value.direction == TransitionCornerDirectionType.RIGHT_DOWN
        pres2.dispose()


class TestOrientationTransition:
    """Test Blinds, Checker, Comb, RandomBar transitions with orientation."""

    def test_blinds_vertical_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.BLINDS
        pres.slides[0].slide_show_transition.value.direction = Orientation.VERTICAL
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.value.direction == Orientation.VERTICAL
        pres2.dispose()

    def test_checker_horizontal_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.CHECKER
        pres.slides[0].slide_show_transition.value.direction = Orientation.HORIZONTAL
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.value.direction == Orientation.HORIZONTAL
        pres2.dispose()


class TestInOutTransition:
    """Test Zoom transition with in/out direction."""

    def test_zoom_out_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.ZOOM
        pres.slides[0].slide_show_transition.value.direction = TransitionInOutDirectionType.OUT
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.value.direction == TransitionInOutDirectionType.OUT
        pres2.dispose()


class TestSplitTransition:
    """Test Split transition with direction and orientation."""

    def test_split_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.SPLIT
        val = pres.slides[0].slide_show_transition.value
        val.direction = TransitionInOutDirectionType.IN
        val.orientation = Orientation.VERTICAL
        pres2 = tmp_pptx(pres)
        val2 = pres2.slides[0].slide_show_transition.value
        assert isinstance(val2, SplitTransition)
        assert val2.direction == TransitionInOutDirectionType.IN
        assert val2.orientation == Orientation.VERTICAL
        pres2.dispose()


class TestWheelTransition:
    """Test Wheel transition with spokes property."""

    def test_wheel_spokes_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.WHEEL
        pres.slides[0].slide_show_transition.value.spokes = 8
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.value.spokes == 8
        pres2.dispose()

    def test_wheel_default_spokes_is_4(self):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.WHEEL
        assert pres.slides[0].slide_show_transition.value.spokes == 4
        pres.dispose()


class TestMorphTransition:
    """Test Morph transition with morph_type property."""

    def test_morph_by_word_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.MORPH
        pres.slides[0].slide_show_transition.value.morph_type = TransitionMorphType.BY_WORD
        pres2 = tmp_pptx(pres)
        val = pres2.slides[0].slide_show_transition.value
        assert isinstance(val, MorphTransition)
        assert val.morph_type == TransitionMorphType.BY_WORD
        pres2.dispose()

    def test_morph_by_char(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.MORPH
        pres.slides[0].slide_show_transition.value.morph_type = TransitionMorphType.BY_CHAR
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.value.morph_type == TransitionMorphType.BY_CHAR
        pres2.dispose()


# ---- P14 (PowerPoint 2010+) transitions ----

class TestP14Transitions:
    """Test PowerPoint 2010+ transition types."""

    def test_vortex_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.VORTEX
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.type == TransitionType.VORTEX
        assert isinstance(pres2.slides[0].slide_show_transition.value, SideDirectionTransition)
        pres2.dispose()

    def test_honeycomb_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.HONEYCOMB
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.type == TransitionType.HONEYCOMB
        pres2.dispose()

    def test_ripple_direction_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.RIPPLE
        pres.slides[0].slide_show_transition.value.direction = TransitionCornerAndCenterDirectionType.LEFT_UP
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.value.direction == TransitionCornerAndCenterDirectionType.LEFT_UP
        pres2.dispose()

    def test_glitter_pattern_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.GLITTER
        pres.slides[0].slide_show_transition.value.pattern = TransitionPattern.HEXAGON
        pres.slides[0].slide_show_transition.value.direction = TransitionSideDirectionType.DOWN
        pres2 = tmp_pptx(pres)
        val = pres2.slides[0].slide_show_transition.value
        assert isinstance(val, GlitterTransition)
        assert val.pattern == TransitionPattern.HEXAGON
        assert val.direction == TransitionSideDirectionType.DOWN
        pres2.dispose()

    def test_flythrough_bounce_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.FLYTHROUGH
        pres.slides[0].slide_show_transition.value.has_bounce = True
        pres.slides[0].slide_show_transition.value.direction = TransitionInOutDirectionType.OUT
        pres2 = tmp_pptx(pres)
        val = pres2.slides[0].slide_show_transition.value
        assert isinstance(val, FlyThroughTransition)
        assert val.has_bounce is True
        assert val.direction == TransitionInOutDirectionType.OUT
        pres2.dispose()

    def test_shred_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.SHRED
        pres.slides[0].slide_show_transition.value.pattern = TransitionShredPattern.RECTANGLE
        pres.slides[0].slide_show_transition.value.direction = TransitionInOutDirectionType.OUT
        pres2 = tmp_pptx(pres)
        val = pres2.slides[0].slide_show_transition.value
        assert isinstance(val, ShredTransition)
        assert val.pattern == TransitionShredPattern.RECTANGLE
        assert val.direction == TransitionInOutDirectionType.OUT
        pres2.dispose()

    def test_reveal_through_black_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.REVEAL
        pres.slides[0].slide_show_transition.value.through_black = True
        pres.slides[0].slide_show_transition.value.direction = TransitionLeftRightDirectionType.RIGHT
        pres2 = tmp_pptx(pres)
        val = pres2.slides[0].slide_show_transition.value
        assert isinstance(val, RevealTransition)
        assert val.through_black is True
        assert val.direction == TransitionLeftRightDirectionType.RIGHT
        pres2.dispose()

    def test_switch_direction_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.SWITCH
        pres.slides[0].slide_show_transition.value.direction = TransitionLeftRightDirectionType.RIGHT
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.value.direction == TransitionLeftRightDirectionType.RIGHT
        pres2.dispose()

    def test_flash_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.FLASH
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.type == TransitionType.FLASH
        pres2.dispose()

    def test_doors_orientation_round_trip(self, tmp_pptx):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = TransitionType.DOORS
        pres.slides[0].slide_show_transition.value.direction = Orientation.VERTICAL
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.value.direction == Orientation.VERTICAL
        pres2.dispose()


# ---- P15 (PowerPoint 2013+) preset transitions ----

class TestP15Transitions:
    """Test PowerPoint 2013+ preset transition types."""

    @pytest.mark.parametrize("ttype", [
        TransitionType.FALL_OVER,
        TransitionType.DRAPE,
        TransitionType.CURTAINS,
        TransitionType.WIND,
        TransitionType.PRESTIGE,
        TransitionType.FRACTURE,
        TransitionType.CRUSH,
        TransitionType.PEEL_OFF,
        TransitionType.PAGE_CURL_DOUBLE,
        TransitionType.PAGE_CURL_SINGLE,
        TransitionType.AIRPLANE,
        TransitionType.ORIGAMI,
    ])
    def test_p15_preset_round_trip(self, tmp_pptx, ttype):
        pres = Presentation()
        pres.slides[0].slide_show_transition.type = ttype
        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.type == ttype
        pres2.dispose()


# ---- Multiple slides ----

class TestMultipleSlides:
    """Test transitions on multiple slides in the same presentation."""

    def test_different_transitions_per_slide(self, tmp_pptx):
        pres = Presentation()
        layout = pres.slides[0].layout_slide

        pres.slides[0].slide_show_transition.type = TransitionType.CIRCLE
        pres.slides[0].slide_show_transition.advance_after_time = 3000

        s1 = pres.slides.add_empty_slide(layout)
        s1.slide_show_transition.type = TransitionType.COMB
        s1.slide_show_transition.advance_after_time = 5000

        s2 = pres.slides.add_empty_slide(layout)
        s2.slide_show_transition.type = TransitionType.ZOOM
        s2.slide_show_transition.advance_after_time = 7000

        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].slide_show_transition.type == TransitionType.CIRCLE
        assert pres2.slides[0].slide_show_transition.advance_after_time == 3000
        assert pres2.slides[1].slide_show_transition.type == TransitionType.COMB
        assert pres2.slides[1].slide_show_transition.advance_after_time == 5000
        assert pres2.slides[2].slide_show_transition.type == TransitionType.ZOOM
        assert pres2.slides[2].slide_show_transition.advance_after_time == 7000
        pres2.dispose()
