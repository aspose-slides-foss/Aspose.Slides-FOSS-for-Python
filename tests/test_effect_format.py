"""Tests for EffectFormat: shadow, glow, soft edge, blur, reflection."""
from aspose.slides_foss import Presentation, ShapeType, RectangleAlignment
from aspose.slides_foss.drawing import Color


def _clear(pres):
    pres.slides[0].shapes.clear()
    return pres.slides[0]


def test_outer_shadow(tmp_pptx):
    """Outer shadow properties persist after save/reload."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
    ef = shape.effect_format
    ef.enable_outer_shadow_effect()
    shadow = ef.outer_shadow_effect
    shadow.blur_radius = 10
    shadow.direction = 315
    shadow.distance = 8
    shadow.shadow_color.color = Color.from_argb(128, 0, 0, 0)

    pres2 = tmp_pptx(pres)
    ef2 = pres2.slides[0].shapes[0].effect_format
    s2 = ef2.outer_shadow_effect
    assert s2 is not None, "outer_shadow_effect should not be None after reload"
    assert s2.blur_radius == 10
    assert s2.direction == 315
    assert s2.distance == 8
    pres2.dispose()


def test_glow(tmp_pptx):
    """Glow effect persists."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 100, 100, 200, 200)
    ef = shape.effect_format
    ef.enable_glow_effect()
    ef.glow_effect.radius = 15
    ef.glow_effect.color.color = Color.gold

    pres2 = tmp_pptx(pres)
    g2 = pres2.slides[0].shapes[0].effect_format.glow_effect
    assert g2 is not None, "glow_effect should not be None after reload"
    assert g2.radius == 15
    pres2.dispose()


def test_soft_edge(tmp_pptx):
    """Soft edge radius persists."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
    ef = shape.effect_format
    ef.enable_soft_edge_effect()
    ef.soft_edge_effect.radius = 10

    pres2 = tmp_pptx(pres)
    se2 = pres2.slides[0].shapes[0].effect_format.soft_edge_effect
    assert se2 is not None, "soft_edge_effect should not be None after reload"
    assert se2.radius == 10
    pres2.dispose()


def test_blur(tmp_pptx):
    """Blur effect persists."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
    ef = shape.effect_format
    ef.set_blur_effect(8, True)

    pres2 = tmp_pptx(pres)
    b2 = pres2.slides[0].shapes[0].effect_format.blur_effect
    assert b2 is not None, "blur_effect should not be None after reload"
    assert b2.radius == 8
    pres2.dispose()


def test_enable_disable_effects():
    """Effects can be enabled then disabled."""
    with Presentation() as pres:
        shape = pres.slides[0].shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
        ef = shape.effect_format
        ef.enable_outer_shadow_effect()
        ef.enable_glow_effect()
        assert ef.is_no_effects is False

        ef.disable_outer_shadow_effect()
        ef.disable_glow_effect()
        assert ef.is_no_effects is True
