"""Tests for scatter and bubble chart data round-trip and properties."""
import pytest

from aspose.slides_foss import Presentation
from aspose.slides_foss.charts import (
    ChartType, BubbleSizeRepresentationType, MarkerStyleType,
)


def _first_chart(pres):
    return pres.slides[0].shapes[0]


def _add_clean_chart(pres, chart_type):
    """Add a chart with no sample series — returns the chart."""
    chart = pres.slides[0].shapes.add_chart(chart_type, 50, 50, 500, 400, False)
    chart.chart_data.series.clear()
    return chart


# ---------------------------------------------------------------
# Scatter
# ---------------------------------------------------------------

class TestScatter:
    def test_add_scatter_data_points(self):
        """X/Y values are accessible on the data points after adding."""
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.SCATTER_WITH_MARKERS)
        s = chart.chart_data.series.add("S", ChartType.SCATTER_WITH_MARKERS)
        pts = [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)]
        for x, y in pts:
            s.data_points.add_data_point_for_scatter_series(x, y)

        assert len(s.data_points) == 3
        for dp, (x, y) in zip(s.data_points, pts):
            assert dp.x_value.as_literal_double == x
            assert dp.y_value.as_literal_double == y

    def test_scatter_round_trip_xy_values(self, tmp_pptx):
        """Save/reload preserves X and Y values for scatter series."""
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.SCATTER_WITH_MARKERS)
        s = chart.chart_data.series.add("Data", ChartType.SCATTER_WITH_MARKERS)
        expected = [(1.0, 2.5), (2.5, 4.1), (4.2, 3.3), (6.1, 5.8)]
        for x, y in expected:
            s.data_points.add_data_point_for_scatter_series(x, y)

        pres2 = tmp_pptx(pres)
        s2 = _first_chart(pres2).chart_data.series[0]
        assert len(s2.data_points) == len(expected)
        for dp, (x, y) in zip(s2.data_points, expected):
            assert dp.x_value is not None, "x_value must survive round-trip"
            assert dp.y_value is not None, "y_value must survive round-trip"
            assert dp.x_value.as_literal_double == pytest.approx(x)
            assert dp.y_value.as_literal_double == pytest.approx(y)

    def test_scatter_multi_series_round_trip(self, tmp_pptx):
        """Two scatter series each keep their own X/Y values."""
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.SCATTER_WITH_MARKERS)

        data1 = [(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)]
        s1 = chart.chart_data.series.add("A", ChartType.SCATTER_WITH_MARKERS)
        for x, y in data1:
            s1.data_points.add_data_point_for_scatter_series(x, y)

        data2 = [(1.5, 5.0), (2.5, 6.0), (3.5, 7.0)]
        s2 = chart.chart_data.series.add("B", ChartType.SCATTER_WITH_MARKERS)
        for x, y in data2:
            s2.data_points.add_data_point_for_scatter_series(x, y)

        pres2 = tmp_pptx(pres)
        series = list(_first_chart(pres2).chart_data.series)
        assert len(series) == 2
        for s, expected in zip(series, [data1, data2]):
            for dp, (x, y) in zip(s.data_points, expected):
                assert dp.x_value.as_literal_double == pytest.approx(x)
                assert dp.y_value.as_literal_double == pytest.approx(y)

    @pytest.mark.parametrize("chart_type", [
        ChartType.SCATTER_WITH_MARKERS,
        ChartType.SCATTER_WITH_SMOOTH_LINES,
        ChartType.SCATTER_WITH_SMOOTH_LINES_AND_MARKERS,
        ChartType.SCATTER_WITH_STRAIGHT_LINES,
        ChartType.SCATTER_WITH_STRAIGHT_LINES_AND_MARKERS,
    ])
    def test_all_scatter_subtypes_round_trip(self, chart_type, tmp_pptx):
        """Each scatter subtype preserves X/Y values through save/reload."""
        pres = Presentation()
        chart = _add_clean_chart(pres, chart_type)
        s = chart.chart_data.series.add("S", chart_type)
        expected = [(0.0, 0.0), (1.0, 2.0), (2.0, 1.5), (3.0, 4.0)]
        for x, y in expected:
            s.data_points.add_data_point_for_scatter_series(x, y)

        pres2 = tmp_pptx(pres)
        s2 = _first_chart(pres2).chart_data.series[0]
        for dp, (x, y) in zip(s2.data_points, expected):
            assert dp.x_value.as_literal_double == pytest.approx(x)
            assert dp.y_value.as_literal_double == pytest.approx(y)

    def test_scatter_marker_round_trip(self, tmp_pptx):
        """Series marker symbol/size persist across save/reload."""
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.SCATTER_WITH_MARKERS)
        s = chart.chart_data.series.add("S", ChartType.SCATTER_WITH_MARKERS)
        for x, y in [(1.0, 1.0), (2.0, 2.0)]:
            s.data_points.add_data_point_for_scatter_series(x, y)
        s.marker.symbol = MarkerStyleType.DIAMOND
        s.marker.size = 14

        pres2 = tmp_pptx(pres)
        s2 = _first_chart(pres2).chart_data.series[0]
        assert s2.marker.symbol == MarkerStyleType.DIAMOND
        assert s2.marker.size == 14

    def test_scatter_has_no_categories_path(self):
        """When data points supply X values, categories are not emitted to xVal."""
        import zipfile, tempfile, os
        from aspose.slides_foss.export import SaveFormat

        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.SCATTER_WITH_MARKERS)
        s = chart.chart_data.series.add("S", ChartType.SCATTER_WITH_MARKERS)
        for x, y in [(1.0, 10.0), (2.0, 20.0)]:
            s.data_points.add_data_point_for_scatter_series(x, y)

        fd, path = tempfile.mkstemp(suffix='.pptx')
        os.close(fd)
        try:
            pres.save(path, SaveFormat.PPTX)
            with zipfile.ZipFile(path) as z:
                xml = z.read('ppt/charts/chart1.xml').decode()
        finally:
            os.unlink(path)

        # xVal should use numRef (numeric) not strRef (string categories)
        assert '<c:xVal>' in xml
        xval_block = xml.split('<c:xVal>')[1].split('</c:xVal>')[0]
        assert '<c:numRef>' in xval_block
        assert '<c:strRef>' not in xval_block


