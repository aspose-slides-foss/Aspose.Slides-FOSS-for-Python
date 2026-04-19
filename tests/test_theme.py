"""Tests for presentation theme: color scheme, font scheme, format scheme, theme managers."""
from aspose.slides_foss import Presentation, FillType
from aspose.slides_foss.drawing import Color
from aspose.slides_foss.FontData import FontData


# ------------------------------------------------------------------
# master_theme basic access
# ------------------------------------------------------------------

def test_master_theme_not_none():
    """Presentation.master_theme returns an object."""
    pres = Presentation()
    assert pres.master_theme is not None
    pres.dispose()


def test_master_theme_name():
    """Theme name is readable."""
    pres = Presentation()
    name = pres.master_theme.name
    assert isinstance(name, str) and len(name) > 0
    pres.dispose()


def test_master_theme_name_roundtrip(tmp_pptx):
    """Theme name can be changed and survives save/reload."""
    pres = Presentation()
    pres.master_theme.name = "My Custom Theme"
    pres2 = tmp_pptx(pres)
    assert pres2.master_theme.name == "My Custom Theme"
    pres2.dispose()


# ------------------------------------------------------------------
# Color scheme
# ------------------------------------------------------------------

def test_color_scheme_all_slots():
    """All 12 color scheme slots are accessible."""
    pres = Presentation()
    cs = pres.master_theme.color_scheme
    slots = [
        cs.dark1, cs.light1, cs.dark2, cs.light2,
        cs.accent1, cs.accent2, cs.accent3, cs.accent4,
        cs.accent5, cs.accent6, cs.hyperlink, cs.followed_hyperlink,
    ]
    for slot in slots:
        assert slot is not None
        c = slot.color
        assert hasattr(c, 'r') and hasattr(c, 'g') and hasattr(c, 'b')
    pres.dispose()


def test_color_scheme_template_accent1():
    """Default template accent1 should be a specific color (from Office theme)."""
    pres = Presentation()
    c = pres.master_theme.color_scheme.accent1.color
    # Template Office theme accent1 = #156082
    assert c.r == 0x15 and c.g == 0x60 and c.b == 0x82
    pres.dispose()


def test_color_scheme_modify_accent4_roundtrip(tmp_pptx):
    """Modifying accent4 to red survives save/reload."""
    pres = Presentation()
    pres.master_theme.color_scheme.accent4.color = Color.red
    pres2 = tmp_pptx(pres)
    c = pres2.master_theme.color_scheme.accent4.color
    assert c.r == 255 and c.g == 0 and c.b == 0
    pres2.dispose()


def test_color_scheme_modify_dark2_roundtrip(tmp_pptx):
    """Modifying dark2 to green survives save/reload."""
    pres = Presentation()
    pres.master_theme.color_scheme.dark2.color = Color.green
    pres2 = tmp_pptx(pres)
    c = pres2.master_theme.color_scheme.dark2.color
    assert c.r == 0 and c.g == 128 and c.b == 0
    pres2.dispose()


def test_color_scheme_presentation_ref():
    """ColorScheme.presentation returns the parent Presentation."""
    pres = Presentation()
    cs = pres.master_theme.color_scheme
    assert cs.presentation is pres
    pres.dispose()


# ------------------------------------------------------------------
# Font scheme
# ------------------------------------------------------------------

def test_font_scheme_name():
    """Font scheme name is readable."""
    pres = Presentation()
    name = pres.master_theme.font_scheme.name
    assert isinstance(name, str) and len(name) > 0
    pres.dispose()


def test_font_scheme_major_minor():
    """Major and minor font collections exist with latin fonts."""
    pres = Presentation()
    fs = pres.master_theme.font_scheme
    assert fs.major is not None
    assert fs.minor is not None
    assert fs.major.latin_font is not None
    assert fs.minor.latin_font is not None
    assert len(fs.major.latin_font.font_name) > 0
    assert len(fs.minor.latin_font.font_name) > 0
    pres.dispose()


def test_font_scheme_modify_minor_latin_roundtrip(tmp_pptx):
    """Changing the minor latin font survives save/reload."""
    pres = Presentation()
    pres.master_theme.font_scheme.minor.latin_font = FontData("Arial")
    pres2 = tmp_pptx(pres)
    assert pres2.master_theme.font_scheme.minor.latin_font.font_name == "Arial"
    pres2.dispose()


def test_font_scheme_modify_major_latin_roundtrip(tmp_pptx):
    """Changing the major latin font survives save/reload."""
    pres = Presentation()
    pres.master_theme.font_scheme.major.latin_font = FontData("Times New Roman")
    pres2 = tmp_pptx(pres)
    assert pres2.master_theme.font_scheme.major.latin_font.font_name == "Times New Roman"
    pres2.dispose()


