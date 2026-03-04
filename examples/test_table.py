"""
Tables — create tables, access rows/columns/cells, formatting, and merging.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import Presentation, ShapeType, FillType
from aspose.slides_foss.drawing import Color
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def create_basic_table():
    """Create a table with column widths and row heights."""
    with Presentation() as pres:
        slide = pres.slides[0]

        col_widths = [100, 150, 200]
        row_heights = [40, 40, 40]
        table = slide.shapes.add_table(50, 50, col_widths, row_heights)

        print(f"Table rows: {len(table.rows)}, columns: {len(table.columns)}")

        # Set text in cells
        for row_idx in range(len(table.rows)):
            for col_idx in range(len(table.columns)):
                cell = table.rows[row_idx][col_idx]
                cell.text_frame.text = f"R{row_idx}C{col_idx}"

        pres.save(os.path.join(OUT, "basic_table.pptx"), SaveFormat.PPTX)
        print("Saved basic_table.pptx")


def access_rows_columns_cells():
    """Access individual rows, columns, and cells."""
    with Presentation() as pres:
        slide = pres.slides[0]
        table = slide.shapes.add_table(50, 50, [120, 120], [40, 40, 40])

        # Access via rows
        row0 = table.rows[0]
        print(f"Row 0 height: {row0.height}")
        print(f"Row 0 cell count: {len(row0)}")

        # Access via columns
        col0 = table.columns[0]
        print(f"Column 0 width: {col0.width}")

        # Access a specific cell
        cell = table.rows[1][0]
        cell.text_frame.text = "Hello"
        print(f"Cell (1,0) text: {cell.text_frame.text}")

        pres.save(os.path.join(OUT, "table_access.pptx"), SaveFormat.PPTX)


def cell_margins():
    """Set cell margins (padding)."""
    with Presentation() as pres:
        slide = pres.slides[0]
        table = slide.shapes.add_table(50, 50, [200], [80])

        cell = table.rows[0][0]
        cell.margin_left = 10
        cell.margin_right = 10
        cell.margin_top = 5
        cell.margin_bottom = 5
        cell.text_frame.text = "Cell with margins"
        print(f"Margins: L={cell.margin_left}, R={cell.margin_right}, T={cell.margin_top}, B={cell.margin_bottom}")

        pres.save(os.path.join(OUT, "table_margins.pptx"), SaveFormat.PPTX)


def cell_text_and_formatting():
    """Set text content in table cells."""
    with Presentation() as pres:
        slide = pres.slides[0]
        table = slide.shapes.add_table(50, 50, [200, 200], [50, 50])

        # Set text via text_frame
        table.rows[0][0].text_frame.text = "Header 1"
        table.rows[0][1].text_frame.text = "Header 2"
        table.rows[1][0].text_frame.text = "Data 1"
        table.rows[1][1].text_frame.text = "Data 2"

        # Verify
        for r in range(len(table.rows)):
            for c in range(len(table.columns)):
                print(f"  [{r},{c}] = '{table.rows[r][c].text_frame.text}'")

        pres.save(os.path.join(OUT, "table_text.pptx"), SaveFormat.PPTX)


def cell_format_borders():
    """Set cell borders via CellFormat."""
    with Presentation() as pres:
        slide = pres.slides[0]
        table = slide.shapes.add_table(50, 50, [150, 150], [50, 50])

        cell = table.rows[0][0]
        cell.text_frame.text = "Bordered"

        # Set borders on the cell
        fmt = cell.cell_format
        for border in [fmt.border_top, fmt.border_bottom, fmt.border_left, fmt.border_right]:
            border.fill_format.fill_type = FillType.SOLID
            border.fill_format.solid_fill_color.color = Color.red
            border.width = 3

        print("Cell borders set to red, width=3")
        pres.save(os.path.join(OUT, "table_borders.pptx"), SaveFormat.PPTX)


def cell_fill():
    """Apply fill to a table cell."""
    with Presentation() as pres:
        slide = pres.slides[0]
        table = slide.shapes.add_table(50, 50, [200], [60, 60])

        # Solid fill on first cell
        cell = table.rows[0][0]
        cell.cell_format.fill_format.fill_type = FillType.SOLID
        cell.cell_format.fill_format.solid_fill_color.color = Color.light_blue
        cell.text_frame.text = "Blue fill"

        # No fill on second cell
        cell2 = table.rows[1][0]
        cell2.text_frame.text = "No fill"

        print("Cell fill applied")
        pres.save(os.path.join(OUT, "table_fill.pptx"), SaveFormat.PPTX)


def row_height():
    """Read and set row heights."""
    with Presentation() as pres:
        slide = pres.slides[0]
        table = slide.shapes.add_table(50, 50, [200], [30, 50, 70])

        for i, row in enumerate(table.rows):
            print(f"  Row {i} height: {row.height}")

        # Change minimal height
        table.rows[0].minimal_height = 60
        print(f"Row 0 minimal_height after change: {table.rows[0].minimal_height}")

        pres.save(os.path.join(OUT, "table_row_height.pptx"), SaveFormat.PPTX)


def table_style_presets():
    """Set table style banding options."""
    with Presentation() as pres:
        slide = pres.slides[0]
        table = slide.shapes.add_table(50, 50, [120, 120, 120], [40, 40, 40, 40])

        # Fill cells with data
        for r in range(len(table.rows)):
            for c in range(len(table.columns)):
                table.rows[r][c].text_frame.text = f"R{r}C{c}"

        # Set style options
        table.first_row = True
        table.horizontal_banding = True
        table.vertical_banding = False

        print(f"first_row={table.first_row}, h_banding={table.horizontal_banding}")
        pres.save(os.path.join(OUT, "table_styles.pptx"), SaveFormat.PPTX)


def merge_cells():
    """Merge table cells."""
    with Presentation() as pres:
        slide = pres.slides[0]
        table = slide.shapes.add_table(50, 50, [100, 100, 100], [40, 40, 40])

        # Merge cells (0,0) to (0,1) — horizontal merge in first row
        cell1 = table.rows[0][0]
        cell2 = table.rows[0][1]
        table.merge_cells(cell1, cell2, False)
        cell1.text_frame.text = "Merged"

        print(f"Cell (0,0) col_span: {cell1.col_span}")
        print(f"Cell (0,0) is_merged: {cell1.is_merged_cell}")

        pres.save(os.path.join(OUT, "table_merge.pptx"), SaveFormat.PPTX)


if __name__ == "__main__":
    create_basic_table()
    access_rows_columns_cells()
    cell_margins()
    cell_text_and_formatting()
    cell_format_borders()
    cell_fill()
    row_height()
    table_style_presets()
    merge_cells()
    print("\n=== test_table.py completed ===")