# ---------------------------------------------------------------
# Bubble
# ---------------------------------------------------------------

class TestBubble:
    def test_add_bubble_data_points(self):
        """X/Y/Size values accessible on bubble data points after adding."""
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.BUBBLE)
        s = chart.chart_data.series.add("B", ChartType.BUBBLE)
        pts = [(1.0, 2.0, 5), (3.0, 4.0, 15), (5.0, 6.0, 25)]
        for x, y, sz in pts:
            s.data_points.add_data_point_for_bubble_series(x, y, sz)

        for dp, (x, y, sz) in zip(s.data_points, pts):
            assert dp.x_value.as_literal_double == x
            assert dp.y_value.as_literal_double == y
            assert dp.bubble_size.as_literal_double == sz

    def test_bubble_round_trip_xys(self, tmp_pptx):
        """Save/reload preserves X, Y, and size for bubble series."""
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.BUBBLE)
        s = chart.chart_data.series.add("Companies", ChartType.BUBBLE)
        expected = [(1.0, 10.0, 5), (2.5, 22.0, 18), (4.0, 15.0, 40), (5.5, 28.0, 65)]
        for x, y, sz in expected:
            s.data_points.add_data_point_for_bubble_series(x, y, sz)

        pres2 = tmp_pptx(pres)
        s2 = _first_chart(pres2).chart_data.series[0]
        assert len(s2.data_points) == len(expected)
        for dp, (x, y, sz) in zip(s2.data_points, expected):
            assert dp.x_value.as_literal_double == pytest.approx(x)
            assert dp.y_value.as_literal_double == pytest.approx(y)
            assert dp.bubble_size.as_literal_double == pytest.approx(sz)

    def test_bubble_size_scale_round_trip(self, tmp_pptx):
        """bubble_size_scale persists across save/reload."""
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.BUBBLE)
        s = chart.chart_data.series.add("B", ChartType.BUBBLE)
        for x, y, sz in [(1.0, 1.0, 10), (2.0, 2.0, 20)]:
            s.data_points.add_data_point_for_bubble_series(x, y, sz)
        chart.chart_data.series_groups[0].bubble_size_scale = 200

        pres2 = tmp_pptx(pres)
        grp = _first_chart(pres2).chart_data.series_groups[0]
        assert grp.bubble_size_scale == 200

    @pytest.mark.parametrize("rep", [
        BubbleSizeRepresentationType.WIDTH,
        BubbleSizeRepresentationType.AREA,
    ])
    def test_bubble_size_representation_round_trip(self, rep, tmp_pptx):
        """bubble_size_representation persists across save/reload."""
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.BUBBLE)
        s = chart.chart_data.series.add("B", ChartType.BUBBLE)
        for x, y, sz in [(1.0, 1.0, 10), (2.0, 2.0, 20)]:
            s.data_points.add_data_point_for_bubble_series(x, y, sz)
        chart.chart_data.series_groups[0].bubble_size_representation = rep

        pres2 = tmp_pptx(pres)
        grp = _first_chart(pres2).chart_data.series_groups[0]
        assert grp.bubble_size_representation == rep

    def test_bubble_3d_round_trip(self, tmp_pptx):
        """BUBBLE_WITH_3D preserves X/Y/size."""
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.BUBBLE_WITH_3D)
        s = chart.chart_data.series.add("B3", ChartType.BUBBLE_WITH_3D)
        for x, y, sz in [(1.0, 3.0, 10), (2.0, 6.0, 25)]:
            s.data_points.add_data_point_for_bubble_series(x, y, sz)

        pres2 = tmp_pptx(pres)
        s2 = _first_chart(pres2).chart_data.series[0]
        assert len(s2.data_points) == 2
        assert s2.data_points[1].bubble_size.as_literal_double == pytest.approx(25)

    def test_bubble_multi_series_round_trip(self, tmp_pptx):
        """Two bubble series keep their own X/Y/size values."""
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.BUBBLE)
        data1 = [(1.0, 10.0, 5), (2.0, 20.0, 10)]
        s1 = chart.chart_data.series.add("A", ChartType.BUBBLE)
        for x, y, sz in data1:
            s1.data_points.add_data_point_for_bubble_series(x, y, sz)

        data2 = [(3.0, 30.0, 15), (4.0, 40.0, 20)]
        s2 = chart.chart_data.series.add("B", ChartType.BUBBLE)
        for x, y, sz in data2:
            s2.data_points.add_data_point_for_bubble_series(x, y, sz)

        pres2 = tmp_pptx(pres)
        series = list(_first_chart(pres2).chart_data.series)
        assert len(series) == 2
        for s, expected in zip(series, [data1, data2]):
            for dp, (x, y, sz) in zip(s.data_points, expected):
                assert dp.x_value.as_literal_double == pytest.approx(x)
                assert dp.y_value.as_literal_double == pytest.approx(y)
                assert dp.bubble_size.as_literal_double == pytest.approx(sz)