def test_font_scheme_name_roundtrip(tmp_pptx):
    """Changing the font scheme name survives save/reload."""
    pres = Presentation()
    pres.master_theme.font_scheme.name = "MyFontScheme"
    pres2 = tmp_pptx(pres)
    assert pres2.master_theme.font_scheme.name == "MyFontScheme"
    pres2.dispose()


# ------------------------------------------------------------------
# Format scheme
# ------------------------------------------------------------------

def test_format_scheme_fill_styles_count():
    """Fill styles collection has 3 items (standard Office theme)."""
    pres = Presentation()
    assert pres.master_theme.format_scheme.fill_styles.length == 3
    pres.dispose()


def test_format_scheme_line_styles_count():
    """Line styles collection has 3 items."""
    pres = Presentation()
    assert pres.master_theme.format_scheme.line_styles.length == 3
    pres.dispose()


def test_format_scheme_effect_styles_count():
    """Effect styles collection has 3 items."""
    pres = Presentation()
    assert pres.master_theme.format_scheme.effect_styles.length == 3
    pres.dispose()


def test_format_scheme_bg_fill_styles_count():
    """Background fill styles collection has 3 items."""
    pres = Presentation()
    assert pres.master_theme.format_scheme.background_fill_styles.length == 3
    pres.dispose()


def test_format_scheme_line_style_width():
    """First line style has a readable width."""
    pres = Presentation()
    ls = pres.master_theme.format_scheme.line_styles[0]
    assert ls.width > 0
    pres.dispose()


def test_format_scheme_fill_style_type():
    """First fill style has a valid fill type."""
    pres = Presentation()
    ff = pres.master_theme.format_scheme.fill_styles[0]
    assert ff.fill_type == FillType.SOLID
    pres.dispose()


def test_format_scheme_effect_style_format():
    """Effect style has an effect_format."""
    pres = Presentation()
    es = pres.master_theme.format_scheme.effect_styles[0]
    ef = es.effect_format
    assert ef is not None
    pres.dispose()


def test_format_scheme_fill_style_modify_roundtrip(tmp_pptx):
    """Modifying a fill style color survives save/reload."""
    pres = Presentation()
    fs = pres.master_theme.format_scheme.fill_styles[0]
    fs.solid_fill_color.color = Color.red
    pres2 = tmp_pptx(pres)
    fs2 = pres2.master_theme.format_scheme.fill_styles[0]
    c = fs2.solid_fill_color.color
    assert c.r == 255 and c.g == 0 and c.b == 0
    pres2.dispose()


def test_format_scheme_iteration():
    """Can iterate over fill styles collection."""
    pres = Presentation()
    count = 0
    for ff in pres.master_theme.format_scheme.fill_styles:
        count += 1
        assert ff is not None
    assert count == 3
    pres.dispose()


# ------------------------------------------------------------------
# Extra color schemes
# ------------------------------------------------------------------

def test_extra_color_schemes_collection():
    """ExtraColorSchemeCollection is accessible (usually empty)."""
    pres = Presentation()
    ecs = pres.master_theme.extra_color_schemes
    assert ecs is not None
    # Default Office theme typically has no extra color schemes
    assert ecs.length >= 0
    pres.dispose()


# ------------------------------------------------------------------
# Theme managers
# ------------------------------------------------------------------

def test_slide_theme_manager():
    """Slide has a theme manager."""
    pres = Presentation()
    mgr = pres.slides[0].theme_manager
    assert mgr is not None
    assert mgr.is_override_theme_enabled is False
    pres.dispose()


def test_layout_theme_manager():
    """Layout slide has a theme manager."""
    pres = Presentation()
    mgr = pres.slides[0].layout_slide.theme_manager
    assert mgr is not None
    pres.dispose()


def test_master_theme_manager():
    """Master slide has a theme manager."""
    pres = Presentation()
    mgr = pres.masters[0].theme_manager
    assert mgr is not None
    pres.dispose()


def test_master_theme_manager_override_theme():
    """MasterThemeManager has override_theme property."""
    pres = Presentation()
    mgr = pres.masters[0].theme_manager
    # Initially no override
    assert mgr.override_theme is None or mgr.is_override_theme_enabled is False
    pres.dispose()


# ------------------------------------------------------------------
# Override theme
# ------------------------------------------------------------------

def test_override_theme_is_empty():
    """Slide override theme starts empty."""
    pres = Presentation()
    mgr = pres.slides[0].theme_manager
    ot = mgr.override_theme
    assert ot is not None
    assert ot.is_empty is True
    pres.dispose()


def test_override_theme_clear():
    """OverrideTheme.clear() resets to empty."""
    pres = Presentation()
    ot = pres.slides[0].theme_manager.override_theme
    ot.clear()
    assert ot.is_empty is True
    pres.dispose()
