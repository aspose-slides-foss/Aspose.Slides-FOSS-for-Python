"""Tests for chart creation and data manipulation."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aspose.slides_foss.Presentation import Presentation
from aspose.slides_foss.charts.ChartType import ChartType


class TestChartCreate(unittest.TestCase):

    def test_add_clustered_column_chart(self):
        pres = Presentation()
        slide = pres.slides[0]
        chart = slide.shapes.add_chart(ChartType.CLUSTERED_COLUMN, 100, 100, 500, 400)
        self.assertIsNotNone(chart)
        self.assertEqual(chart.type, ChartType.CLUSTERED_COLUMN)

    def test_chart_has_sample_data(self):
        pres = Presentation()
        slide = pres.slides[0]
        chart = slide.shapes.add_chart(ChartType.CLUSTERED_COLUMN, 100, 100, 500, 400)
        cd = chart.chart_data
        self.assertGreater(len(cd.series), 0)
        self.assertGreater(len(cd.categories), 0)

    def test_chart_series_data_points(self):
        pres = Presentation()
        slide = pres.slides[0]
        chart = slide.shapes.add_chart(ChartType.CLUSTERED_COLUMN, 100, 100, 500, 400)
        series = chart.chart_data.series[0]
        self.assertEqual(series.name.as_literal_string, 'Series 1')
        self.assertEqual(len(series.data_points), 4)
        self.assertAlmostEqual(series.data_points[0].value.to_double(), 4.3)

    def test_chart_categories(self):
        pres = Presentation()
        slide = pres.slides[0]
        chart = slide.shapes.add_chart(ChartType.CLUSTERED_COLUMN, 100, 100, 500, 400)
        cats = chart.chart_data.categories
        self.assertEqual(len(cats), 4)
        self.assertEqual(cats[0].value, 'Category 1')
        self.assertEqual(cats[3].value, 'Category 4')

    def test_add_chart_no_sample(self):
        pres = Presentation()
        slide = pres.slides[0]
        chart = slide.shapes.add_chart(ChartType.CLUSTERED_COLUMN, 100, 100, 500, 400, False)
        self.assertEqual(len(chart.chart_data.series), 0)

    def test_pie_chart(self):
        pres = Presentation()
        slide = pres.slides[0]
        chart = slide.shapes.add_chart(ChartType.PIE, 100, 100, 400, 400)
        self.assertEqual(chart.type, ChartType.PIE)
        # Pie should have 1 series
        self.assertEqual(len(chart.chart_data.series), 1)


class TestChartDataWorkbook(unittest.TestCase):

    def test_workbook_get_cell(self):
        pres = Presentation()
        slide = pres.slides[0]
        chart = slide.shapes.add_chart(ChartType.CLUSTERED_COLUMN, 100, 100, 500, 400)
        wb = chart.chart_data.chart_data_workbook
        # Read existing data
        cell = wb.get_cell(0, 0, 1)  # B1 = "Series 1"
        self.assertEqual(cell.value, 'Series 1')

    def test_workbook_set_cell(self):
        pres = Presentation()
        slide = pres.slides[0]
        chart = slide.shapes.add_chart(ChartType.CLUSTERED_COLUMN, 100, 100, 500, 400)
        wb = chart.chart_data.chart_data_workbook
        cell = wb.get_cell(0, 1, 1, 99.9)  # B2 = 99.9
        self.assertAlmostEqual(cell.value, 99.9)

    def test_workbook_worksheets(self):
        pres = Presentation()
        slide = pres.slides[0]
        chart = slide.shapes.add_chart(ChartType.CLUSTERED_COLUMN, 100, 100, 500, 400)
        wb = chart.chart_data.chart_data_workbook
        worksheets = wb.worksheets
        self.assertEqual(len(worksheets), 1)
        self.assertEqual(worksheets[0].name, 'Sheet1')


class TestChartModifyData(unittest.TestCase):

    def test_clear_and_rebuild(self):
        pres = Presentation()
        slide = pres.slides[0]
        chart = slide.shapes.add_chart(ChartType.CLUSTERED_COLUMN, 100, 100, 500, 400)
        cd = chart.chart_data
        wb = cd.chart_data_workbook

        # Clear existing data
        cd.series.clear()
        cd.categories.clear()

        # Add new categories
        cd.categories.add(wb.get_cell(0, 1, 0, 'Q1'))
        cd.categories.add(wb.get_cell(0, 2, 0, 'Q2'))

        # Add new series
        series = cd.series.add(wb.get_cell(0, 0, 1, 'Revenue'), chart.type)
        series.data_points.add_data_point_for_bar_series(wb.get_cell(0, 1, 1, 100))
        series.data_points.add_data_point_for_bar_series(wb.get_cell(0, 2, 1, 200))

        self.assertEqual(len(cd.categories), 2)
        self.assertEqual(len(cd.series), 1)
        self.assertEqual(len(cd.series[0].data_points), 2)
        self.assertEqual(cd.categories[0].value, 'Q1')
        self.assertAlmostEqual(cd.series[0].data_points[0].value.to_double(), 100)
        self.assertAlmostEqual(cd.series[0].data_points[1].value.to_double(), 200)


class TestChartRoundTrip(unittest.TestCase):

    def test_save_and_reopen(self):
        import io
        pres = Presentation()
        slide = pres.slides[0]
        chart = slide.shapes.add_chart(ChartType.CLUSTERED_COLUMN, 100, 100, 500, 400)

        # Save to stream
        stream = io.BytesIO()
        from aspose.slides_foss.export.SaveFormat import SaveFormat
        pres.save(stream, SaveFormat.PPTX)
        stream.seek(0)

        # Reopen
        pres2 = Presentation(stream)
        slide2 = pres2.slides[0]

        # Find the chart shape
        chart2 = None
        for shape in slide2.shapes:
            if hasattr(shape, 'chart_data'):
                chart2 = shape
                break

        self.assertIsNotNone(chart2, "Chart not found after reload")
        self.assertEqual(chart2.type, ChartType.CLUSTERED_COLUMN)
        self.assertEqual(len(chart2.chart_data.series), 3)
        self.assertEqual(len(chart2.chart_data.categories), 4)
        self.assertEqual(chart2.chart_data.categories[0].value, 'Category 1')


CHARTS_PPTX = r'C:\Dev\GitHub\Aspose.Slides-FOSS-for-Python\manual_tests\Charts.pptx'


@unittest.skipUnless(os.path.exists(CHARTS_PPTX), 'Charts.pptx not available')
class TestChartReadExisting(unittest.TestCase):

    def test_read_charts_pptx(self):
        pres = Presentation(CHARTS_PPTX)
        slide = pres.slides[0]

        # Find charts
        charts = [s for s in slide.shapes if hasattr(s, 'chart_data')]
        self.assertGreaterEqual(len(charts), 1, "Expected at least one chart")

        chart = charts[0]
        self.assertIsNotNone(chart.chart_data)
        self.assertGreater(len(chart.chart_data.series), 0)

    def test_read_chart_data_values(self):
        pres = Presentation(CHARTS_PPTX)
        slide = pres.slides[0]
        charts = [s for s in slide.shapes if hasattr(s, 'chart_data')]
        chart = charts[0]

        # First series should be "Series 1"
        series0 = chart.chart_data.series[0]
        self.assertEqual(series0.name.as_literal_string, 'Series 1')

        # Check data points
        self.assertGreater(len(series0.data_points), 0)
        self.assertAlmostEqual(series0.data_points[0].value.to_double(), 4.3)


class TestChartSeriesGroups(unittest.TestCase):

    def test_series_groups_created_for_clustered_column(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        groups = chart.chart_data.series_groups
        self.assertEqual(len(groups), 1)
        from aspose.slides_foss.charts.CombinableSeriesTypesGroup import CombinableSeriesTypesGroup
        self.assertEqual(groups[0].type, CombinableSeriesTypesGroup.BAR_CHART_VERT_CLUSTERED)

    def test_series_groups_contain_all_series(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        group = chart.chart_data.series_groups[0]
        self.assertEqual(len(group.series), len(chart.chart_data.series))

    def test_parent_series_group_back_link(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        group = chart.chart_data.series_groups[0]
        for s in chart.chart_data.series:
            self.assertIs(s.parent_series_group, group)

    def test_gap_width_default_and_set(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        group = chart.chart_data.series_groups[0]
        self.assertEqual(group.gap_width, 150)
        group.gap_width = 200
        self.assertEqual(group.gap_width, 200)

    def test_overlap_set_via_parent_series_group(self):
        """Matches doc example: series.parent_series_group.overlap = 30"""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 20, 20, 500, 200)
        series = chart.chart_data.series[0]
        self.assertEqual(series.overlap, 0)
        series.parent_series_group.overlap = 30
        self.assertEqual(series.overlap, 30)

    def test_gap_width_round_trip(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.STACKED_COLUMN, 50, 50, 500, 400)
        chart.chart_data.series_groups[0].gap_width = 42
        import tempfile, os
        f = tempfile.NamedTemporaryFile(suffix='.pptx', delete=False)
        f.close()
        try:
            from aspose.slides_foss.export.SaveFormat import SaveFormat
            pres.save(f.name, SaveFormat.PPTX)
            pres2 = Presentation(f.name)
            chart2 = pres2.slides[0].shapes[0]
            self.assertEqual(chart2.chart_data.series_groups[0].gap_width, 42)
        finally:
            os.unlink(f.name)

    def test_overlap_round_trip(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.chart_data.series_groups[0].overlap = -75
        import tempfile, os
        f = tempfile.NamedTemporaryFile(suffix='.pptx', delete=False)
        f.close()
        try:
            from aspose.slides_foss.export.SaveFormat import SaveFormat
            pres.save(f.name, SaveFormat.PPTX)
            pres2 = Presentation(f.name)
            chart2 = pres2.slides[0].shapes[0]
            self.assertEqual(chart2.chart_data.series_groups[0].overlap, -75)
        finally:
            os.unlink(f.name)

    def test_pie_chart_group_type(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.PIE, 50, 50, 500, 400)
        from aspose.slides_foss.charts.CombinableSeriesTypesGroup import CombinableSeriesTypesGroup
        self.assertEqual(chart.chart_data.series_groups[0].type, CombinableSeriesTypesGroup.PIE_CHART)

    def test_first_slice_angle(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.PIE, 50, 50, 500, 400)
        group = chart.chart_data.series_groups[0]
        group.first_slice_angle = 90
        self.assertEqual(group.first_slice_angle, 90)

    def test_doughnut_hole_size(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.DOUGHNUT, 50, 50, 500, 400)
        group = chart.chart_data.series_groups[0]
        group.doughnut_hole_size = 80
        self.assertEqual(group.doughnut_hole_size, 80)

    def test_is_color_varied(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.PIE, 50, 50, 500, 400)
        group = chart.chart_data.series_groups[0]
        group.is_color_varied = True
        self.assertTrue(group.is_color_varied)
        group.is_color_varied = False
        self.assertFalse(group.is_color_varied)

    def test_series_readonly_delegation(self):
        """Read-only properties on ChartSeries delegate to parent group."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        group = chart.chart_data.series_groups[0]
        series = chart.chart_data.series[0]
        group.gap_width = 99
        group.overlap = -10
        self.assertEqual(series.gap_width, 99)
        self.assertEqual(series.overlap, -10)


    def test_add_series_updates_groups(self):
        """Adding a series should be reflected in series_groups."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        cd = chart.chart_data
        initial_count = len(cd.series_groups[0].series)
        cd.series.add('New Series', ChartType.CLUSTERED_COLUMN)
        # After adding, groups should rebuild and include the new series
        group = cd.series_groups[0]
        self.assertEqual(len(group.series), initial_count + 1)

    def test_remove_series_updates_groups(self):
        """Removing a series should be reflected in series_groups."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        cd = chart.chart_data
        initial_count = len(cd.series_groups[0].series)
        self.assertGreater(initial_count, 1)
        cd.series.remove_at(0)
        group = cd.series_groups[0]
        self.assertEqual(len(group.series), initial_count - 1)

    def test_clear_series_updates_groups(self):
        """Clearing all series should result in empty group series."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        cd = chart.chart_data
        cd.series.clear()
        group = cd.series_groups[0]
        self.assertEqual(len(group.series), 0)

    def test_group_identity_preserved_after_series_change(self):
        """Group object identity and properties survive series mutation."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        cd = chart.chart_data
        group = cd.series_groups[0]
        group.gap_width = 77
        group.overlap = -20
        group_id = id(group)
        # Mutate series
        cd.series.add('Extra', ChartType.CLUSTERED_COLUMN)
        group_after = cd.series_groups[0]
        # Same object
        self.assertEqual(id(group_after), group_id)
        # Properties still there
        self.assertEqual(group_after.gap_width, 77)
        self.assertEqual(group_after.overlap, -20)

    def test_new_series_has_parent_group(self):
        """A newly added series should have a valid parent_series_group."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        new_series = chart.chart_data.series.add('Extra', ChartType.CLUSTERED_COLUMN)
        self.assertIsNotNone(new_series.parent_series_group)
        self.assertIs(new_series.parent_series_group, chart.chart_data.series_groups[0])


class TestComboChartSeriesGroups(unittest.TestCase):
    """Combo charts: multiple chart types on one plot area → multiple series groups."""

    def _save_and_reload(self, pres):
        import tempfile, os
        from aspose.slides_foss.export.SaveFormat import SaveFormat
        f = tempfile.NamedTemporaryFile(suffix='.pptx', delete=False)
        f.close()
        try:
            pres.save(f.name, SaveFormat.PPTX)
            pres2 = Presentation(f.name)
            return pres2
        finally:
            os.unlink(f.name)

    def test_combo_column_line_produces_two_groups(self):
        """Changing a series type to LINE splits into two chart-type elements."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 600, 400)
        chart.chart_data.series[2].type = ChartType.LINE

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        groups = chart2.chart_data.series_groups
        self.assertEqual(len(groups), 2)

    def test_combo_group_types_correct(self):
        """Each group has the correct CombinableSeriesTypesGroup."""
        from aspose.slides_foss.charts.CombinableSeriesTypesGroup import CombinableSeriesTypesGroup
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 600, 400)
        chart.chart_data.series[2].type = ChartType.LINE

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        groups = chart2.chart_data.series_groups
        self.assertEqual(groups[0].type, CombinableSeriesTypesGroup.BAR_CHART_VERT_CLUSTERED)
        self.assertEqual(groups[1].type, CombinableSeriesTypesGroup.LINE_CHART_LINE)

    def test_combo_series_distribution(self):
        """2 column + 1 line → group[0] has 2 series, group[1] has 1."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 600, 400)
        chart.chart_data.series[2].type = ChartType.LINE

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        groups = chart2.chart_data.series_groups
        self.assertEqual(len(groups[0].series), 2)
        self.assertEqual(len(groups[1].series), 1)

    def test_combo_series_types_preserved(self):
        """Each series retains its type after round-trip."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 600, 400)
        chart.chart_data.series[2].type = ChartType.LINE

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        types = [s.type for s in chart2.chart_data.series]
        self.assertEqual(types[0], ChartType.CLUSTERED_COLUMN)
        self.assertEqual(types[1], ChartType.CLUSTERED_COLUMN)
        self.assertEqual(types[2], ChartType.LINE)

    def test_combo_total_series_count(self):
        """Total series count across all groups equals original."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 600, 400)
        original_count = len(chart.chart_data.series)
        chart.chart_data.series[2].type = ChartType.LINE

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertEqual(len(chart2.chart_data.series), original_count)

    def test_combo_group_properties_independent(self):
        """Each group's properties are independent."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 600, 400)
        chart.chart_data.series[2].type = ChartType.LINE

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        groups = chart2.chart_data.series_groups
        groups[0].gap_width = 42
        # Line group gap_width should be its own default, not 42
        self.assertEqual(groups[0].gap_width, 42)
        self.assertNotEqual(groups[1].gap_width, 42)

    def test_combo_gap_width_round_trip(self):
        """gap_width set on bar group survives save+reload of combo chart."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 600, 400)
        chart.chart_data.series[2].type = ChartType.LINE
        # Must save first to create the lineChart element, then reload
        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        chart2.chart_data.series_groups[0].gap_width = 77

        pres3 = self._save_and_reload(pres2)
        chart3 = pres3.slides[0].shapes[0]
        self.assertEqual(chart3.chart_data.series_groups[0].gap_width, 77)

    def test_combo_two_line_one_column(self):
        """1 column + 2 line series → 2 groups with correct sizes."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 600, 400)
        chart.chart_data.series[1].type = ChartType.LINE
        chart.chart_data.series[2].type = ChartType.LINE

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        groups = chart2.chart_data.series_groups
        self.assertEqual(len(groups), 2)
        self.assertEqual(len(groups[0].series), 1)  # 1 column
        self.assertEqual(len(groups[1].series), 2)  # 2 lines

    def test_all_same_type_single_group(self):
        """When all series have the same type, only one group exists."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 600, 400)

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertEqual(len(chart2.chart_data.series_groups), 1)

    def test_combo_parent_series_group_correct(self):
        """Each series in a combo chart links to the correct group."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 600, 400)
        chart.chart_data.series[2].type = ChartType.LINE

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        groups = chart2.chart_data.series_groups
        for s in groups[0].series:
            self.assertIs(s.parent_series_group, groups[0])
        for s in groups[1].series:
            self.assertIs(s.parent_series_group, groups[1])

    def test_load_existing_combo_chart(self):
        """Create combo with commercial-like XML, verify it loads correctly."""
        # Create, save, reload — simulates loading an existing combo chart
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 600, 400)
        chart.chart_data.series[2].type = ChartType.LINE

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]

        # Verify data survived
        self.assertEqual(len(chart2.chart_data.series), 3)
        self.assertGreater(len(chart2.chart_data.series[0].data_points), 0)
        self.assertGreater(len(chart2.chart_data.series[2].data_points), 0)