# ---------------------------------------------------------------
# Emitter shape checks
# ---------------------------------------------------------------

class TestEmittedXml:
    """Spot-check the raw chart1.xml output for scatter/bubble."""

    def _save_and_read_chart_xml(self, pres, tmp_path):
        import zipfile
        from aspose.slides_foss.export import SaveFormat
        path = str(tmp_path / "x.pptx")
        pres.save(path, SaveFormat.PPTX)
        with zipfile.ZipFile(path) as z:
            return z.read('ppt/charts/chart1.xml').decode()

    def test_scatter_emits_xVal_and_yVal(self, tmp_path):
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.SCATTER_WITH_MARKERS)
        s = chart.chart_data.series.add("S", ChartType.SCATTER_WITH_MARKERS)
        s.data_points.add_data_point_for_scatter_series(1.0, 2.0)
        s.data_points.add_data_point_for_scatter_series(3.0, 4.0)

        xml = self._save_and_read_chart_xml(pres, tmp_path)
        assert '<c:xVal>' in xml
        assert '<c:yVal>' in xml
        assert '<c:val>' not in xml  # scatter must not use <c:val>

    def test_bubble_emits_xVal_yVal_bubbleSize(self, tmp_path):
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.BUBBLE)
        s = chart.chart_data.series.add("B", ChartType.BUBBLE)
        s.data_points.add_data_point_for_bubble_series(1.0, 2.0, 10)
        s.data_points.add_data_point_for_bubble_series(3.0, 4.0, 20)

        xml = self._save_and_read_chart_xml(pres, tmp_path)
        assert '<c:xVal>' in xml
        assert '<c:yVal>' in xml
        assert '<c:bubbleSize>' in xml

    def test_scatter_yVal_values_are_non_zero(self, tmp_path):
        """Regression: yVal used to emit zeros when y_value was set via the
        scatter API."""
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.SCATTER_WITH_MARKERS)
        s = chart.chart_data.series.add("S", ChartType.SCATTER_WITH_MARKERS)
        s.data_points.add_data_point_for_scatter_series(1.0, 7.5)
        s.data_points.add_data_point_for_scatter_series(2.0, 8.5)

        xml = self._save_and_read_chart_xml(pres, tmp_path)
        yval_block = xml.split('<c:yVal>')[1].split('</c:yVal>')[0]
        assert '<c:v>7.5</c:v>' in yval_block
        assert '<c:v>8.5</c:v>' in yval_block

    def test_3d_bubble_emits_bubble3D_in_ser(self, tmp_path):
        """<c:bubble3D val="1"/> must live inside <c:ser>, not at chart-type level.

        Regression: old code put bubble3D directly under <c:bubbleChart>, which
        corrupted the file in PowerPoint.
        """
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.BUBBLE_WITH_3D)
        s = chart.chart_data.series.add("B3", ChartType.BUBBLE_WITH_3D)
        s.data_points.add_data_point_for_bubble_series(1.0, 2.0, 10)

        xml = self._save_and_read_chart_xml(pres, tmp_path)
        # bubble3D should appear inside <c:ser>, right after </c:bubbleSize>
        ser_block = xml.split('<c:ser>')[1].split('</c:ser>')[0]
        assert '<c:bubble3D val="1"/>' in ser_block
        # and should NOT appear outside the ser as a direct child of bubbleChart
        chart_block = xml.split('<c:bubbleChart>')[1].split('<c:ser>')[0]
        assert 'bubble3D' not in chart_block

    def test_plain_bubble_emits_bubble3D_val_0(self, tmp_path):
        """Plain bubble series also get <c:bubble3D val="0"/> — matches commercial."""
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.BUBBLE)
        s = chart.chart_data.series.add("B", ChartType.BUBBLE)
        s.data_points.add_data_point_for_bubble_series(1.0, 2.0, 10)

        xml = self._save_and_read_chart_xml(pres, tmp_path)
        ser_block = xml.split('<c:ser>')[1].split('</c:ser>')[0]
        assert '<c:bubble3D val="0"/>' in ser_block

    def test_straight_line_scatter_emits_smooth_val_0(self, tmp_path):
        """Straight-line scatter must explicitly set <c:smooth val="0"/>,
        otherwise PowerPoint defaults the line to smoothed."""
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.SCATTER_WITH_STRAIGHT_LINES)
        s = chart.chart_data.series.add(
            "L", ChartType.SCATTER_WITH_STRAIGHT_LINES)
        s.data_points.add_data_point_for_scatter_series(1.0, 1.0)
        s.data_points.add_data_point_for_scatter_series(2.0, 2.0)

        xml = self._save_and_read_chart_xml(pres, tmp_path)
        assert '<c:smooth val="0"/>' in xml
        assert '<c:smooth val="1"/>' not in xml

    def test_smooth_line_scatter_emits_smooth_val_1(self, tmp_path):
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.SCATTER_WITH_SMOOTH_LINES)
        s = chart.chart_data.series.add(
            "S", ChartType.SCATTER_WITH_SMOOTH_LINES)
        s.data_points.add_data_point_for_scatter_series(1.0, 1.0)
        s.data_points.add_data_point_for_scatter_series(2.0, 2.0)

        xml = self._save_and_read_chart_xml(pres, tmp_path)
        assert '<c:smooth val="1"/>' in xml


