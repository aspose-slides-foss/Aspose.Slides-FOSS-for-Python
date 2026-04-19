"""Tests for ChartPlotArea implementation."""

import pytest
from aspose.slides_foss import Presentation, ShapeType
from aspose.slides_foss.export import SaveFormat
from aspose.slides_foss.charts import ChartType, ChartPlotArea, LayoutTargetType


@pytest.fixture
def pres_with_chart(tmp_path):
    """Create a presentation with a chart and return (pres, chart)."""
    pres = Presentation()
    slide = pres.slides[0]
    # Add a chart: x=50, y=50, w=500, h=400 (EMU values)
    chart_shape = slide.shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
    return pres, chart_shape


class TestChartPlotAreaAccess:
    def test_plot_area_not_none(self, pres_with_chart):
        pres, chart = pres_with_chart
        assert chart.plot_area is not None

    def test_plot_area_is_chart_plot_area(self, pres_with_chart):
        pres, chart = pres_with_chart
        assert isinstance(chart.plot_area, ChartPlotArea)

    def test_plot_area_cached(self, pres_with_chart):
        pres, chart = pres_with_chart
        pa1 = chart.plot_area
        pa2 = chart.plot_area
        assert pa1 is pa2

    def test_chart_reference(self, pres_with_chart):
        pres, chart = pres_with_chart
        assert chart.plot_area.chart is chart


class TestPlotAreaLayoutDefaults:
    def test_default_x(self, pres_with_chart):
        pres, chart = pres_with_chart
        # Default plot area has no manualLayout, so values are 0.0
        assert chart.plot_area.x == 0.0

    def test_default_y(self, pres_with_chart):
        pres, chart = pres_with_chart
        assert chart.plot_area.y == 0.0

    def test_default_width(self, pres_with_chart):
        pres, chart = pres_with_chart
        assert chart.plot_area.width == 0.0

    def test_default_height(self, pres_with_chart):
        pres, chart = pres_with_chart
        assert chart.plot_area.height == 0.0

    def test_is_location_autocalculated_default(self, pres_with_chart):
        pres, chart = pres_with_chart
        assert chart.plot_area.is_location_autocalculated is True


class TestPlotAreaLayoutReadWrite:
    def test_set_x(self, pres_with_chart):
        pres, chart = pres_with_chart
        chart.plot_area.x = 0.1
        assert chart.plot_area.x == pytest.approx(0.1)

    def test_set_y(self, pres_with_chart):
        pres, chart = pres_with_chart
        chart.plot_area.y = 0.2
        assert chart.plot_area.y == pytest.approx(0.2)

    def test_set_width(self, pres_with_chart):
        pres, chart = pres_with_chart
        chart.plot_area.width = 0.8
        assert chart.plot_area.width == pytest.approx(0.8)

    def test_set_height(self, pres_with_chart):
        pres, chart = pres_with_chart
        chart.plot_area.height = 0.7
        assert chart.plot_area.height == pytest.approx(0.7)

    def test_right_computed(self, pres_with_chart):
        pres, chart = pres_with_chart
        chart.plot_area.x = 0.1
        chart.plot_area.width = 0.8
        assert chart.plot_area.right == pytest.approx(0.9)

    def test_bottom_computed(self, pres_with_chart):
        pres, chart = pres_with_chart
        chart.plot_area.y = 0.05
        chart.plot_area.height = 0.9
        assert chart.plot_area.bottom == pytest.approx(0.95)

    def test_not_autocalculated_after_set(self, pres_with_chart):
        pres, chart = pres_with_chart
        chart.plot_area.x = 0.1
        assert chart.plot_area.is_location_autocalculated is False


class TestPlotAreaLayoutTargetType:
    def test_default_layout_target_type(self, pres_with_chart):
        pres, chart = pres_with_chart
        assert chart.plot_area.layout_target_type == LayoutTargetType.INNER

    def test_set_layout_target_type_outer(self, pres_with_chart):
        pres, chart = pres_with_chart
        chart.plot_area.layout_target_type = LayoutTargetType.OUTER
        assert chart.plot_area.layout_target_type == LayoutTargetType.OUTER

    def test_set_layout_target_type_inner(self, pres_with_chart):
        pres, chart = pres_with_chart
        chart.plot_area.layout_target_type = LayoutTargetType.OUTER
        chart.plot_area.layout_target_type = LayoutTargetType.INNER
        assert chart.plot_area.layout_target_type == LayoutTargetType.INNER


