"""Tests for saving presentations in Markdown format."""
import io
import os

import pytest

from aspose.slides_foss import (
    BulletType, NullableBool, Presentation, ShapeType, TextAlignment,
    TextStrikethroughType, TextUnderlineType,
)
from aspose.slides_foss.charts import ChartType
from aspose.slides_foss.drawing import PointF
from aspose.slides_foss.export import (
    Flavor, HandleRepeatedSpaces, MarkdownExportType, MarkdownSaveOptions,
    NewLineType, SaveFormat,
)


def unix_options(**kwargs):
    options = MarkdownSaveOptions()
    options.new_line_type = NewLineType.UNIX
    for name, value in kwargs.items():
        setattr(options, name, value)
    return options


def export_md(pres, options=None, slides=None):
    buf = io.BytesIO()
    if slides is not None:
        pres.save(buf, slides, SaveFormat.MD, options if options is not None else unix_options())
    else:
        pres.save(buf, SaveFormat.MD, options if options is not None else unix_options())
    return buf.getvalue().decode('utf-8')


def add_text_box(slide, text, x=50, y=50, w=400, h=100):
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, x, y, w, h)
    shape.text_frame.text = text
    return shape


# ---------------------------------------------------------------
# Options
# ---------------------------------------------------------------

def test_options_defaults():
    options = MarkdownSaveOptions()
    assert options.export_type == MarkdownExportType.TEXT_ONLY
    assert options.flavor == Flavor.DEFAULT
    assert options.handle_repeated_spaces == HandleRepeatedSpaces.ALTERNATE_SPACES_TO_NBSP
    assert options.remove_empty_lines is False
    assert options.show_comments is False
    assert options.show_hidden_slides is False
    assert options.show_slide_number is False
    assert options.slide_number_format == '# {0}'


def test_slide_number_format_validation():
    options = MarkdownSaveOptions()
    with pytest.raises(ValueError):
        options.slide_number_format = ''
    with pytest.raises(ValueError):
        options.slide_number_format = None
    with pytest.raises(ValueError):
        options.slide_number_format = '# Slide'
    options.slide_number_format = '## Slide {0}'
    assert options.slide_number_format == '## Slide {0}'


# ---------------------------------------------------------------
# Basic output
# ---------------------------------------------------------------

def test_basic_text_export():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'Hello world')
        assert export_md(pres) == '---  \n\nHello world  \n'


def test_default_new_line_is_windows():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'Hello')
        buf = io.BytesIO()
        pres.save(buf, SaveFormat.MD)
        assert buf.getvalue().decode('utf-8') == '---  \r\n\r\nHello  \r\n'


def test_new_line_type_mac():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'Hello')
        md = export_md(pres, unix_options(new_line_type=NewLineType.MAC))
        assert md == '---  \r\rHello  \r'


def test_save_to_file_path(tmp_path):
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'Hello file')
        path = str(tmp_path / 'out.md')
        pres.save(path, SaveFormat.MD, unix_options())
        with open(path, encoding='utf-8') as f:
            assert f.read() == '---  \n\nHello file  \n'


def test_save_without_options():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'Hello')
        buf = io.BytesIO()
        pres.save(buf, SaveFormat.MD)
        assert 'Hello' in buf.getvalue().decode('utf-8')


# ---------------------------------------------------------------
# Character formatting
# ---------------------------------------------------------------

def _format_first_portion(shape):
    return shape.text_frame.paragraphs[0].portions[0].portion_format


def test_bold_italic():
    with Presentation() as pres:
        shape = add_text_box(pres.slides[0], 'Bold text')
        _format_first_portion(shape).font_bold = NullableBool.TRUE
        shape2 = add_text_box(pres.slides[0], 'Italic text', y=200)
        _format_first_portion(shape2).font_italic = NullableBool.TRUE
        md = export_md(pres)
        assert '**Bold text**' in md
        assert '*Italic text*' in md


def test_strikethrough_and_underline_default_flavor():
    with Presentation() as pres:
        shape = add_text_box(pres.slides[0], 'Struck')
        _format_first_portion(shape).strikethrough_type = TextStrikethroughType.SINGLE
        shape2 = add_text_box(pres.slides[0], 'Underlined', y=200)
        _format_first_portion(shape2).font_underline = TextUnderlineType.SINGLE
        md = export_md(pres)
        assert '~~Struck~~' in md
        assert '{==Underlined==}' in md


def test_underline_disabled_in_github_flavor():
    with Presentation() as pres:
        shape = add_text_box(pres.slides[0], 'Underlined')
        _format_first_portion(shape).font_underline = TextUnderlineType.SINGLE
        md = export_md(pres, unix_options(flavor=Flavor.GITHUB))
        assert '{==' not in md
        assert 'Underlined' in md