# ---------------------------------------------------------------
# Workbook-cell path
# ---------------------------------------------------------------

class TestWorkbookCells:
    """Adding data points via chart_data_workbook.get_cell(..., value)."""

    def test_scatter_via_workbook_cells(self, tmp_pptx):
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.SCATTER_WITH_MARKERS)
        wb = chart.chart_data.chart_data_workbook
        name_cell = wb.get_cell(0, "B1", "Data")
        s = chart.chart_data.series.add(name_cell, ChartType.SCATTER_WITH_MARKERS)
        expected = [(1.0, 2.5), (2.5, 4.1), (4.2, 3.3)]
        for i, (x, y) in enumerate(expected):
            row = i + 2
            x_cell = wb.get_cell(0, f"A{row}", x)
            y_cell = wb.get_cell(0, f"B{row}", y)
            s.data_points.add_data_point_for_scatter_series(x_cell, y_cell)

        pres2 = tmp_pptx(pres)
        s2 = _first_chart(pres2).chart_data.series[0]
        for dp, (x, y) in zip(s2.data_points, expected):
            assert dp.x_value.as_literal_double == pytest.approx(x)
            assert dp.y_value.as_literal_double == pytest.approx(y)

    def test_3d_bubble_chart_type_is_preserved(self):
        """Regression: add_chart(BUBBLE_WITH_3D) → chart.type must return
        BUBBLE_WITH_3D (not BUBBLE). The distinguishing bubble3D marker
        lives in <c:ser> which doesn't exist at chart creation time, so
        type detection alone would pick BUBBLE.
        """
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(
            ChartType.BUBBLE_WITH_3D, 50, 50, 500, 400, False)
        assert chart.type == ChartType.BUBBLE_WITH_3D

    def test_3d_bubble_adds_bubble3D_val_1_via_chart_type(self, tmp_path):
        """End-to-end: when a chart is created as BUBBLE_WITH_3D and a series
        is added with chart.type, the series emits <c:bubble3D val="1"/>.
        """
        import zipfile
        from aspose.slides_foss.export import SaveFormat

        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(
            ChartType.BUBBLE_WITH_3D, 50, 50, 500, 400, False)
        chart.chart_data.series.clear()
        s = chart.chart_data.series.add("S", chart.type)
        s.data_points.add_data_point_for_bubble_series(1.0, 2.0, 10)

        path = str(tmp_path / "x.pptx")
        pres.save(path, SaveFormat.PPTX)
        with zipfile.ZipFile(path) as z:
            xml = z.read('ppt/charts/chart1.xml').decode()
        assert '<c:bubble3D val="1"/>' in xml
        assert '<c:bubble3D val="0"/>' not in xml

    def test_multi_series_formula_refs_match_cells(self, tmp_path):
        """Regression: for a multi-series scatter built with cells from
        distinct columns, each series' xVal/yVal <c:f> ref must point
        at the columns where the cells actually live. Otherwise the
        chart cache and the embedded workbook drift apart — when the user
        hits Edit Data in PowerPoint, the chart reloads from the workbook
        and values shift or disappear.
        """
        import zipfile, re
        from aspose.slides_foss.export import SaveFormat

        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.SCATTER_WITH_MARKERS)
        wb = chart.chart_data.chart_data_workbook

        # Series 1 uses A/B
        n1 = wb.get_cell(0, "B1", "One")
        s1 = chart.chart_data.series.add(n1, ChartType.SCATTER_WITH_MARKERS)
        for i, (x, y) in enumerate([(1.0, 2.0), (3.0, 4.0)]):
            s1.data_points.add_data_point_for_scatter_series(
                wb.get_cell(0, f"A{i+2}", x), wb.get_cell(0, f"B{i+2}", y))

        # Series 2 uses C/D
        n2 = wb.get_cell(0, "D1", "Two")
        s2 = chart.chart_data.series.add(n2, ChartType.SCATTER_WITH_MARKERS)
        for i, (x, y) in enumerate([(5.0, 6.0), (7.0, 8.0)]):
            s2.data_points.add_data_point_for_scatter_series(
                wb.get_cell(0, f"C{i+2}", x), wb.get_cell(0, f"D{i+2}", y))

        path = str(tmp_path / "x.pptx")
        pres.save(path, SaveFormat.PPTX)
        with zipfile.ZipFile(path) as z:
            xml = z.read('ppt/charts/chart1.xml').decode()

        refs = re.findall(r'<c:f>([^<]+)</c:f>', xml)
        # series 1: name=B1, x=A, y=B; series 2: name=D1, x=C, y=D
        assert refs[0] == 'Sheet1!$B$1'
        assert refs[1].startswith('Sheet1!$A$2') and refs[1].endswith('A$3')
        assert refs[2].startswith('Sheet1!$B$2') and refs[2].endswith('B$3')
        assert refs[3] == 'Sheet1!$D$1'
        assert refs[4].startswith('Sheet1!$C$2') and refs[4].endswith('C$3')
        assert refs[5].startswith('Sheet1!$D$2') and refs[5].endswith('D$3')

    def test_bubble_via_workbook_cells(self, tmp_pptx):
        pres = Presentation()
        chart = _add_clean_chart(pres, ChartType.BUBBLE)
        wb = chart.chart_data.chart_data_workbook
        name_cell = wb.get_cell(0, "B1", "Data")
        s = chart.chart_data.series.add(name_cell, ChartType.BUBBLE)
        expected = [(1.0, 10.0, 5), (2.0, 20.0, 15), (3.0, 30.0, 25)]
        for i, (x, y, sz) in enumerate(expected):
            row = i + 2
            x_cell = wb.get_cell(0, f"A{row}", x)
            y_cell = wb.get_cell(0, f"B{row}", y)
            sz_cell = wb.get_cell(0, f"C{row}", sz)
            s.data_points.add_data_point_for_bubble_series(x_cell, y_cell, sz_cell)

        pres2 = tmp_pptx(pres)
        s2 = _first_chart(pres2).chart_data.series[0]
        for dp, (x, y, sz) in zip(s2.data_points, expected):
            assert dp.x_value.as_literal_double == pytest.approx(x)
            assert dp.y_value.as_literal_double == pytest.approx(y)
            assert dp.bubble_size.as_literal_double == pytest.approx(sz)
