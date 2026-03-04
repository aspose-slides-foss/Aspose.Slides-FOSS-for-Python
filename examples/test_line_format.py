"""
LineFormat — width, dash style, cap style, join style, arrowheads, and fill.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import (
    Presentation, ShapeType, FillType,
    LineDashStyle, LineCapStyle, LineJoinStyle, LineStyle,
    LineArrowheadStyle, LineArrowheadWidth, LineArrowheadLength,
)
from aspose.slides_foss.drawing import Color
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def line_width_and_color():
    """Set line width and color on a shape outline."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)

        lf = shape.line_format
        lf.width = 5
        lf.fill_format.fill_type = FillType.SOLID
        lf.fill_format.solid_fill_color.color = Color.dark_red

        print(f"Line width: {lf.width}")
        pres.save(os.path.join(OUT, "line_width_color.pptx"), SaveFormat.PPTX)


def dash_style():
    """Set different line dash styles."""
    with Presentation() as pres:
        slide = pres.slides[0]

        styles = [LineDashStyle.SOLID, LineDashStyle.DASH, LineDashStyle.DOT, LineDashStyle.DASH_DOT]
        for i, style in enumerate(styles):
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50 + i * 80, 200, 50)
            lf = shape.line_format
            lf.width = 3
            lf.dash_style = style
            lf.fill_format.fill_type = FillType.SOLID
            lf.fill_format.solid_fill_color.color = Color.black
            shape.text_frame.text = str(style)

        print(f"Created {len(styles)} shapes with different dash styles")
        pres.save(os.path.join(OUT, "dash_styles.pptx"), SaveFormat.PPTX)


def cap_style():
    """Set line cap style."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)

        lf = shape.line_format
        lf.width = 8
        lf.cap_style = LineCapStyle.ROUND
        lf.fill_format.fill_type = FillType.SOLID
        lf.fill_format.solid_fill_color.color = Color.navy

        print(f"cap_style: {lf.cap_style}")
        pres.save(os.path.join(OUT, "cap_style.pptx"), SaveFormat.PPTX)


def join_style():
    """Set line join style."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)

        lf = shape.line_format
        lf.width = 6
        lf.join_style = LineJoinStyle.BEVEL
        lf.fill_format.fill_type = FillType.SOLID
        lf.fill_format.solid_fill_color.color = Color.dark_green

        print(f"join_style: {lf.join_style}")
        pres.save(os.path.join(OUT, "join_style.pptx"), SaveFormat.PPTX)


def line_style():
    """Set line style (single, double, etc.)."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)

        lf = shape.line_format
        lf.width = 4
        lf.style = LineStyle.THIN_THICK
        lf.fill_format.fill_type = FillType.SOLID
        lf.fill_format.solid_fill_color.color = Color.purple

        print(f"line style: {lf.style}")
        pres.save(os.path.join(OUT, "line_style.pptx"), SaveFormat.PPTX)


def arrowheads():
    """Set arrowheads on a connector."""
    with Presentation() as pres:
        slide = pres.slides[0]
        connector = slide.shapes.add_connector(
            ShapeType.STRAIGHT_CONNECTOR1, 50, 100, 400, 100
        )

        lf = connector.line_format
        lf.width = 3
        lf.fill_format.fill_type = FillType.SOLID
        lf.fill_format.solid_fill_color.color = Color.black

        # Begin arrowhead
        lf.begin_arrowhead_style = LineArrowheadStyle.OVAL
        lf.begin_arrowhead_width = LineArrowheadWidth.WIDE
        lf.begin_arrowhead_length = LineArrowheadLength.LONG

        # End arrowhead
        lf.end_arrowhead_style = LineArrowheadStyle.TRIANGLE
        lf.end_arrowhead_width = LineArrowheadWidth.WIDE
        lf.end_arrowhead_length = LineArrowheadLength.LONG

        print(f"Begin: {lf.begin_arrowhead_style}, End: {lf.end_arrowhead_style}")
        pres.save(os.path.join(OUT, "arrowheads.pptx"), SaveFormat.PPTX)


if __name__ == "__main__":
    line_width_and_color()
    dash_style()
    cap_style()
    join_style()
    line_style()
    arrowheads()
    print("\n=== test_line_format.py completed ===")