def test_xwiki_flavor_italic():
    with Presentation() as pres:
        shape = add_text_box(pres.slides[0], 'Italic')
        _format_first_portion(shape).font_italic = NullableBool.TRUE
        md = export_md(pres, unix_options(flavor=Flavor.X_WIKI))
        assert '//Italic//' in md


# ---------------------------------------------------------------
# Escaping and spaces
# ---------------------------------------------------------------

def test_reserved_chars_are_escaped():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'a*b `code` c|d')
        md = export_md(pres)
        assert 'a\\*b \\`code\\` c\\|d' in md


def test_repeated_spaces_alternate():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'a  b')
        md = export_md(pres)
        assert 'a &nbsp;b' in md


def test_repeated_spaces_none():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'a  b')
        md = export_md(pres, unix_options(handle_repeated_spaces=HandleRepeatedSpaces.NONE))
        assert 'a  b' in md


def test_repeated_spaces_multiple_to_nbsp():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'a   b')
        md = export_md(pres, unix_options(handle_repeated_spaces=HandleRepeatedSpaces.MULTIPLE_SPACES_TO_NBSP))
        assert 'a &nbsp;&nbsp;b' in md


# ---------------------------------------------------------------
# Paragraphs, lists, headings
# ---------------------------------------------------------------

def test_multiple_paragraphs():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'First\nSecond')
        md = export_md(pres)
        assert 'First  \nSecond' in md


def test_empty_paragraph_produces_nbsp_line():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'First\n\nThird')
        md = export_md(pres)
        assert '&nbsp;' in md


def test_remove_empty_lines():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'First\n\nThird')
        md = export_md(pres, unix_options(remove_empty_lines=True))
        assert '&nbsp;' not in md
        assert 'First' in md
        assert 'Third' in md


def test_unordered_and_ordered_lists():
    with Presentation() as pres:
        shape = add_text_box(pres.slides[0], 'Bullet item\nNumbered item')
        paragraphs = list(shape.text_frame.paragraphs)
        paragraphs[0].paragraph_format.bullet.type = BulletType.SYMBOL
        paragraphs[1].paragraph_format.bullet.type = BulletType.NUMBERED
        md = export_md(pres)
        assert '- Bullet item' in md
        assert '1. Numbered item' in md


def test_nested_list_depth():
    with Presentation() as pres:
        shape = add_text_box(pres.slides[0], 'Nested')
        paragraph = list(shape.text_frame.paragraphs)[0]
        paragraph.paragraph_format.bullet.type = BulletType.SYMBOL
        paragraph.paragraph_format.depth = 1
        md = export_md(pres)
        assert '    - Nested' in md


def test_title_and_subtitle_headings(test_data_dir):
    with Presentation(os.path.join(test_data_dir, 'title_slide.pptx')) as pres:
        md = export_md(pres)
        assert '# Presentation Title' in md
        assert '## Subtitle text' in md
        assert '# Body text' not in md


# ---------------------------------------------------------------
# Slides: numbers, hidden, subsets
# ---------------------------------------------------------------

def test_show_slide_number():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'Content')
        md = export_md(pres, unix_options(show_slide_number=True))
        assert md.startswith('\n---  \n# 1\n---  \n')


def test_custom_slide_number_format():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'Content')
        options = unix_options(show_slide_number=True)
        options.slide_number_format = '## Slide {0}'
        md = export_md(pres, options)
        assert '## Slide 1' in md


def test_hidden_slides_excluded_by_default():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'Visible')
        slide2 = pres.slides.add_empty_slide(pres.layout_slides[0])
        add_text_box(slide2, 'Hidden content')
        slide2.hidden = True
        md = export_md(pres)
        assert 'Visible' in md
        assert 'Hidden content' not in md

        md_all = export_md(pres, unix_options(show_hidden_slides=True))
        assert 'Hidden content' in md_all


def test_slides_array_selects_and_orders():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'One')
        slide2 = pres.slides.add_empty_slide(pres.layout_slides[0])
        add_text_box(slide2, 'Two')
        md = export_md(pres, slides=[2, 1])
        assert md.index('Two') < md.index('One')


def test_slides_array_duplicates():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'One')
        md = export_md(pres, slides=[1, 1])
        assert md.count('One') == 2


def test_slides_array_out_of_range():
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'One')
        with pytest.raises(ValueError):
            export_md(pres, slides=[2])
        with pytest.raises(ValueError):
            export_md(pres, slides=[0])


# ---------------------------------------------------------------
# Comments
# ---------------------------------------------------------------

