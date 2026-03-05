"""Tests for Table: create, cell text, merge, borders, style options."""
from aspose.slides_foss import Presentation, FillType
from aspose.slides_foss.drawing import Color


def _find_table(slide):
    """Find the Table shape on a slide (skip placeholders)."""
    from aspose.slides_foss import Table
    for shape in slide.shapes:
        if isinstance(shape, Table):
            return shape
    return None


def _blank_slide(pres):
    """Return the first slide with placeholders removed."""
    slide = pres.slides[0]
    slide.shapes.clear()
    return slide


def test_create_table():
    """Create a table and verify row/column counts."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        table = slide.shapes.add_table(50, 50, [100, 150, 200], [40, 40, 40])
        assert len(table.rows) == 3
        assert len(table.columns) == 3


def test_cell_text(tmp_pptx):
    """Cell text round-trips through save/reload."""
    pres = Presentation()
    slide = _blank_slide(pres)
    table = slide.shapes.add_table(50, 50, [100, 100], [40, 40])
    table.rows[0][0].text_frame.text = "A"
    table.rows[0][1].text_frame.text = "B"
    table.rows[1][0].text_frame.text = "C"
    table.rows[1][1].text_frame.text = "D"

    pres2 = tmp_pptx(pres)
    t2 = _find_table(pres2.slides[0])
    assert t2 is not None
    assert t2.rows[0][0].text_frame.text == "A"
    assert t2.rows[0][1].text_frame.text == "B"
    assert t2.rows[1][0].text_frame.text == "C"
    assert t2.rows[1][1].text_frame.text == "D"
    pres2.dispose()


def test_merge_cells(tmp_pptx):
    """Merged cells preserve col_span after reload."""
    pres = Presentation()
    slide = _blank_slide(pres)
    table = slide.shapes.add_table(50, 50, [100, 100, 100], [40, 40])
    cell1 = table.rows[0][0]
    cell2 = table.rows[0][1]
    table.merge_cells(cell1, cell2, False)
    assert cell1.is_merged_cell is True
    assert cell1.col_span >= 2

    pres2 = tmp_pptx(pres)
    t2 = _find_table(pres2.slides[0])
    assert t2 is not None
    assert t2.rows[0][0].is_merged_cell is True
    pres2.dispose()


def test_cell_borders(tmp_pptx):
    """Cell borders persist."""
    pres = Presentation()
    slide = _blank_slide(pres)
    table = slide.shapes.add_table(50, 50, [150], [50])
    cell = table.rows[0][0]
    cell.text_frame.text = "Bordered"
    fmt = cell.cell_format
    for border in [fmt.border_top, fmt.border_bottom, fmt.border_left, fmt.border_right]:
        border.fill_format.fill_type = FillType.SOLID
        border.fill_format.solid_fill_color.color = Color.red
        border.width = 3

    pres2 = tmp_pptx(pres)
    t2 = _find_table(pres2.slides[0])
    assert t2 is not None
    fmt2 = t2.rows[0][0].cell_format
    assert fmt2.border_top.width == 3
    pres2.dispose()


def test_table_style_options(tmp_pptx):
    """Table style flags persist."""
    pres = Presentation()
    slide = _blank_slide(pres)
    table = slide.shapes.add_table(50, 50, [120, 120], [40, 40, 40])
    table.first_row = True
    table.horizontal_banding = True
    table.vertical_banding = False

    pres2 = tmp_pptx(pres)
    t2 = _find_table(pres2.slides[0])
    assert t2 is not None
    assert t2.first_row is True
    assert t2.horizontal_banding is True
    pres2.dispose()


def test_row_height():
    """Row heights match constructor arguments."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        table = slide.shapes.add_table(50, 50, [200], [30, 50, 70])
        assert table.rows[0].height == 30
        assert table.rows[1].height == 50
        assert table.rows[2].height == 70


def test_column_width():
    """Column widths match constructor arguments."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        table = slide.shapes.add_table(50, 50, [100, 200, 300], [40])
        assert table.columns[0].width == 100
        assert table.columns[1].width == 200
        assert table.columns[2].width == 300


def test_cell_fill(tmp_pptx):
    """Cell fill colour persists."""
    pres = Presentation()
    slide = _blank_slide(pres)
    table = slide.shapes.add_table(50, 50, [200], [60])
    cell = table.rows[0][0]
    cell.cell_format.fill_format.fill_type = FillType.SOLID
    cell.cell_format.fill_format.solid_fill_color.color = Color.light_blue
    cell.text_frame.text = "Blue"

    pres2 = tmp_pptx(pres)
    t2 = _find_table(pres2.slides[0])
    assert t2 is not None
    cf2 = t2.rows[0][0].cell_format
    assert cf2.fill_format.fill_type == FillType.SOLID
    pres2.dispose()