class TestTrendlines(unittest.TestCase):
    """Tests for chart trendline creation, properties, and round-trip."""

    def _save_and_reload(self, pres):
        import tempfile
        from aspose.slides_foss.export.SaveFormat import SaveFormat
        f = tempfile.NamedTemporaryFile(suffix='.pptx', delete=False)
        f.close()
        try:
            pres.save(f.name, SaveFormat.PPTX)
            pres2 = Presentation(f.name)
            return pres2
        finally:
            os.unlink(f.name)

    def _get_chart(self, pres):
        for shape in pres.slides[0].shapes:
            if hasattr(shape, 'chart_data'):
                return shape
        return None

    def test_add_linear_trendline(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        series = chart.chart_data.series[0]
        tl = series.trend_lines.add(TrendlineType.LINEAR)
        self.assertEqual(series.trend_lines.count, 1)
        self.assertEqual(tl.trendline_type, TrendlineType.LINEAR)

    def test_add_multiple_trendlines(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        series = chart.chart_data.series[0]
        series.trend_lines.add(TrendlineType.LINEAR)
        series.trend_lines.add(TrendlineType.EXPONENTIAL)
        series.trend_lines.add(TrendlineType.POLYNOMIAL)
        self.assertEqual(series.trend_lines.count, 3)

    def test_remove_trendline(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        series = chart.chart_data.series[0]
        tl = series.trend_lines.add(TrendlineType.LINEAR)
        series.trend_lines.add(TrendlineType.EXPONENTIAL)
        self.assertEqual(series.trend_lines.count, 2)
        series.trend_lines.remove(tl)
        self.assertEqual(series.trend_lines.count, 1)
        self.assertEqual(series.trend_lines[0].trendline_type, TrendlineType.EXPONENTIAL)

    def test_trendline_name(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        tl = chart.chart_data.series[0].trend_lines.add(TrendlineType.LINEAR)
        tl.trendline_name = 'My Trend'
        self.assertEqual(tl.trendline_name, 'My Trend')

    def test_trendline_display_equation(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        tl = chart.chart_data.series[0].trend_lines.add(TrendlineType.LINEAR)
        self.assertFalse(tl.display_equation)
        tl.display_equation = True
        self.assertTrue(tl.display_equation)

    def test_trendline_display_r_squared(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        tl = chart.chart_data.series[0].trend_lines.add(TrendlineType.LINEAR)
        self.assertFalse(tl.display_r_squared_value)
        tl.display_r_squared_value = True
        self.assertTrue(tl.display_r_squared_value)

    def test_trendline_forward_backward(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        tl = chart.chart_data.series[0].trend_lines.add(TrendlineType.LINEAR)
        tl.forward = 2.5
        tl.backward = 1.0
        self.assertAlmostEqual(tl.forward, 2.5)
        self.assertAlmostEqual(tl.backward, 1.0)

    def test_polynomial_order(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        tl = chart.chart_data.series[0].trend_lines.add(TrendlineType.POLYNOMIAL)
        tl.order = 4
        self.assertEqual(tl.order, 4)

    def test_polynomial_order_validation(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        tl = chart.chart_data.series[0].trend_lines.add(TrendlineType.POLYNOMIAL)
        with self.assertRaises(ValueError):
            tl.order = 1
        with self.assertRaises(ValueError):
            tl.order = 7

    def test_moving_average_period(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        tl = chart.chart_data.series[0].trend_lines.add(TrendlineType.MOVING_AVERAGE)
        tl.period = 5
        self.assertEqual(tl.period, 5)

    def test_moving_average_period_validation(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        tl = chart.chart_data.series[0].trend_lines.add(TrendlineType.MOVING_AVERAGE)
        with self.assertRaises(ValueError):
            tl.period = 1
        with self.assertRaises(ValueError):
            tl.period = 256

    def test_intercept(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        import math
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        tl = chart.chart_data.series[0].trend_lines.add(TrendlineType.LINEAR)
        # Default is NaN (auto)
        self.assertTrue(math.isnan(tl.intercept))
        tl.intercept = 5.0
        self.assertAlmostEqual(tl.intercept, 5.0)

    def test_all_trendline_types(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        series = chart.chart_data.series[0]
        for tt in TrendlineType:
            tl = series.trend_lines.add(tt)
            self.assertEqual(tl.trendline_type, tt)
        self.assertEqual(series.trend_lines.count, len(TrendlineType))

    def test_trendline_round_trip_linear(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        tl = chart.chart_data.series[0].trend_lines.add(TrendlineType.LINEAR)
        tl.trendline_name = 'Linear Trend'
        tl.display_equation = True
        tl.display_r_squared_value = True
        tl.forward = 1.5
        tl.backward = 0.5

        pres2 = self._save_and_reload(pres)
        chart2 = self._get_chart(pres2)
        tl2 = chart2.chart_data.series[0].trend_lines[0]
        self.assertEqual(tl2.trendline_type, TrendlineType.LINEAR)
        self.assertEqual(tl2.trendline_name, 'Linear Trend')
        self.assertTrue(tl2.display_equation)
        self.assertTrue(tl2.display_r_squared_value)
        self.assertAlmostEqual(tl2.forward, 1.5)
        self.assertAlmostEqual(tl2.backward, 0.5)

    def test_trendline_round_trip_polynomial(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        tl = chart.chart_data.series[0].trend_lines.add(TrendlineType.POLYNOMIAL)
        tl.order = 5
        tl.intercept = 10.0

        pres2 = self._save_and_reload(pres)
        chart2 = self._get_chart(pres2)
        tl2 = chart2.chart_data.series[0].trend_lines[0]
        self.assertEqual(tl2.trendline_type, TrendlineType.POLYNOMIAL)
        self.assertEqual(tl2.order, 5)
        self.assertAlmostEqual(tl2.intercept, 10.0)

    def test_trendline_round_trip_moving_average(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        tl = chart.chart_data.series[0].trend_lines.add(TrendlineType.MOVING_AVERAGE)
        tl.period = 4

        pres2 = self._save_and_reload(pres)
        chart2 = self._get_chart(pres2)
        tl2 = chart2.chart_data.series[0].trend_lines[0]
        self.assertEqual(tl2.trendline_type, TrendlineType.MOVING_AVERAGE)
        self.assertEqual(tl2.period, 4)

    def test_trendline_round_trip_all_types(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        series = chart.chart_data.series[0]
        for tt in TrendlineType:
            series.trend_lines.add(tt)

        pres2 = self._save_and_reload(pres)
        chart2 = self._get_chart(pres2)
        series2 = chart2.chart_data.series[0]
        self.assertEqual(series2.trend_lines.count, len(TrendlineType))
        types_after = [series2.trend_lines[i].trendline_type for i in range(series2.trend_lines.count)]
        self.assertEqual(types_after, list(TrendlineType))

    def test_multiple_series_independent_trendlines(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        s0 = chart.chart_data.series[0]
        s1 = chart.chart_data.series[1]
        s0.trend_lines.add(TrendlineType.LINEAR)
        s1.trend_lines.add(TrendlineType.EXPONENTIAL)
        s1.trend_lines.add(TrendlineType.POWER)

        pres2 = self._save_and_reload(pres)
        chart2 = self._get_chart(pres2)
        self.assertEqual(chart2.chart_data.series[0].trend_lines.count, 1)
        self.assertEqual(chart2.chart_data.series[1].trend_lines.count, 2)
        self.assertEqual(chart2.chart_data.series[0].trend_lines[0].trendline_type, TrendlineType.LINEAR)
        self.assertEqual(chart2.chart_data.series[1].trend_lines[0].trendline_type, TrendlineType.EXPONENTIAL)
        self.assertEqual(chart2.chart_data.series[1].trend_lines[1].trendline_type, TrendlineType.POWER)

    def test_trendline_iteration(self):
        from aspose.slides_foss.charts.TrendlineType import TrendlineType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        series = chart.chart_data.series[0]
        series.trend_lines.add(TrendlineType.LINEAR)
        series.trend_lines.add(TrendlineType.LOGARITHMIC)
        types = [tl.trendline_type for tl in series.trend_lines]
        self.assertEqual(types, [TrendlineType.LINEAR, TrendlineType.LOGARITHMIC])

    def test_series_without_trendlines(self):
        """Series with no trendlines should have count=0."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        for series in chart.chart_data.series:
            self.assertEqual(series.trend_lines.count, 0)


class TestDataTable(unittest.TestCase):
    """Tests for chart data table creation, properties, and round-trip."""

    def _save_and_reload(self, pres):
        import tempfile
        from aspose.slides_foss.export.SaveFormat import SaveFormat
        f = tempfile.NamedTemporaryFile(suffix='.pptx', delete=False)
        f.close()
        try:
            pres.save(f.name, SaveFormat.PPTX)
            pres2 = Presentation(f.name)
            return pres2
        finally:
            os.unlink(f.name)

    def test_has_data_table_default_false(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        self.assertFalse(chart.has_data_table)

    def test_enable_data_table(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_data_table = True
        self.assertTrue(chart.has_data_table)

    def test_disable_data_table(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_data_table = True
        self.assertTrue(chart.has_data_table)
        chart.has_data_table = False
        self.assertFalse(chart.has_data_table)

    def test_chart_data_table_property(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        dt = chart.chart_data_table
        self.assertIsNotNone(dt)
        from aspose.slides_foss.charts.DataTable import DataTable
        self.assertIsInstance(dt, DataTable)

    def test_data_table_border_horizontal(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_data_table = True
        dt = chart.chart_data_table
        dt.has_border_horizontal = True
        self.assertTrue(dt.has_border_horizontal)
        dt.has_border_horizontal = False
        self.assertFalse(dt.has_border_horizontal)

    def test_data_table_border_vertical(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_data_table = True
        dt = chart.chart_data_table
        dt.has_border_vertical = True
        self.assertTrue(dt.has_border_vertical)
        dt.has_border_vertical = False
        self.assertFalse(dt.has_border_vertical)

    def test_data_table_border_outline(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_data_table = True
        dt = chart.chart_data_table
        dt.has_border_outline = True
        self.assertTrue(dt.has_border_outline)
        dt.has_border_outline = False
        self.assertFalse(dt.has_border_outline)

    def test_data_table_show_legend_key(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_data_table = True
        dt = chart.chart_data_table
        dt.show_legend_key = True
        self.assertTrue(dt.show_legend_key)
        dt.show_legend_key = False
        self.assertFalse(dt.show_legend_key)

    def test_data_table_round_trip(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_data_table = True
        dt = chart.chart_data_table
        dt.has_border_horizontal = True
        dt.has_border_vertical = True
        dt.has_border_outline = False
        dt.show_legend_key = True

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertTrue(chart2.has_data_table)
        dt2 = chart2.chart_data_table
        self.assertTrue(dt2.has_border_horizontal)
        self.assertTrue(dt2.has_border_vertical)
        self.assertFalse(dt2.has_border_outline)
        self.assertTrue(dt2.show_legend_key)

    def test_data_table_removed_round_trip(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_data_table = True
        chart.has_data_table = False

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertFalse(chart2.has_data_table)

    def test_data_table_chart_back_reference(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        dt = chart.chart_data_table
        self.assertIs(dt.chart, chart)


class TestAxesManager(unittest.TestCase):
    """Tests for Chart.axes and Axis properties."""

    def test_axes_manager_not_none(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        axes = chart.axes
        self.assertIsNotNone(axes)

    def test_horizontal_axis_exists(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        h_axis = chart.axes.horizontal_axis
        self.assertIsNotNone(h_axis)

    def test_vertical_axis_exists(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        v_axis = chart.axes.vertical_axis
        self.assertIsNotNone(v_axis)

    def test_horizontal_axis_position_bottom(self):
        from aspose.slides_foss.charts.AxisPositionType import AxisPositionType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        self.assertEqual(chart.axes.horizontal_axis.position, AxisPositionType.BOTTOM)

    def test_vertical_axis_position_left(self):
        from aspose.slides_foss.charts.AxisPositionType import AxisPositionType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        self.assertEqual(chart.axes.vertical_axis.position, AxisPositionType.LEFT)

    def test_axis_is_visible_default(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        self.assertTrue(chart.axes.vertical_axis.is_visible)

    def test_axis_set_invisible(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.axes.vertical_axis.is_visible = False
        self.assertFalse(chart.axes.vertical_axis.is_visible)

    def test_axis_max_min_value(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        v = chart.axes.vertical_axis
        v.max_value = 100.0
        v.min_value = -10.0
        self.assertAlmostEqual(v.max_value, 100.0)
        self.assertAlmostEqual(v.min_value, -10.0)
        self.assertFalse(v.is_automatic_max_value)
        self.assertFalse(v.is_automatic_min_value)

    def test_axis_auto_max_min(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        v = chart.axes.vertical_axis
        # Default is automatic
        self.assertTrue(v.is_automatic_max_value)
        self.assertTrue(v.is_automatic_min_value)

    def test_axis_major_minor_unit(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        v = chart.axes.vertical_axis
        v.major_unit = 5.0
        v.minor_unit = 1.0
        self.assertAlmostEqual(v.major_unit, 5.0)
        self.assertAlmostEqual(v.minor_unit, 1.0)
        self.assertFalse(v.is_automatic_major_unit)
        self.assertFalse(v.is_automatic_minor_unit)

    def test_axis_logarithmic(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        v = chart.axes.vertical_axis
        self.assertFalse(v.is_logarithmic)
        v.is_logarithmic = True
        self.assertTrue(v.is_logarithmic)
        self.assertAlmostEqual(v.log_base, 10.0)
        v.log_base = 2.0
        self.assertAlmostEqual(v.log_base, 2.0)

    def test_axis_plot_order_reversed(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        v = chart.axes.vertical_axis
        self.assertFalse(v.is_plot_order_reversed)
        v.is_plot_order_reversed = True
        self.assertTrue(v.is_plot_order_reversed)

    def test_axis_cross_type(self):
        from aspose.slides_foss.charts.CrossesType import CrossesType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        v = chart.axes.vertical_axis
        v.cross_type = CrossesType.MAXIMUM
        self.assertEqual(v.cross_type, CrossesType.MAXIMUM)
        v.cross_type = CrossesType.CUSTOM
        v.cross_at = 5.0
        self.assertEqual(v.cross_type, CrossesType.CUSTOM)
        self.assertAlmostEqual(v.cross_at, 5.0)

    def test_axis_tick_marks(self):
        from aspose.slides_foss.charts.TickMarkType import TickMarkType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        v = chart.axes.vertical_axis
        v.major_tick_mark = TickMarkType.OUTSIDE
        v.minor_tick_mark = TickMarkType.NONE
        self.assertEqual(v.major_tick_mark, TickMarkType.OUTSIDE)
        self.assertEqual(v.minor_tick_mark, TickMarkType.NONE)

    def test_axis_tick_label_position(self):
        from aspose.slides_foss.charts.TickLabelPositionType import TickLabelPositionType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        h = chart.axes.horizontal_axis
        h.tick_label_position = TickLabelPositionType.LOW
        self.assertEqual(h.tick_label_position, TickLabelPositionType.LOW)

    def test_axis_number_format(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        v = chart.axes.vertical_axis
        v.number_format = '0.00%'
        self.assertEqual(v.number_format, '0.00%')

    def test_axis_has_title(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        v = chart.axes.vertical_axis
        self.assertFalse(v.has_title)
        v.has_title = True
        self.assertTrue(v.has_title)

    def test_axis_label_offset(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        h = chart.axes.horizontal_axis
        h.label_offset = 200
        self.assertEqual(h.label_offset, 200)

    def test_scatter_chart_has_two_value_axes(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.SCATTER_WITH_MARKERS, 50, 50, 500, 400)
        axes = chart.axes
        self.assertIsNotNone(axes.horizontal_axis)
        self.assertIsNotNone(axes.vertical_axis)

    def test_pie_chart_no_axes(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.PIE, 50, 50, 400, 400)
        axes = chart.axes
        self.assertIsNone(axes.horizontal_axis)
        self.assertIsNone(axes.vertical_axis)

    def test_axes_round_trip(self):
        """Set axis properties, save, reload, verify."""
        import tempfile, os
        from aspose.slides_foss.charts.TickMarkType import TickMarkType
        from aspose.slides_foss.export.SaveFormat import SaveFormat
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        v = chart.axes.vertical_axis
        v.max_value = 50.0
        v.min_value = -5.0
        v.major_unit = 10.0
        v.is_visible = False
        v.major_tick_mark = TickMarkType.OUTSIDE
        v.number_format = '#,##0'

        fd, path = tempfile.mkstemp(suffix='.pptx')
        os.close(fd)
        try:
            pres.save(path, SaveFormat.PPTX)
            pres2 = Presentation(path)
            chart2 = pres2.slides[0].shapes[0]
            v2 = chart2.axes.vertical_axis
            self.assertAlmostEqual(v2.max_value, 50.0)
            self.assertAlmostEqual(v2.min_value, -5.0)
            self.assertAlmostEqual(v2.major_unit, 10.0)
            self.assertFalse(v2.is_visible)
            self.assertEqual(v2.major_tick_mark, TickMarkType.OUTSIDE)
            self.assertEqual(v2.number_format, '#,##0')
        finally:
            os.unlink(path)


class TestSecondaryAxis(unittest.TestCase):
    """Tests for plot_on_second_axis and secondary axes."""

    def test_series_default_not_on_second_axis(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        s = chart.chart_data.series[0]
        self.assertFalse(s.plot_on_second_axis)

    def test_set_plot_on_second_axis(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        s = chart.chart_data.series[0]
        s.plot_on_second_axis = True
        self.assertTrue(s.plot_on_second_axis)

    def test_secondary_vertical_axis_created(self):
        from aspose.slides_foss.charts.AxisPositionType import AxisPositionType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.chart_data.series[0].plot_on_second_axis = True
        # Need to re-create axes manager since XML changed
        chart._axes_manager = None
        axes = chart.axes
        self.assertIsNotNone(axes.secondary_vertical_axis)
        self.assertEqual(axes.secondary_vertical_axis.position, AxisPositionType.RIGHT)

    def test_secondary_axis_round_trip(self):
        """Set plot_on_second_axis, save, reload, verify."""
        import tempfile, os
        from aspose.slides_foss.export.SaveFormat import SaveFormat
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.chart_data.series[0].plot_on_second_axis = True

        fd, path = tempfile.mkstemp(suffix='.pptx')
        os.close(fd)
        try:
            pres.save(path, SaveFormat.PPTX)
            pres2 = Presentation(path)
            chart2 = pres2.slides[0].shapes[0]
            # Series order may differ after reload; find by name
            moved = None
            for s in chart2.chart_data.series:
                if s.name.as_literal_string == 'Series 1':
                    moved = s
                    break
            self.assertIsNotNone(moved, "Series 1 not found after reload")
            self.assertTrue(moved.plot_on_second_axis)
            # Other series should remain on primary
            for s in chart2.chart_data.series:
                if s.name.as_literal_string != 'Series 1':
                    self.assertFalse(s.plot_on_second_axis)
        finally:
            os.unlink(path)

    def test_series_group_plot_on_second_axis(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.chart_data.series[0].plot_on_second_axis = True
        groups = chart.chart_data.series_groups
        # Should have at least one group with plot_on_second_axis=True
        second_groups = [g for g in groups if g.plot_on_second_axis]
        self.assertTrue(len(second_groups) > 0)

    def test_move_series_back_to_primary(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        s = chart.chart_data.series[0]
        s.plot_on_second_axis = True
        self.assertTrue(s.plot_on_second_axis)
        s.plot_on_second_axis = False
        self.assertFalse(s.plot_on_second_axis)

    def test_series_on_second_axis_not_in_primary_group(self):
        """A series moved to secondary axis must NOT appear in the primary group."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.chart_data.series[0].plot_on_second_axis = True
        groups = chart.chart_data.series_groups
        primary_groups = [g for g in groups if not g.plot_on_second_axis]
        secondary_groups = [g for g in groups if g.plot_on_second_axis]
        self.assertEqual(len(primary_groups), 1)
        self.assertEqual(len(secondary_groups), 1)
        # Primary group has 2 series, secondary has 1
        self.assertEqual(len(primary_groups[0].series), 2)
        self.assertEqual(len(secondary_groups[0].series), 1)
        # No series appears in both groups
        primary_names = {s.name.as_literal_string for i in range(len(primary_groups[0].series))
                         for s in [primary_groups[0].series[i]]}
        secondary_names = {s.name.as_literal_string for i in range(len(secondary_groups[0].series))
                           for s in [secondary_groups[0].series[i]]}
        self.assertEqual(primary_names & secondary_names, set())

    def test_all_series_in_group_reflect_second_axis(self):
        """All series within a secondary group must report plot_on_second_axis=True."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        # Move two series to secondary
        chart.chart_data.series[0].plot_on_second_axis = True
        chart.chart_data.series[1].plot_on_second_axis = True
        groups = chart.chart_data.series_groups
        secondary_groups = [g for g in groups if g.plot_on_second_axis]
        self.assertEqual(len(secondary_groups), 1)
        for i in range(len(secondary_groups[0].series)):
            s = secondary_groups[0].series[i]
            self.assertTrue(s.plot_on_second_axis,
                            f'{s.name.as_literal_string} should be on second axis')

    def test_same_type_different_axes_form_separate_groups(self):
        """Same chart type on primary vs secondary axis → two separate groups."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.chart_data.series[0].plot_on_second_axis = True
        groups = chart.chart_data.series_groups
        self.assertEqual(len(groups), 2)
        # Both groups are bar/column type
        self.assertEqual(groups[0].type, groups[1].type)
        # But on different axes
        self.assertNotEqual(groups[0].plot_on_second_axis, groups[1].plot_on_second_axis)

    def test_move_all_series_to_second_axis_collapses_groups(self):
        """Moving all series to secondary should result in one secondary group."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        for s in chart.chart_data.series:
            s.plot_on_second_axis = True
        groups = chart.chart_data.series_groups
        # All series in one group on secondary axis
        self.assertEqual(len(groups), 1)
        self.assertTrue(groups[0].plot_on_second_axis)
        self.assertEqual(len(groups[0].series), 3)

    def test_series_group_readonly_reflects_individual_series(self):
        """Group's read-only plot_on_second_axis reflects all its series."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        s0 = chart.chart_data.series[0]
        # Initially all on primary
        grp = s0.parent_series_group
        self.assertFalse(grp.plot_on_second_axis)
        # Move one series — group splits
        s0.plot_on_second_axis = True
        new_grp = s0.parent_series_group
        self.assertTrue(new_grp.plot_on_second_axis)

    # ------------------------------------------------------------------ #
    #  Chart Title
    # ------------------------------------------------------------------ #

    def test_chart_title_basic(self):
        """Chart title can be created with text."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        self.assertFalse(chart.has_title)
        chart.has_title = True
        self.assertTrue(chart.has_title)
        chart.chart_title.add_text_frame_for_overriding('')
        tf = chart.chart_title.text_frame_for_overriding
        self.assertIsNotNone(tf)
        portion = tf.paragraphs[0].portions[0]
        portion.text = 'My Chart Title'
        self.assertEqual(chart.chart_title.text_frame_for_overriding.paragraphs[0].portions[0].text,
                         'My Chart Title')

    def test_chart_title_overlay(self):
        """Chart title overlay defaults to True after add_text_frame_for_overriding."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_title = True
        chart.chart_title.add_text_frame_for_overriding('Test')
        self.assertTrue(chart.chart_title.overlay)
        chart.chart_title.overlay = False
        self.assertFalse(chart.chart_title.overlay)

    def test_chart_title_formatting(self):
        """Chart title text can be formatted."""
        from aspose.slides_foss import FillType, NullableBool
        from aspose.slides_foss.drawing import Color
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_title = True
        chart.chart_title.add_text_frame_for_overriding('')
        portion = chart.chart_title.text_frame_for_overriding.paragraphs[0].portions[0]
        portion.text = 'Styled Title'
        portion.portion_format.fill_format.fill_type = FillType.SOLID
        portion.portion_format.fill_format.solid_fill_color.color = Color.gray
        portion.portion_format.font_height = 20
        portion.portion_format.font_bold = NullableBool.TRUE
        portion.portion_format.font_italic = NullableBool.TRUE
        # Verify
        pf = portion.portion_format
        self.assertEqual(pf.font_height, 20)
        self.assertEqual(pf.font_bold, NullableBool.TRUE)
        self.assertEqual(pf.font_italic, NullableBool.TRUE)

    def test_chart_title_remove(self):
        """Setting has_title to False removes the title."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_title = True
        chart.chart_title.add_text_frame_for_overriding('Title')
        self.assertTrue(chart.has_title)
        chart.has_title = False
        self.assertFalse(chart.has_title)

    def test_axis_title_vertical(self):
        """Vertical axis title can be set."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        v = chart.axes.vertical_axis
        v.has_title = True
        v.title.add_text_frame_for_overriding('')
        portion = v.title.text_frame_for_overriding.paragraphs[0].portions[0]
        portion.text = 'Value Axis'
        self.assertEqual(v.title.text_frame_for_overriding.paragraphs[0].portions[0].text,
                         'Value Axis')

    def test_axis_title_horizontal(self):
        """Horizontal axis title can be set."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        h = chart.axes.horizontal_axis
        h.has_title = True
        h.title.add_text_frame_for_overriding('')
        portion = h.title.text_frame_for_overriding.paragraphs[0].portions[0]
        portion.text = 'Category Axis'
        self.assertEqual(h.title.text_frame_for_overriding.paragraphs[0].portions[0].text,
                         'Category Axis')

    def test_chart_title_round_trip(self):
        """Chart title survives save/reload."""
        import tempfile, os
        from aspose.slides_foss import FillType, NullableBool
        from aspose.slides_foss.drawing import Color
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_title = True
        chart.chart_title.add_text_frame_for_overriding('')
        portion = chart.chart_title.text_frame_for_overriding.paragraphs[0].portions[0]
        portion.text = 'Round Trip Title'
        portion.portion_format.font_height = 18
        portion.portion_format.font_bold = NullableBool.TRUE

        # Axis titles
        chart.axes.vertical_axis.has_title = True
        chart.axes.vertical_axis.title.add_text_frame_for_overriding('')
        chart.axes.vertical_axis.title.text_frame_for_overriding.paragraphs[0].portions[0].text = 'Y Axis'

        chart.axes.horizontal_axis.has_title = True
        chart.axes.horizontal_axis.title.add_text_frame_for_overriding('')
        chart.axes.horizontal_axis.title.text_frame_for_overriding.paragraphs[0].portions[0].text = 'X Axis'

        fd, path = tempfile.mkstemp(suffix='.pptx')
        os.close(fd)
        try:
            from aspose.slides_foss.export import SaveFormat
            pres.save(path, SaveFormat.PPTX)
            pres2 = Presentation(path)
            chart2 = pres2.slides[0].shapes[0]
            self.assertTrue(chart2.has_title)
            self.assertEqual(
                chart2.chart_title.text_frame_for_overriding.paragraphs[0].portions[0].text,
                'Round Trip Title')
            self.assertEqual(
                chart2.axes.vertical_axis.title.text_frame_for_overriding.paragraphs[0].portions[0].text,
                'Y Axis')
            self.assertEqual(
                chart2.axes.horizontal_axis.title.text_frame_for_overriding.paragraphs[0].portions[0].text,
                'X Axis')
        finally:
            os.unlink(path)

    def test_axis_title_rotation(self):
        """Axis title rotation is stored on bodyPr rot attribute."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        # Vertical axis: -90 degrees
        v = chart.axes.vertical_axis
        v.has_title = True
        v.title.add_text_frame_for_overriding('')
        v.title.text_frame_for_overriding.paragraphs[0].portions[0].text = 'Y Axis'
        v.title.text_frame_for_overriding.text_frame_format.rotation_angle = -90
        self.assertAlmostEqual(
            v.title.text_frame_for_overriding.text_frame_format.rotation_angle, -90.0)
        # Horizontal axis: 45 degrees
        h = chart.axes.horizontal_axis
        h.has_title = True
        h.title.add_text_frame_for_overriding('')
        h.title.text_frame_for_overriding.paragraphs[0].portions[0].text = 'X Axis'
        h.title.text_frame_for_overriding.text_frame_format.rotation_angle = 45
        self.assertAlmostEqual(
            h.title.text_frame_for_overriding.text_frame_format.rotation_angle, 45.0)

    def test_axis_title_rotation_round_trip(self):
        """Axis title rotation survives save/reload."""
        import tempfile, os
        from aspose.slides_foss.export import SaveFormat
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.axes.vertical_axis.has_title = True
        chart.axes.vertical_axis.title.add_text_frame_for_overriding('')
        chart.axes.vertical_axis.title.text_frame_for_overriding.paragraphs[0].portions[0].text = 'Y'
        chart.axes.vertical_axis.title.text_frame_for_overriding.text_frame_format.rotation_angle = -90
        chart.axes.horizontal_axis.has_title = True
        chart.axes.horizontal_axis.title.add_text_frame_for_overriding('')
        chart.axes.horizontal_axis.title.text_frame_for_overriding.paragraphs[0].portions[0].text = 'X'
        chart.axes.horizontal_axis.title.text_frame_for_overriding.text_frame_format.rotation_angle = 45

        fd, path = tempfile.mkstemp(suffix='.pptx')
        os.close(fd)
        try:
            pres.save(path, SaveFormat.PPTX)
            pres2 = Presentation(path)
            chart2 = pres2.slides[0].shapes[0]
            self.assertAlmostEqual(
                chart2.axes.vertical_axis.title.text_frame_for_overriding.text_frame_format.rotation_angle,
                -90.0)
            self.assertAlmostEqual(
                chart2.axes.horizontal_axis.title.text_frame_for_overriding.text_frame_format.rotation_angle,
                45.0)
        finally:
            os.unlink(path)

    def test_chart_title_overlay_false_means_no_overlap(self):
        """overlay=False means the title takes space above the plot area."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_title = True
        chart.chart_title.add_text_frame_for_overriding('Title')
        # Default overlay after add_text_frame_for_overriding is True
        self.assertTrue(chart.chart_title.overlay)
        # Set to False (title takes its own space, doesn't overlap plot)
        chart.chart_title.overlay = False
        self.assertFalse(chart.chart_title.overlay)

    def test_chart_title_overlay_round_trip(self):
        """Chart title overlay setting survives save/reload."""
        import tempfile, os
        from aspose.slides_foss.export import SaveFormat
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_title = True
        chart.chart_title.add_text_frame_for_overriding('Title')
        chart.chart_title.overlay = False

        fd, path = tempfile.mkstemp(suffix='.pptx')
        os.close(fd)
        try:
            pres.save(path, SaveFormat.PPTX)
            pres2 = Presentation(path)
            chart2 = pres2.slides[0].shapes[0]
            self.assertFalse(chart2.chart_title.overlay)
        finally:
            os.unlink(path)

    def test_chart_title_layout_position(self):
        """Chart title custom position (x, y, width, height)."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_title = True
        chart.chart_title.add_text_frame_for_overriding('Positioned')
        chart.chart_title.x = 0.1
        chart.chart_title.y = 0.05
        chart.chart_title.width = 0.5
        chart.chart_title.height = 0.1
        self.assertAlmostEqual(chart.chart_title.x, 0.1)
        self.assertAlmostEqual(chart.chart_title.y, 0.05)
        self.assertAlmostEqual(chart.chart_title.width, 0.5)
        self.assertAlmostEqual(chart.chart_title.height, 0.1)
        self.assertAlmostEqual(chart.chart_title.right, 0.6)
        self.assertAlmostEqual(chart.chart_title.bottom, 0.15)

    def test_chart_title_layout_round_trip(self):
        """Chart title layout survives save/reload."""
        import tempfile, os
        from aspose.slides_foss.export import SaveFormat
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_title = True
        chart.chart_title.add_text_frame_for_overriding('Positioned')
        chart.chart_title.x = 0.2
        chart.chart_title.y = 0.03
        chart.chart_title.width = 0.6
        chart.chart_title.height = 0.08

        fd, path = tempfile.mkstemp(suffix='.pptx')
        os.close(fd)
        try:
            pres.save(path, SaveFormat.PPTX)
            pres2 = Presentation(path)
            chart2 = pres2.slides[0].shapes[0]
            self.assertAlmostEqual(chart2.chart_title.x, 0.2)
            self.assertAlmostEqual(chart2.chart_title.y, 0.03)
            self.assertAlmostEqual(chart2.chart_title.width, 0.6)
            self.assertAlmostEqual(chart2.chart_title.height, 0.08)
        finally:
            os.unlink(path)

    def test_axis_title_layout_position(self):
        """Axis titles support custom position."""
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        v = chart.axes.vertical_axis
        v.has_title = True
        v.title.add_text_frame_for_overriding('')
        v.title.text_frame_for_overriding.paragraphs[0].portions[0].text = 'Y'
        v.title.x = 0.02
        v.title.y = 0.3
        v.title.width = 0.05
        v.title.height = 0.4
        self.assertAlmostEqual(v.title.x, 0.02)
        self.assertAlmostEqual(v.title.y, 0.3)
        self.assertAlmostEqual(v.title.width, 0.05)
        self.assertAlmostEqual(v.title.height, 0.4)

        h = chart.axes.horizontal_axis
        h.has_title = True
        h.title.add_text_frame_for_overriding('')
        h.title.text_frame_for_overriding.paragraphs[0].portions[0].text = 'X'
        h.title.x = 0.3
        h.title.y = 0.9
        h.title.width = 0.4
        h.title.height = 0.05
        self.assertAlmostEqual(h.title.x, 0.3)
        self.assertAlmostEqual(h.title.y, 0.9)
        self.assertAlmostEqual(h.title.width, 0.4)
        self.assertAlmostEqual(h.title.height, 0.05)

    def test_axis_title_layout_round_trip(self):
        """Axis title layout survives save/reload."""
        import tempfile, os
        from aspose.slides_foss.export import SaveFormat
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        v = chart.axes.vertical_axis
        v.has_title = True
        v.title.add_text_frame_for_overriding('')
        v.title.text_frame_for_overriding.paragraphs[0].portions[0].text = 'Y'
        v.title.x = 0.01
        v.title.y = 0.25
        v.title.width = 0.04
        v.title.height = 0.5

        h = chart.axes.horizontal_axis
        h.has_title = True
        h.title.add_text_frame_for_overriding('')
        h.title.text_frame_for_overriding.paragraphs[0].portions[0].text = 'X'
        h.title.x = 0.25
        h.title.y = 0.92
        h.title.width = 0.5
        h.title.height = 0.06

        fd, path = tempfile.mkstemp(suffix='.pptx')
        os.close(fd)
        try:
            pres.save(path, SaveFormat.PPTX)
            pres2 = Presentation(path)
            chart2 = pres2.slides[0].shapes[0]
            self.assertAlmostEqual(chart2.axes.vertical_axis.title.x, 0.01)
            self.assertAlmostEqual(chart2.axes.vertical_axis.title.y, 0.25)
            self.assertAlmostEqual(chart2.axes.vertical_axis.title.width, 0.04)
            self.assertAlmostEqual(chart2.axes.vertical_axis.title.height, 0.5)
            self.assertAlmostEqual(chart2.axes.horizontal_axis.title.x, 0.25)
            self.assertAlmostEqual(chart2.axes.horizontal_axis.title.y, 0.92)
            self.assertAlmostEqual(chart2.axes.horizontal_axis.title.width, 0.5)
            self.assertAlmostEqual(chart2.axes.horizontal_axis.title.height, 0.06)
        finally:
            os.unlink(path)


class TestLegend(unittest.TestCase):
    """Tests for Chart.legend properties."""

    def _save_and_reload(self, pres):
        import tempfile
        from aspose.slides_foss.export.SaveFormat import SaveFormat
        fd, path = tempfile.mkstemp(suffix='.pptx')
        os.close(fd)
        try:
            pres.save(path, SaveFormat.PPTX)
            return Presentation(path)
        finally:
            os.unlink(path)

    def test_has_legend_default(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        self.assertTrue(chart.has_legend)

    def test_toggle_has_legend(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_legend = False
        self.assertFalse(chart.has_legend)
        chart.has_legend = True
        self.assertTrue(chart.has_legend)

    def test_legend_object_returned(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        legend = chart.legend
        self.assertIsNotNone(legend)

    def test_legend_position_default(self):
        from aspose.slides_foss.charts.LegendPositionType import LegendPositionType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        self.assertEqual(chart.legend.position, LegendPositionType.BOTTOM)

    def test_legend_position_set(self):
        from aspose.slides_foss.charts.LegendPositionType import LegendPositionType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.legend.position = LegendPositionType.RIGHT
        self.assertEqual(chart.legend.position, LegendPositionType.RIGHT)

    def test_legend_position_all_values(self):
        from aspose.slides_foss.charts.LegendPositionType import LegendPositionType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        for pos in LegendPositionType:
            chart.legend.position = pos
            self.assertEqual(chart.legend.position, pos)

    def test_legend_overlay_default(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        self.assertFalse(chart.legend.overlay)

    def test_legend_overlay_set(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.legend.overlay = True
        self.assertTrue(chart.legend.overlay)
        chart.legend.overlay = False
        self.assertFalse(chart.legend.overlay)

    def test_legend_format(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        fmt = chart.legend.format
        self.assertIsNotNone(fmt)
        self.assertIsNotNone(fmt.fill)
        self.assertIsNotNone(fmt.line)

    def test_legend_text_format(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        tf = chart.legend.text_format
        self.assertIsNotNone(tf)
        pf = tf.portion_format
        self.assertIsNotNone(pf)

    def test_legend_text_format_font_height(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.legend.text_format.portion_format.font_height = 20
        self.assertAlmostEqual(chart.legend.text_format.portion_format.font_height, 20)

    def test_legend_layout_xy(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.legend.x = 0.1
        chart.legend.y = 0.2
        self.assertAlmostEqual(chart.legend.x, 0.1)
        self.assertAlmostEqual(chart.legend.y, 0.2)

    def test_legend_layout_width_height(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.legend.width = 0.3
        chart.legend.height = 0.4
        self.assertAlmostEqual(chart.legend.width, 0.3)
        self.assertAlmostEqual(chart.legend.height, 0.4)

    def test_legend_right_bottom(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.legend.x = 0.1
        chart.legend.y = 0.2
        chart.legend.width = 0.3
        chart.legend.height = 0.4
        self.assertAlmostEqual(chart.legend.right, 0.4)
        self.assertAlmostEqual(chart.legend.bottom, 0.6)

    def test_legend_entries_count(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        entries = chart.legend.entries
        # Default chart has 3 series
        self.assertEqual(entries.count, 3)

    def test_legend_entry_hide(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        entry = chart.legend.entries[1]
        self.assertFalse(entry.hide)
        entry.hide = True
        self.assertTrue(entry.hide)
        entry.hide = False
        self.assertFalse(entry.hide)

    def test_legend_entry_text_format(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        tf = chart.legend.entries[0].text_format
        self.assertIsNotNone(tf)
        tf.portion_format.font_height = 14
        self.assertAlmostEqual(chart.legend.entries[0].text_format.portion_format.font_height, 14)

    def test_legend_chart_back_reference(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        self.assertIs(chart.legend.chart, chart)

    def test_legend_round_trip_position(self):
        from aspose.slides_foss.charts.LegendPositionType import LegendPositionType
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.legend.position = LegendPositionType.TOP_RIGHT
        chart.legend.overlay = True

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertTrue(chart2.has_legend)
        self.assertEqual(chart2.legend.position, LegendPositionType.TOP_RIGHT)
        self.assertTrue(chart2.legend.overlay)

    def test_legend_round_trip_layout(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.legend.x = 0.15
        chart.legend.y = 0.25
        chart.legend.width = 0.35
        chart.legend.height = 0.45

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertAlmostEqual(chart2.legend.x, 0.15)
        self.assertAlmostEqual(chart2.legend.y, 0.25)
        self.assertAlmostEqual(chart2.legend.width, 0.35)
        self.assertAlmostEqual(chart2.legend.height, 0.45)

    def test_legend_round_trip_entry_hide(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.legend.entries[1].hide = True

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertFalse(chart2.legend.entries[0].hide)
        self.assertTrue(chart2.legend.entries[1].hide)
        self.assertFalse(chart2.legend.entries[2].hide)

    def test_legend_round_trip_text_format(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.legend.text_format.portion_format.font_height = 18

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertAlmostEqual(chart2.legend.text_format.portion_format.font_height, 18)

    def test_legend_removed_round_trip(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.has_legend = False

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertFalse(chart2.has_legend)

    def test_legend_fill_format(self):
        from aspose.slides_foss.FillType import FillType
        from aspose.slides_foss.drawing import Color
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        chart.legend.format.fill.fill_type = FillType.SOLID
        chart.legend.format.fill.solid_fill_color.color = Color.light_gray

        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertEqual(chart2.legend.format.fill.fill_type, FillType.SOLID)


class TestChartProperties(unittest.TestCase):
    """Tests for Chart-level properties: display_blanks_as, plot_visible_cells_only,
    show_data_labels_over_maximum, has_rounded_corners, style, text_format,
    rotation_3d, back_wall, side_wall, floor, chart."""

    def _save_and_reload(self, pres):
        import tempfile, os
        from aspose.slides_foss.export.SaveFormat import SaveFormat
        f = tempfile.NamedTemporaryFile(suffix='.pptx', delete=False)
        f.close()
        try:
            pres.save(f.name, SaveFormat.PPTX)
            pres2 = Presentation(f.name)
            return pres2
        finally:
            os.unlink(f.name)

    def _make_chart(self):
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 500, 400)
        return pres, chart

    # ---- display_blanks_as ----

    def test_display_blanks_as_default(self):
        from aspose.slides_foss.charts.DisplayBlanksAsType import DisplayBlanksAsType
        _, chart = self._make_chart()
        self.assertEqual(chart.display_blanks_as, DisplayBlanksAsType.ZERO)

    def test_display_blanks_as_set_zero(self):
        from aspose.slides_foss.charts.DisplayBlanksAsType import DisplayBlanksAsType
        pres, chart = self._make_chart()
        chart.display_blanks_as = DisplayBlanksAsType.ZERO
        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertEqual(chart2.display_blanks_as, DisplayBlanksAsType.ZERO)

    def test_display_blanks_as_set_span(self):
        from aspose.slides_foss.charts.DisplayBlanksAsType import DisplayBlanksAsType
        pres, chart = self._make_chart()
        chart.display_blanks_as = DisplayBlanksAsType.SPAN
        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertEqual(chart2.display_blanks_as, DisplayBlanksAsType.SPAN)

    # ---- plot_visible_cells_only ----

    def test_plot_visible_cells_only_default(self):
        _, chart = self._make_chart()
        self.assertTrue(chart.plot_visible_cells_only)

    def test_plot_visible_cells_only_set_false(self):
        pres, chart = self._make_chart()
        chart.plot_visible_cells_only = False
        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertFalse(chart2.plot_visible_cells_only)

    # ---- show_data_labels_over_maximum ----

    def test_show_data_labels_over_maximum_default(self):
        _, chart = self._make_chart()
        # Default for newly created charts
        val = chart.show_data_labels_over_maximum
        self.assertIsInstance(val, bool)

    def test_show_data_labels_over_maximum_roundtrip(self):
        pres, chart = self._make_chart()
        chart.show_data_labels_over_maximum = True
        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertTrue(chart2.show_data_labels_over_maximum)

    # ---- has_rounded_corners ----

    def test_has_rounded_corners_default(self):
        _, chart = self._make_chart()
        self.assertIsInstance(chart.has_rounded_corners, bool)

    def test_has_rounded_corners_set_true(self):
        pres, chart = self._make_chart()
        chart.has_rounded_corners = True
        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertTrue(chart2.has_rounded_corners)

    def test_has_rounded_corners_set_false(self):
        pres, chart = self._make_chart()
        chart.has_rounded_corners = False
        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertFalse(chart2.has_rounded_corners)

    # ---- style ----

    def test_style_default(self):
        from aspose.slides_foss.charts.StyleType import StyleType
        _, chart = self._make_chart()
        self.assertIsInstance(chart.style, StyleType)

    def test_style_roundtrip(self):
        from aspose.slides_foss.charts.StyleType import StyleType
        pres, chart = self._make_chart()
        chart.style = StyleType.STYLE10
        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertEqual(chart2.style, StyleType.STYLE10)

    # ---- text_format ----

    def test_text_format_access(self):
        _, chart = self._make_chart()
        tf = chart.text_format
        self.assertIsNotNone(tf)
        pf = tf.portion_format
        self.assertIsNotNone(pf)

    # ---- rotation_3d ----

    def test_rotation_3d_defaults(self):
        _, chart = self._make_chart()
        r3d = chart.rotation_3d
        self.assertIsNotNone(r3d)
        self.assertIsInstance(r3d.rotation_x, int)
        self.assertIsInstance(r3d.rotation_y, int)
        self.assertIsInstance(r3d.perspective, int)
        self.assertIsInstance(r3d.right_angle_axes, bool)
        self.assertIsInstance(r3d.depth_percents, int)
        self.assertIsInstance(r3d.height_percents, int)

    def test_rotation_3d_roundtrip(self):
        pres, chart = self._make_chart()
        r3d = chart.rotation_3d
        r3d.rotation_x = 15
        r3d.rotation_y = 20
        r3d.perspective = 45
        r3d.right_angle_axes = False
        r3d.depth_percents = 150
        r3d.height_percents = 200
        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        r3d2 = chart2.rotation_3d
        self.assertEqual(r3d2.rotation_x, 15)
        self.assertEqual(r3d2.rotation_y, 20)
        self.assertEqual(r3d2.perspective, 45)
        self.assertFalse(r3d2.right_angle_axes)
        self.assertEqual(r3d2.depth_percents, 150)
        self.assertEqual(r3d2.height_percents, 200)

    # ---- walls and floor ----

    def test_back_wall_access(self):
        _, chart = self._make_chart()
        bw = chart.back_wall
        self.assertIsNotNone(bw)
        self.assertIsInstance(bw.thickness, int)
        self.assertIsNotNone(bw.format)

    def test_side_wall_access(self):
        _, chart = self._make_chart()
        sw = chart.side_wall
        self.assertIsNotNone(sw)
        self.assertIsInstance(sw.thickness, int)

    def test_floor_access(self):
        _, chart = self._make_chart()
        fl = chart.floor
        self.assertIsNotNone(fl)
        self.assertIsInstance(fl.thickness, int)

    def test_wall_thickness_roundtrip(self):
        pres, chart = self._make_chart()
        chart.back_wall.thickness = 25
        pres2 = self._save_and_reload(pres)
        chart2 = pres2.slides[0].shapes[0]
        self.assertEqual(chart2.back_wall.thickness, 25)

    # ---- chart (self-ref) ----

    def test_chart_self_reference(self):
        _, chart = self._make_chart()
        self.assertIs(chart.chart, chart)


class TestDataLabels(unittest.TestCase):
    """Tests for DataLabel, DataLabelCollection, DataLabelFormat."""

    def _save_and_reload(self, pres):
        import tempfile, os
        from aspose.slides_foss.export.SaveFormat import SaveFormat
        f = tempfile.NamedTemporaryFile(suffix='.pptx', delete=False)
        f.close()
        try:
            pres.save(f.name, SaveFormat.PPTX)
            pres2 = Presentation(f.name)
            return pres2
        finally:
            os.unlink(f.name)

    def _make_chart(self, chart_type=None):
        if chart_type is None:
            chart_type = ChartType.CLUSTERED_COLUMN
        pres = Presentation()
        chart = pres.slides[0].shapes.add_chart(chart_type, 50, 50, 500, 400)
        return pres, chart

    def test_labels_collection_exists(self):
        _, chart = self._make_chart()
        labels = chart.chart_data.series[0].labels
        self.assertIsNotNone(labels)
        self.assertEqual(labels.count, 4)
        self.assertIs(labels.parent_series, chart.chart_data.series[0])
        self.assertIs(labels.chart, chart)

    def test_default_show_value_roundtrip(self):
        pres, chart = self._make_chart()
        lf = chart.chart_data.series[0].labels.default_data_label_format
        lf.show_value = True
        lf.show_category_name = True
        pres2 = self._save_and_reload(pres)
        lf2 = pres2.slides[0].shapes[0].chart_data.series[0].labels.default_data_label_format
        self.assertTrue(lf2.show_value)
        self.assertTrue(lf2.show_category_name)
        self.assertFalse(lf2.show_percentage)

    def test_position_roundtrip(self):
        from aspose.slides_foss.charts import LegendDataLabelPosition
        pres, chart = self._make_chart()
        lf = chart.chart_data.series[0].labels.default_data_label_format
        lf.position = LegendDataLabelPosition.OUTSIDE_END
        pres2 = self._save_and_reload(pres)
        lf2 = pres2.slides[0].shapes[0].chart_data.series[0].labels.default_data_label_format
        self.assertEqual(lf2.position, LegendDataLabelPosition.OUTSIDE_END)

    def test_separator_roundtrip(self):
        pres, chart = self._make_chart()
        lf = chart.chart_data.series[0].labels.default_data_label_format
        lf.separator = ' | '
        pres2 = self._save_and_reload(pres)
        lf2 = pres2.slides[0].shapes[0].chart_data.series[0].labels.default_data_label_format
        self.assertEqual(lf2.separator, ' | ')

    def test_number_format_roundtrip(self):
        pres, chart = self._make_chart()
        lf = chart.chart_data.series[0].labels.default_data_label_format
        lf.number_format = '0.00%'
        lf.is_number_format_linked_to_source = False
        pres2 = self._save_and_reload(pres)
        lf2 = pres2.slides[0].shapes[0].chart_data.series[0].labels.default_data_label_format
        self.assertEqual(lf2.number_format, '0.00%')
        self.assertFalse(lf2.is_number_format_linked_to_source)

    def test_per_point_label_override(self):
        pres, chart = self._make_chart()
        dp0 = chart.chart_data.series[0].data_points[0]
        lbl = dp0.label
        lbl.data_label_format.show_value = True
        lbl.x = 0.1
        lbl.y = 0.2
        lbl.add_text_frame_for_overriding('Peak')
        pres2 = self._save_and_reload(pres)
        dp0_r = pres2.slides[0].shapes[0].chart_data.series[0].data_points[0]
        self.assertTrue(dp0_r.label.data_label_format.show_value)
        self.assertAlmostEqual(dp0_r.label.x, 0.1, places=4)
        self.assertAlmostEqual(dp0_r.label.y, 0.2, places=4)
        self.assertEqual(dp0_r.label.get_actual_label_text(), 'Peak')

    def test_layout_width_height(self):
        pres, chart = self._make_chart()
        lbl = chart.chart_data.series[0].data_points[1].label
        lbl.x = 0.05
        lbl.y = 0.1
        lbl.width = 0.15
        lbl.height = 0.08
        pres2 = self._save_and_reload(pres)
        lbl2 = pres2.slides[0].shapes[0].chart_data.series[0].data_points[1].label
        self.assertAlmostEqual(lbl2.width, 0.15, places=4)
        self.assertAlmostEqual(lbl2.height, 0.08, places=4)
        self.assertAlmostEqual(lbl2.right, 0.05 + 0.15, places=4)
        self.assertAlmostEqual(lbl2.bottom, 0.1 + 0.08, places=4)

    def test_leader_lines_format(self):
        pres, chart = self._make_chart(ChartType.PIE)
        labels = chart.chart_data.series[0].labels
        labels.default_data_label_format.show_leader_lines = True
        ll = labels.leader_lines_format
        self.assertIsNotNone(ll)
        self.assertIsNotNone(ll.line)
        pres2 = self._save_and_reload(pres)
        labels2 = pres2.slides[0].shapes[0].chart_data.series[0].labels
        self.assertTrue(labels2.default_data_label_format.show_leader_lines)

    def test_show_label_value_from_cell(self):
        pres, chart = self._make_chart()
        lf = chart.chart_data.series[0].labels.default_data_label_format
        lf.show_label_value_from_cell = True
        pres2 = self._save_and_reload(pres)
        lf2 = pres2.slides[0].shapes[0].chart_data.series[0].labels.default_data_label_format
        self.assertTrue(lf2.show_label_value_from_cell)

    def test_hide_collection(self):
        pres, chart = self._make_chart()
        labels = chart.chart_data.series[0].labels
        labels.default_data_label_format.show_value = True
        labels.hide()
        self.assertFalse(labels.is_visible)

    def test_per_point_hide(self):
        _, chart = self._make_chart()
        lbl = chart.chart_data.series[0].data_points[0].label
        lbl.hide()
        # After hide, a <c:delete val='1'/> is present on the <c:dLbl>.
        c_ns = 'http://schemas.openxmlformats.org/drawingml/2006/chart'
        self.assertIsNotNone(lbl._elem.find('{' + c_ns + '}delete'))

    def test_is_visible_reflects_flags(self):
        _, chart = self._make_chart()
        labels = chart.chart_data.series[0].labels
        self.assertFalse(labels.is_visible)
        labels.default_data_label_format.show_value = True
        self.assertTrue(labels.is_visible)


if __name__ == '__main__':
    unittest.main()
