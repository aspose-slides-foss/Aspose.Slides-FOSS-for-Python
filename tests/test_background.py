"""Tests for slide background: solid, gradient, pattern, picture fills + effective data."""
from aspose.slides_foss import (
    Presentation, BackgroundType, FillType,
    GradientShape, PatternStyle, PictureFillMode, TileFlip,
)
from aspose.slides_foss.drawing import Color

from conftest import create_test_png


# ------------------------------------------------------------------
# Solid background
# ------------------------------------------------------------------

def test_solid_background_on_slide(tmp_pptx):
    """Solid-colour background on a normal slide round-trips."""
    pres = Presentation()
    slide = pres.slides[0]
    slide.background.type = BackgroundType.OWN_BACKGROUND
    slide.background.fill_format.fill_type = FillType.SOLID
    slide.background.fill_format.solid_fill_color.color = Color.blue

    pres2 = tmp_pptx(pres)
    bg = pres2.slides[0].background
    assert bg.type == BackgroundType.OWN_BACKGROUND
    assert bg.fill_format.fill_type == FillType.SOLID
    c = bg.fill_format.solid_fill_color.color
    assert c.r == 0 and c.g == 0 and c.b == 255
    pres2.dispose()


def test_solid_background_on_master(tmp_pptx):
    """Solid-colour background on master slide round-trips."""
    pres = Presentation()
    master = pres.masters[0]
    master.background.type = BackgroundType.OWN_BACKGROUND
    master.background.fill_format.fill_type = FillType.SOLID
    master.background.fill_format.solid_fill_color.color = Color.forest_green

    pres2 = tmp_pptx(pres)
    bg = pres2.masters[0].background
    assert bg.type == BackgroundType.OWN_BACKGROUND
    assert bg.fill_format.fill_type == FillType.SOLID
    c = bg.fill_format.solid_fill_color.color
    assert c.r == 34 and c.g == 139 and c.b == 34
    pres2.dispose()


def test_solid_background_on_layout(tmp_pptx):
    """Solid-colour background on layout slide round-trips."""
    pres = Presentation()
    layout = pres.slides[0].layout_slide
    layout.background.type = BackgroundType.OWN_BACKGROUND
    layout.background.fill_format.fill_type = FillType.SOLID
    layout.background.fill_format.solid_fill_color.color = Color.coral

    pres2 = tmp_pptx(pres)
    bg = pres2.slides[0].layout_slide.background
    assert bg.type == BackgroundType.OWN_BACKGROUND
    assert bg.fill_format.fill_type == FillType.SOLID
    c = bg.fill_format.solid_fill_color.color
    assert c.r == 255 and c.g == 127 and c.b == 80
    pres2.dispose()


# ------------------------------------------------------------------
# Gradient background
# ------------------------------------------------------------------

def test_gradient_background(tmp_pptx):
    """Gradient background with tile flip round-trips."""
    pres = Presentation()
    slide = pres.slides[0]
    slide.background.type = BackgroundType.OWN_BACKGROUND
    slide.background.fill_format.fill_type = FillType.GRADIENT
    slide.background.fill_format.gradient_format.tile_flip = TileFlip.FLIP_BOTH

    pres2 = tmp_pptx(pres)
    bg = pres2.slides[0].background
    assert bg.type == BackgroundType.OWN_BACKGROUND
    assert bg.fill_format.fill_type == FillType.GRADIENT
    assert bg.fill_format.gradient_format.tile_flip == TileFlip.FLIP_BOTH
    pres2.dispose()


def test_gradient_background_with_stops(tmp_pptx):
    """Gradient background with colour stops round-trips."""
    pres = Presentation()
    slide = pres.slides[0]
    slide.background.type = BackgroundType.OWN_BACKGROUND
    slide.background.fill_format.fill_type = FillType.GRADIENT
    gf = slide.background.fill_format.gradient_format
    gf.gradient_shape = GradientShape.LINEAR
    gf.linear_gradient_angle = 90
    gf.gradient_stops.add(0.0, Color.red)
    gf.gradient_stops.add(1.0, Color.blue)

    pres2 = tmp_pptx(pres)
    bg = pres2.slides[0].background
    assert bg.fill_format.fill_type == FillType.GRADIENT
    stops = bg.fill_format.gradient_format.gradient_stops
    assert len(stops) >= 2
    pres2.dispose()


