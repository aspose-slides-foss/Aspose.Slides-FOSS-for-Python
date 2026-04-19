"""Tests for axis formatting (gridlines, text format, axis format)."""
import os, tempfile, pytest
from aspose.slides_foss import Presentation, FillType, LineDashStyle, FontData
from aspose.slides_foss.NullableBool import NullableBool
from aspose.slides_foss.export import SaveFormat
from aspose.slides_foss.charts import ChartType, Format, ChartLinesFormat, ChartTextFormat, ChartPortionFormat
from aspose.slides_foss.drawing import Color


def _save_and_reload(prs):
    with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as f:
        path = f.name
    try:
        prs.save(path, SaveFormat.PPTX)
        return Presentation(path)
    finally:
        os.unlink(path)


class TestAxisGridlinesFormat:
    def test_major_gridlines_line_color(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 400, 300)
        gl = chart.axes.vertical_axis.major_grid_lines_format
        assert isinstance(gl, ChartLinesFormat)
        gl.line.fill_format.fill_type = FillType.SOLID
        gl.line.fill_format.solid_fill_color.color = Color.from_argb(255, 0, 0, 255)
        gl.line.width = 5

        prs2 = _save_and_reload(prs)
        chart2 = prs2.slides[0].shapes[0]
        gl2 = chart2.axes.vertical_axis.major_grid_lines_format
        assert gl2.line.fill_format.fill_type == FillType.SOLID
        assert gl2.line.fill_format.solid_fill_color.color.b == 255
        assert abs(gl2.line.width - 5) < 0.5

    def test_minor_gridlines_line_color(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 400, 300)
        gl = chart.axes.vertical_axis.minor_grid_lines_format
        gl.line.fill_format.fill_type = FillType.SOLID
        gl.line.fill_format.solid_fill_color.color = Color.from_argb(255, 255, 0, 0)
        gl.line.width = 3

        prs2 = _save_and_reload(prs)
        chart2 = prs2.slides[0].shapes[0]
        gl2 = chart2.axes.vertical_axis.minor_grid_lines_format
        assert gl2.line.fill_format.fill_type == FillType.SOLID
        assert gl2.line.fill_format.solid_fill_color.color.r == 255
        assert abs(gl2.line.width - 3) < 0.5

    def test_category_axis_gridlines(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 400, 300)
        gl = chart.axes.horizontal_axis.major_grid_lines_format
        gl.line.fill_format.fill_type = FillType.SOLID
        gl.line.fill_format.solid_fill_color.color = Color.from_argb(255, 0, 128, 0)

        prs2 = _save_and_reload(prs)
        chart2 = prs2.slides[0].shapes[0]
        gl2 = chart2.axes.horizontal_axis.major_grid_lines_format
        assert gl2.line.fill_format.fill_type == FillType.SOLID
        assert gl2.line.fill_format.solid_fill_color.color.g == 128

    def test_gridlines_dash_style(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 400, 300)
        gl = chart.axes.vertical_axis.major_grid_lines_format
        gl.line.fill_format.fill_type = FillType.SOLID
        gl.line.fill_format.solid_fill_color.color = Color.from_argb(255, 0, 0, 255)
        gl.line.dash_style = LineDashStyle.DASH_DOT

        prs2 = _save_and_reload(prs)
        chart2 = prs2.slides[0].shapes[0]
        gl2 = chart2.axes.vertical_axis.major_grid_lines_format
        assert gl2.line.dash_style == LineDashStyle.DASH_DOT


class TestAxisTextFormat:
    def test_value_axis_text_bold_italic(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 400, 300)
        tf = chart.axes.vertical_axis.text_format
        assert isinstance(tf, ChartTextFormat)
        pf = tf.portion_format
        assert isinstance(pf, ChartPortionFormat)
        pf.font_bold = NullableBool.TRUE
        pf.font_italic = NullableBool.TRUE
        pf.font_height = 16

        prs2 = _save_and_reload(prs)
        chart2 = prs2.slides[0].shapes[0]
        pf2 = chart2.axes.vertical_axis.text_format.portion_format
        assert pf2.font_bold == NullableBool.TRUE
        assert pf2.font_italic == NullableBool.TRUE
        assert abs(pf2.font_height - 16) < 0.5

    def test_text_format_color(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 400, 300)
        pf = chart.axes.vertical_axis.text_format.portion_format
        pf.fill_format.fill_type = FillType.SOLID
        pf.fill_format.solid_fill_color.color = Color.from_argb(255, 0, 100, 0)

        prs2 = _save_and_reload(prs)
        chart2 = prs2.slides[0].shapes[0]
        pf2 = chart2.axes.vertical_axis.text_format.portion_format
        assert pf2.fill_format.fill_type == FillType.SOLID
        assert pf2.fill_format.solid_fill_color.color.g == 100

    def test_text_format_latin_font(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 400, 300)
        pf = chart.axes.horizontal_axis.text_format.portion_format
        pf.latin_font = FontData("Arial")

        prs2 = _save_and_reload(prs)
        chart2 = prs2.slides[0].shapes[0]
        pf2 = chart2.axes.horizontal_axis.text_format.portion_format
        assert pf2.latin_font.font_name == "Arial"


class TestAxisFormat:
    def test_axis_line_format(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 400, 300)
        fmt = chart.axes.vertical_axis.format
        assert isinstance(fmt, Format)
        fmt.line.fill_format.fill_type = FillType.SOLID
        fmt.line.fill_format.solid_fill_color.color = Color.from_argb(255, 255, 0, 0)
        fmt.line.width = 3

        prs2 = _save_and_reload(prs)
        chart2 = prs2.slides[0].shapes[0]
        fmt2 = chart2.axes.vertical_axis.format
        assert fmt2.line.fill_format.fill_type == FillType.SOLID
        assert fmt2.line.fill_format.solid_fill_color.color.r == 255
        assert abs(fmt2.line.width - 3) < 0.5

    def test_axis_fill_format(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 400, 300)
        fmt = chart.axes.vertical_axis.format
        fmt.fill.fill_type = FillType.SOLID
        fmt.fill.solid_fill_color.color = Color.from_argb(255, 200, 200, 200)

        prs2 = _save_and_reload(prs)
        chart2 = prs2.slides[0].shapes[0]
        fmt2 = chart2.axes.vertical_axis.format
        assert fmt2.fill.fill_type == FillType.SOLID
        assert fmt2.fill.solid_fill_color.color.r == 200