class TestPlotAreaFormat:
    def test_format_not_none(self, pres_with_chart):
        pres, chart = pres_with_chart
        assert chart.plot_area.format is not None

    def test_format_fill(self, pres_with_chart):
        pres, chart = pres_with_chart
        fill = chart.plot_area.format.fill
        assert fill is not None

    def test_format_line(self, pres_with_chart):
        pres, chart = pres_with_chart
        line = chart.plot_area.format.line
        assert line is not None


class TestPlotAreaActualLayout:
    def test_actual_x(self, pres_with_chart):
        pres, chart = pres_with_chart
        chart.plot_area.x = 0.15
        chart.validate_chart_layout()
        assert chart.plot_area.actual_x == pytest.approx(0.15)

    def test_actual_y(self, pres_with_chart):
        pres, chart = pres_with_chart
        chart.plot_area.y = 0.25
        chart.validate_chart_layout()
        assert chart.plot_area.actual_y == pytest.approx(0.25)


class TestPlotAreaRoundTrip:
    def test_layout_survives_save_load(self, pres_with_chart, tmp_path):
        pres, chart = pres_with_chart
        chart.plot_area.x = 0.1
        chart.plot_area.y = 0.2
        chart.plot_area.width = 0.75
        chart.plot_area.height = 0.65

        path = str(tmp_path / "plot_area.pptx")
        pres.save(path, SaveFormat.PPTX)

        pres2 = Presentation(path)
        chart2 = pres2.slides[0].shapes[0]
        pa = chart2.plot_area
        assert pa.x == pytest.approx(0.1)
        assert pa.y == pytest.approx(0.2)
        assert pa.width == pytest.approx(0.75)
        assert pa.height == pytest.approx(0.65)

    def test_layout_target_survives_save_load(self, pres_with_chart, tmp_path):
        pres, chart = pres_with_chart
        chart.plot_area.layout_target_type = LayoutTargetType.OUTER

        path = str(tmp_path / "plot_area_target.pptx")
        pres.save(path, SaveFormat.PPTX)

        pres2 = Presentation(path)
        chart2 = pres2.slides[0].shapes[0]
        assert chart2.plot_area.layout_target_type == LayoutTargetType.OUTER

    def test_format_fill_survives_save_load(self, pres_with_chart, tmp_path):
        from aspose.slides_foss import FillType
        from aspose.slides_foss.drawing import Color

        pres, chart = pres_with_chart
        chart.plot_area.format.fill.fill_type = FillType.SOLID
        chart.plot_area.format.fill.solid_fill_color.color = Color.light_gray

        path = str(tmp_path / "plot_area_fill.pptx")
        pres.save(path, SaveFormat.PPTX)

        pres2 = Presentation(path)
        chart2 = pres2.slides[0].shapes[0]
        fill = chart2.plot_area.format.fill
        assert fill.fill_type == FillType.SOLID


class TestValidateChartLayout:
    def test_validate_does_not_raise(self, pres_with_chart):
        pres, chart = pres_with_chart
        chart.validate_chart_layout()  # should not raise


class TestPlotAreaInterfaceProperties:
    def test_as_i_layoutable(self, pres_with_chart):
        pres, chart = pres_with_chart
        assert chart.plot_area.as_i_layoutable is chart.plot_area

    def test_as_i_actual_layout(self, pres_with_chart):
        pres, chart = pres_with_chart
        assert chart.plot_area.as_i_actual_layout is chart.plot_area

    def test_slide_reference(self, pres_with_chart):
        pres, chart = pres_with_chart
        assert chart.plot_area.slide is not None

    def test_presentation_reference(self, pres_with_chart):
        pres, chart = pres_with_chart
        assert chart.plot_area.presentation is not None