# ------------------------------------------------------------------
# Pattern background
# ------------------------------------------------------------------

def test_pattern_background(tmp_pptx):
    """Pattern background round-trips."""
    pres = Presentation()
    slide = pres.slides[0]
    slide.background.type = BackgroundType.OWN_BACKGROUND
    slide.background.fill_format.fill_type = FillType.PATTERN
    pf = slide.background.fill_format.pattern_format
    pf.pattern_style = PatternStyle.PERCENT50
    pf.fore_color.color = Color.dark_blue
    pf.back_color.color = Color.white

    pres2 = tmp_pptx(pres)
    bg = pres2.slides[0].background
    assert bg.type == BackgroundType.OWN_BACKGROUND
    assert bg.fill_format.fill_type == FillType.PATTERN
    assert bg.fill_format.pattern_format.pattern_style == PatternStyle.PERCENT50
    pres2.dispose()


# ------------------------------------------------------------------
# Picture background
# ------------------------------------------------------------------

def test_picture_background_stretch(tmp_pptx):
    """Picture background in stretch mode round-trips."""
    pres = Presentation()
    slide = pres.slides[0]

    slide.background.type = BackgroundType.OWN_BACKGROUND
    slide.background.fill_format.fill_type = FillType.PICTURE
    slide.background.fill_format.picture_fill_format.picture_fill_mode = PictureFillMode.STRETCH

    png_bytes = create_test_png(0, 128, 0)
    pp_image = pres.images.add_image(png_bytes)
    slide.background.fill_format.picture_fill_format.picture.image = pp_image

    pres2 = tmp_pptx(pres)
    bg = pres2.slides[0].background
    assert bg.type == BackgroundType.OWN_BACKGROUND
    assert bg.fill_format.fill_type == FillType.PICTURE
    assert bg.fill_format.picture_fill_format.picture_fill_mode == PictureFillMode.STRETCH
    pres2.dispose()


def test_picture_background_tile(tmp_pptx):
    """Picture background in tile mode round-trips."""
    pres = Presentation()
    slide = pres.slides[0]

    slide.background.type = BackgroundType.OWN_BACKGROUND
    slide.background.fill_format.fill_type = FillType.PICTURE

    png_bytes = create_test_png(255, 0, 0)
    pp_image = pres.images.add_image(png_bytes)
    pff = slide.background.fill_format.picture_fill_format
    pff.picture.image = pp_image
    pff.picture_fill_mode = PictureFillMode.TILE

    pres2 = tmp_pptx(pres)
    bg = pres2.slides[0].background
    assert bg.fill_format.fill_type == FillType.PICTURE
    assert bg.fill_format.picture_fill_format.picture_fill_mode == PictureFillMode.TILE
    pres2.dispose()


# ------------------------------------------------------------------
# Themed background
# ------------------------------------------------------------------

def test_themed_background(tmp_pptx):
    """Themed background type and style_index round-trip."""
    pres = Presentation()
    slide = pres.slides[0]
    slide.background.type = BackgroundType.THEMED
    slide.background.style_index = 3

    pres2 = tmp_pptx(pres)
    bg = pres2.slides[0].background
    assert bg.type == BackgroundType.THEMED
    assert bg.style_index == 3
    pres2.dispose()


# ------------------------------------------------------------------
# Background type transitions
# ------------------------------------------------------------------

def test_change_background_type(tmp_pptx):
    """Changing background type clears previous data."""
    pres = Presentation()
    slide = pres.slides[0]

    # Start with solid
    slide.background.type = BackgroundType.OWN_BACKGROUND
    slide.background.fill_format.fill_type = FillType.SOLID
    slide.background.fill_format.solid_fill_color.color = Color.red
    assert slide.background.type == BackgroundType.OWN_BACKGROUND

    # Switch to themed
    slide.background.type = BackgroundType.THEMED
    assert slide.background.type == BackgroundType.THEMED
    slide.background.style_index = 5

    pres2 = tmp_pptx(pres)
    bg = pres2.slides[0].background
    assert bg.type == BackgroundType.THEMED
    assert bg.style_index == 5
    pres2.dispose()