def test_comments_shown_when_enabled():
    import datetime
    with Presentation() as pres:
        add_text_box(pres.slides[0], 'Content')
        author = pres.comment_authors.add_author('Alice', 'A')
        author.comments.add_comment('Review note', pres.slides[0], PointF(1.0, 1.0),
                                    datetime.datetime(2026, 1, 1, 12, 0, 0))
        md = export_md(pres)
        assert 'Review note' not in md

        md_with = export_md(pres, unix_options(show_comments=True))
        assert 'Alice: "Review note"' in md_with


# ---------------------------------------------------------------
# Tables
# ---------------------------------------------------------------

def _make_table_pres(pres):
    slide = pres.slides[0]
    table = slide.shapes.add_table(50, 50, [100, 100], [30, 30])
    table.rows[0][0].text_frame.text = 'H1'
    table.rows[0][1].text_frame.text = 'H2'
    table.rows[1][0].text_frame.text = 'C1'
    table.rows[1][1].text_frame.text = 'C2'
    return table


def test_table_export():
    with Presentation() as pres:
        _make_table_pres(pres)
        md = export_md(pres)
        assert '|H1|H2|' in md
        assert '|-|-|' in md
        assert '|C1|C2|' in md


def test_table_column_alignment():
    with Presentation() as pres:
        table = _make_table_pres(pres)
        for row in table.rows:
            for paragraph in row[1].text_frame.paragraphs:
                paragraph.paragraph_format.alignment = TextAlignment.CENTER
        md = export_md(pres)
        assert '|-|:-:|' in md


def test_table_dropped_in_flavor_without_tables():
    with Presentation() as pres:
        _make_table_pres(pres)
        md = export_md(pres, unix_options(flavor=Flavor.COMMON_MARK))
        assert 'H1' not in md


# ---------------------------------------------------------------
# Charts
# ---------------------------------------------------------------

def test_regular_chart_export():
    with Presentation() as pres:
        slide = pres.slides[0]
        chart = slide.shapes.add_chart(ChartType.CLUSTERED_COLUMN, 100, 100, 500, 400)
        cd = chart.chart_data
        wb = cd.chart_data_workbook
        cd.series.clear()
        cd.categories.clear()
        cd.categories.add(wb.get_cell(0, 1, 0, 'Q1'))
        cd.categories.add(wb.get_cell(0, 2, 0, 'Q2'))
        series = cd.series.add(wb.get_cell(0, 0, 1, 'Revenue'), chart.type)
        series.data_points.add_data_point_for_bar_series(wb.get_cell(0, 1, 1, 100))
        series.data_points.add_data_point_for_bar_series(wb.get_cell(0, 2, 1, 200))

        md = export_md(pres)
        assert '### ClusteredColumn chart' in md
        assert '||Revenue|' in md
        assert '|-|-|' in md
        assert '|Q1|100|' in md
        assert '|Q2|200|' in md


def test_chart_with_literal_data_export(test_data_dir):
    # Values stored as <c:numLit> and numeric categories must export like any
    # other chart data (this is how some real-world generators write charts).
    with Presentation(os.path.join(test_data_dir, 'chart_numlit.pptx')) as pres:
        md = export_md(pres)
        assert '### Line chart' in md
        assert 'Chart title: Investment' in md
        assert '||Series A|' in md
        assert '|2023|150|' in md
        assert '|2024|210.5|' in md
        assert '|2025|300|' in md


def test_sparse_chart_rows_and_date_categories(test_data_dir):
    # Sparse value points (idx 0 and 3 of 4) keep their positions as empty
    # cells, and date-formatted numeric categories render as dates.
    with Presentation(os.path.join(test_data_dir, 'chart_sparse.pptx')) as pres:
        md = export_md(pres)
        rows = [line for line in md.splitlines()
                if line.startswith('|') and not line.startswith('|-') and line != '||S1|']
        assert len(rows) == 4
        assert rows[0].endswith('|4.3|')
        assert rows[1].endswith('||')
        assert rows[2].endswith('||')
        assert rows[3].endswith('|4.5|')
        # Categories are m/d/yyyy serials 37377..37469 -> dates in 2002
        # (the date separator is locale-dependent, so match loosely).
        assert '37377' not in md
        assert rows[0].startswith('|5') and '2002' in rows[0]


def test_scatter_chart_export():
    with Presentation() as pres:
        chart = pres.slides[0].shapes.add_chart(ChartType.SCATTER_WITH_MARKERS, 50, 50, 500, 400, False)
        chart.chart_data.series.clear()
        series = chart.chart_data.series.add('S', ChartType.SCATTER_WITH_MARKERS)
        series.data_points.add_data_point_for_scatter_series(1.0, 2.0)
        series.data_points.add_data_point_for_scatter_series(3.0, 4.0)

        md = export_md(pres)
        assert '### ScatterWithMarkers chart' in md
        assert '|X|S|' in md
        assert '|1|2|' in md
        assert '|3|4|' in md
