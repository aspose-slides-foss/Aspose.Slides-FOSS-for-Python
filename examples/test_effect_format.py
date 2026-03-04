"""
EffectFormat — outer shadow, glow, reflection, soft edge, blur, enable/disable.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import Presentation, ShapeType, RectangleAlignment
from aspose.slides_foss.drawing import Color
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def outer_shadow():
    """Apply an outer shadow effect to a shape."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
        shape.text_frame.text = "Shadow"

        ef = shape.effect_format
        ef.enable_outer_shadow_effect()

        shadow = ef.outer_shadow_effect
        shadow.blur_radius = 10
        shadow.direction = 315  # degrees
        shadow.distance = 8
        shadow.shadow_color.color = Color.from_argb(128, 0, 0, 0)  # semi-transparent black
        shadow.rect_shadow_alignment = RectangleAlignment.BOTTOM_RIGHT

        print(f"Shadow: blur={shadow.blur_radius}, dir={shadow.direction}, dist={shadow.distance}")
        pres.save(os.path.join(OUT, "outer_shadow.pptx"), SaveFormat.PPTX)


def glow_effect():
    """Apply a glow effect to a shape."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 100, 100, 200, 200)
        shape.text_frame.text = "Glow"

        ef = shape.effect_format
        ef.enable_glow_effect()

        glow = ef.glow_effect
        glow.radius = 15
        glow.color.color = Color.gold

        print(f"Glow: radius={glow.radius}")
        pres.save(os.path.join(OUT, "glow_effect.pptx"), SaveFormat.PPTX)


def reflection_effect():
    """Apply a reflection effect to a shape."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 50, 200, 100)
        shape.text_frame.text = "Reflected"

        ef = shape.effect_format
        ef.enable_reflection_effect()

        ref = ef.reflection_effect
        ref.blur_radius = 2
        ref.direction = 90
        ref.distance = 5
        ref.start_pos_alpha = 50
        ref.end_pos_alpha = 0
        ref.start_reflection_opacity = 50
        ref.end_reflection_opacity = 0
        ref.fade_direction = 90
        ref.scale_horizontal = 100
        ref.scale_vertical = -100

        print(f"Reflection: blur={ref.blur_radius}, distance={ref.distance}")
        pres.save(os.path.join(OUT, "reflection_effect.pptx"), SaveFormat.PPTX)


def soft_edge():
    """Apply a soft edge effect to a shape."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
        shape.text_frame.text = "Soft Edge"

        ef = shape.effect_format
        ef.enable_soft_edge_effect()

        se = ef.soft_edge_effect
        se.radius = 10

        print(f"Soft edge radius: {se.radius}")
        pres.save(os.path.join(OUT, "soft_edge.pptx"), SaveFormat.PPTX)


def blur_effect():
    """Apply a blur effect to a shape."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
        shape.text_frame.text = "Blurred"

        ef = shape.effect_format
        ef.set_blur_effect(8, True)  # radius=8, grow=True

        blur = ef.blur_effect
        print(f"Blur radius: {blur.radius}")
        pres.save(os.path.join(OUT, "blur_effect.pptx"), SaveFormat.PPTX)


def disable_effects():
    """Enable then disable effects."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)

        ef = shape.effect_format

        # Enable some effects
        ef.enable_outer_shadow_effect()
        ef.enable_glow_effect()
        print(f"is_no_effects after enable: {ef.is_no_effects}")

        # Disable them
        ef.disable_outer_shadow_effect()
        ef.disable_glow_effect()
        print(f"is_no_effects after disable: {ef.is_no_effects}")

        pres.save(os.path.join(OUT, "disable_effects.pptx"), SaveFormat.PPTX)


if __name__ == "__main__":
    outer_shadow()
    glow_effect()
    reflection_effect()
    soft_edge()
    blur_effect()
    disable_effects()
    print("\n=== test_effect_format.py completed ===")