def test_clear_background(tmp_pptx):
    """Setting NOT_DEFINED removes the background element."""
    pres = Presentation()
    slide = pres.slides[0]
    slide.background.type = BackgroundType.OWN_BACKGROUND
    slide.background.fill_format.fill_type = FillType.SOLID
    slide.background.fill_format.solid_fill_color.color = Color.red

    # Now clear it
    slide.background.type = BackgroundType.NOT_DEFINED

    pres2 = tmp_pptx(pres)
    assert pres2.slides[0].background.type == BackgroundType.NOT_DEFINED
    pres2.dispose()


# ------------------------------------------------------------------
# Effective background
# ------------------------------------------------------------------

def test_effective_own_background():
    """get_effective returns fill data for OWN_BACKGROUND slide."""
    pres = Presentation()
    slide = pres.slides[0]
    slide.background.type = BackgroundType.OWN_BACKGROUND
    slide.background.fill_format.fill_type = FillType.SOLID
    slide.background.fill_format.solid_fill_color.color = Color.coral

    eff = slide.background.get_effective()
    assert eff.fill_format.fill_type == FillType.SOLID
    c = eff.fill_format.solid_fill_color
    assert c.r == 255 and c.g == 127 and c.b == 80
    pres.dispose()


def test_effective_inherits_from_master():
    """Slide with NOT_DEFINED bg inherits from master."""
    pres = Presentation()
    master = pres.masters[0]
    master.background.type = BackgroundType.OWN_BACKGROUND
    master.background.fill_format.fill_type = FillType.SOLID
    master.background.fill_format.solid_fill_color.color = Color.dark_green

    slide = pres.slides[0]
    assert slide.background.type == BackgroundType.NOT_DEFINED

    eff = slide.background.get_effective()
    assert eff.fill_format.fill_type == FillType.SOLID
    c = eff.fill_format.solid_fill_color
    assert c.r == 0 and c.g == 100 and c.b == 0
    pres.dispose()


def test_effective_inherits_from_layout():
    """Slide with NOT_DEFINED bg inherits from layout before master."""
    pres = Presentation()

    # Set master to blue
    master = pres.masters[0]
    master.background.type = BackgroundType.OWN_BACKGROUND
    master.background.fill_format.fill_type = FillType.SOLID
    master.background.fill_format.solid_fill_color.color = Color.blue

    # Set layout to red — should take priority
    layout = pres.slides[0].layout_slide
    layout.background.type = BackgroundType.OWN_BACKGROUND
    layout.background.fill_format.fill_type = FillType.SOLID
    layout.background.fill_format.solid_fill_color.color = Color.red

    eff = pres.slides[0].background.get_effective()
    assert eff.fill_format.fill_type == FillType.SOLID
    c = eff.fill_format.solid_fill_color
    assert c.r == 255 and c.g == 0 and c.b == 0
    pres.dispose()


# ------------------------------------------------------------------
# Multiple slides
# ------------------------------------------------------------------

def test_different_backgrounds_per_slide(tmp_pptx):
    """Each slide can have its own independent background."""
    pres = Presentation()
    # Add a second slide
    pres.slides.add_empty_slide(pres.slides[0].layout_slide)

    slide1 = pres.slides[0]
    slide1.background.type = BackgroundType.OWN_BACKGROUND
    slide1.background.fill_format.fill_type = FillType.SOLID
    slide1.background.fill_format.solid_fill_color.color = Color.red

    slide2 = pres.slides[1]
    slide2.background.type = BackgroundType.OWN_BACKGROUND
    slide2.background.fill_format.fill_type = FillType.SOLID
    slide2.background.fill_format.solid_fill_color.color = Color.blue

    pres2 = tmp_pptx(pres)
    c1 = pres2.slides[0].background.fill_format.solid_fill_color.color
    c2 = pres2.slides[1].background.fill_format.solid_fill_color.color
    assert c1.r == 255 and c1.b == 0  # red
    assert c2.r == 0 and c2.b == 255  # blue
    pres2.dispose()
