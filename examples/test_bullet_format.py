"""
Bullet format — symbol bullets, numbered bullets, and removing bullets.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import (
    Presentation, ShapeType,
    BulletType, NumberedBulletStyle, FontData, Portion,
)
from aspose.slides_foss.drawing import Color
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def symbol_bullets():
    """Create a bulleted list with custom symbol character."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 200)

        # Set up first paragraph with bullet
        tf = shape.text_frame
        tf.text = ""  # clear default text

        items = ["First item", "Second item", "Third item"]
        for i, text in enumerate(items):
            if i == 0:
                para = tf.paragraphs[0]
            else:
                from aspose.slides_foss import Paragraph
                para = Paragraph()
                tf.paragraphs.add(para)

            portion = Portion(text)
            para.portions.add(portion)

            # Configure bullet
            bf = para.paragraph_format.bullet
            bf.type = BulletType.SYMBOL
            bf.char = "\u2022"  # bullet character
            bf.font = FontData("Arial")
            bf.height = 100  # percentage of text size

            # Bullet color
            bf.color.color = Color.dark_blue

        print(f"Created {tf.paragraphs.count} bullet paragraphs")
        pres.save(os.path.join(OUT, "symbol_bullets.pptx"), SaveFormat.PPTX)


def numbered_bullets():
    """Create a numbered list with different styles."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 200)

        tf = shape.text_frame
        tf.text = ""

        items = ["Step one", "Step two", "Step three"]
        for i, text in enumerate(items):
            if i == 0:
                para = tf.paragraphs[0]
            else:
                from aspose.slides_foss import Paragraph
                para = Paragraph()
                tf.paragraphs.add(para)

            portion = Portion(text)
            para.portions.add(portion)

            # Numbered bullet
            bf = para.paragraph_format.bullet
            bf.type = BulletType.NUMBERED
            bf.numbered_bullet_style = NumberedBulletStyle.BULLET_ARABIC_PERIOD
            bf.numbered_bullet_start_with = 1

        print(f"Created {tf.paragraphs.count} numbered paragraphs")
        pres.save(os.path.join(OUT, "numbered_bullets.pptx"), SaveFormat.PPTX)


def remove_bullets():
    """Remove bullets from paragraphs by setting type to NONE."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 200)

        tf = shape.text_frame
        tf.text = "No bullet here"

        bf = tf.paragraphs[0].paragraph_format.bullet
        bf.type = BulletType.NONE

        print(f"Bullet type: {bf.type}")
        pres.save(os.path.join(OUT, "no_bullets.pptx"), SaveFormat.PPTX)


def custom_start_number():
    """Start numbered list from a custom number."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 200)

        tf = shape.text_frame
        tf.text = ""

        items = ["Continued item", "Another item"]
        for i, text in enumerate(items):
            if i == 0:
                para = tf.paragraphs[0]
            else:
                from aspose.slides_foss import Paragraph
                para = Paragraph()
                tf.paragraphs.add(para)

            portion = Portion(text)
            para.portions.add(portion)

            bf = para.paragraph_format.bullet
            bf.type = BulletType.NUMBERED
            bf.numbered_bullet_style = NumberedBulletStyle.BULLET_ROMAN_UC_PERIOD
            bf.numbered_bullet_start_with = 5  # start from V.

        print("Numbered list starting from 5 (Roman: V.)")
        pres.save(os.path.join(OUT, "custom_start_number.pptx"), SaveFormat.PPTX)


if __name__ == "__main__":
    symbol_bullets()
    numbered_bullets()
    remove_bullets()
    custom_start_number()
    print("\n=== test_bullet_format.py completed ===")
