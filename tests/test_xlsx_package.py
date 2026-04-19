"""Tests for the internal XLSX package infrastructure."""

import io
import os
import sys
import unittest

# Ensure src is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aspose.slides_foss._internal.xlsx import (
    XlsxPackage,
    CellValue,
    col_letter_to_index,
    col_index_to_letter,
    parse_cell_ref,
    format_cell_ref,
    parse_range_ref,
    iterate_range,
)


# ---- Cell Reference Tests ----

class TestCellReference(unittest.TestCase):

    def test_col_letter_to_index(self):
        self.assertEqual(col_letter_to_index('A'), 0)
        self.assertEqual(col_letter_to_index('B'), 1)
        self.assertEqual(col_letter_to_index('Z'), 25)
        self.assertEqual(col_letter_to_index('AA'), 26)
        self.assertEqual(col_letter_to_index('AZ'), 51)
        self.assertEqual(col_letter_to_index('BA'), 52)

    def test_col_index_to_letter(self):
        self.assertEqual(col_index_to_letter(0), 'A')
        self.assertEqual(col_index_to_letter(1), 'B')
        self.assertEqual(col_index_to_letter(25), 'Z')
        self.assertEqual(col_index_to_letter(26), 'AA')
        self.assertEqual(col_index_to_letter(51), 'AZ')
        self.assertEqual(col_index_to_letter(52), 'BA')

    def test_col_roundtrip(self):
        for i in range(200):
            self.assertEqual(col_letter_to_index(col_index_to_letter(i)), i)

    def test_parse_cell_ref(self):
        self.assertEqual(parse_cell_ref('A1'), (0, 0))
        self.assertEqual(parse_cell_ref('B3'), (2, 1))
        self.assertEqual(parse_cell_ref('D5'), (4, 3))
        self.assertEqual(parse_cell_ref('AA100'), (99, 26))

    def test_parse_cell_ref_absolute(self):
        self.assertEqual(parse_cell_ref('$A$1'), (0, 0))
        self.assertEqual(parse_cell_ref('$C$5'), (4, 2))

    def test_format_cell_ref(self):
        self.assertEqual(format_cell_ref(0, 0), 'A1')
        self.assertEqual(format_cell_ref(2, 1), 'B3')
        self.assertEqual(format_cell_ref(4, 3), 'D5')

    def test_parse_range_ref(self):
        self.assertEqual(parse_range_ref('A1:D5'), ((0, 0), (4, 3)))
        self.assertEqual(parse_range_ref('$A$1:$D$5'), ((0, 0), (4, 3)))

    def test_parse_range_ref_with_sheet(self):
        self.assertEqual(parse_range_ref('Sheet1!$A$1:$D$5'), ((0, 0), (4, 3)))

    def test_iterate_range(self):
        cells = list(iterate_range('A1:B2'))
        self.assertEqual(cells, [
            (0, 0, 'A1'), (0, 1, 'B1'),
            (1, 0, 'A2'), (1, 1, 'B2'),
        ])


# ---- XLSX Package Tests ----

class TestXlsxPackageCreateNew(unittest.TestCase):

    def test_create_new(self):
        xlsx = XlsxPackage.create_new()
        names = xlsx.get_sheet_names()
        self.assertEqual(names, ['Sheet1'])

    def test_get_worksheet(self):
        xlsx = XlsxPackage.create_new()
        ws = xlsx.get_worksheet('Sheet1')
        self.assertIsNotNone(ws)
        ws2 = xlsx.get_worksheet(0)
        self.assertIsNotNone(ws2)

    def test_get_nonexistent_worksheet(self):
        xlsx = XlsxPackage.create_new()
        self.assertIsNone(xlsx.get_worksheet('NoSuchSheet'))
        self.assertIsNone(xlsx.get_worksheet(99))


class TestXlsxPackageReadWrite(unittest.TestCase):

    def test_write_and_read_numeric(self):
        xlsx = XlsxPackage.create_new()
        ws = xlsx.get_worksheet('Sheet1')
        ws.set_cell('A1', 42)
        ws.set_cell('B2', 3.14)

        cell_a1 = ws.get_cell('A1')
        self.assertEqual(cell_a1.value, 42)
        self.assertFalse(cell_a1.is_string)

        cell_b2 = ws.get_cell('B2')
        self.assertAlmostEqual(cell_b2.value, 3.14)
        self.assertFalse(cell_b2.is_string)

    def test_write_and_read_string(self):
        xlsx = XlsxPackage.create_new()
        ws = xlsx.get_worksheet('Sheet1')
        ws.set_cell('A1', 'Hello')
        ws.set_cell('B1', 'World')

        cell_a1 = ws.get_cell('A1')
        self.assertEqual(cell_a1.value, 'Hello')
        self.assertTrue(cell_a1.is_string)

        cell_b1 = ws.get_cell('B1')
        self.assertEqual(cell_b1.value, 'World')
        self.assertTrue(cell_b1.is_string)

    def test_empty_cell(self):
        xlsx = XlsxPackage.create_new()
        ws = xlsx.get_worksheet('Sheet1')
        cell = ws.get_cell('Z99')
        self.assertIsNone(cell.value)
        self.assertTrue(cell.is_empty)

    def test_delete_cell(self):
        xlsx = XlsxPackage.create_new()
        ws = xlsx.get_worksheet('Sheet1')
        ws.set_cell('A1', 100)
        self.assertEqual(ws.get_cell('A1').value, 100)
        ws.delete_cell('A1')
        self.assertIsNone(ws.get_cell('A1').value)

    def test_set_cell_none_deletes(self):
        xlsx = XlsxPackage.create_new()
        ws = xlsx.get_worksheet('Sheet1')
        ws.set_cell('A1', 100)
        ws.set_cell('A1', None)
        self.assertIsNone(ws.get_cell('A1').value)

    def test_overwrite_cell(self):
        xlsx = XlsxPackage.create_new()
        ws = xlsx.get_worksheet('Sheet1')
        ws.set_cell('A1', 'first')
        ws.set_cell('A1', 'second')
        self.assertEqual(ws.get_cell('A1').value, 'second')

    def test_range_read_write(self):
        xlsx = XlsxPackage.create_new()
        ws = xlsx.get_worksheet('Sheet1')
        data = [
            ['Name', 'Value'],
            ['Alpha', 10],
            ['Beta', 20],
        ]
        ws.set_range('A1:B3', data)

        result = ws.get_range('A1:B3')
        self.assertEqual(result[0][0].value, 'Name')
        self.assertEqual(result[0][1].value, 'Value')
        self.assertEqual(result[1][0].value, 'Alpha')
        self.assertEqual(result[1][1].value, 10)
        self.assertEqual(result[2][0].value, 'Beta')
        self.assertEqual(result[2][1].value, 20)


class TestXlsxPackageRoundTrip(unittest.TestCase):

    def test_save_and_reopen(self):
        # Create, write, save to bytes, reopen, verify
        xlsx = XlsxPackage.create_new()
        ws = xlsx.get_worksheet('Sheet1')
        ws.set_cell('A1', 'Category')
        ws.set_cell('B1', 'Series 1')
        ws.set_cell('A2', 'Q1')
        ws.set_cell('B2', 100.5)
        ws.set_cell('A3', 'Q2')
        ws.set_cell('B3', 200)

        data = xlsx.to_bytes()
        self.assertIsInstance(data, bytes)
        self.assertGreater(len(data), 0)

        # Reopen
        xlsx2 = XlsxPackage.from_bytes(data)
        self.assertEqual(xlsx2.get_sheet_names(), ['Sheet1'])

        ws2 = xlsx2.get_worksheet('Sheet1')
        self.assertEqual(ws2.get_cell('A1').value, 'Category')
        self.assertEqual(ws2.get_cell('B1').value, 'Series 1')
        self.assertEqual(ws2.get_cell('A2').value, 'Q1')
        self.assertAlmostEqual(ws2.get_cell('B2').value, 100.5)
        self.assertEqual(ws2.get_cell('A3').value, 'Q2')
        self.assertEqual(ws2.get_cell('B3').value, 200)

    def test_add_worksheet(self):
        xlsx = XlsxPackage.create_new()
        ws2 = xlsx.add_worksheet('Data')
        ws2.set_cell('A1', 'test')

        data = xlsx.to_bytes()
        xlsx2 = XlsxPackage.from_bytes(data)
        self.assertEqual(xlsx2.get_sheet_names(), ['Sheet1', 'Data'])
        ws = xlsx2.get_worksheet('Data')
        self.assertEqual(ws.get_cell('A1').value, 'test')


class TestXlsxPackageTable(unittest.TestCase):

    def test_create_table(self):
        xlsx = XlsxPackage.create_new()
        ws = xlsx.get_worksheet('Sheet1')

        # Write data
        ws.set_range('A1:C3', [
            [' ', 'Series 1', 'Series 2'],
            ['Cat 1', 10, 20],
            ['Cat 2', 30, 40],
        ])

        # Create table
        table = xlsx.create_table(ws, 'Table1', 'A1:C3', [' ', 'Series 1', 'Series 2'])
        self.assertEqual(table.get_ref(), 'A1:C3')
        self.assertEqual(table.get_display_name(), 'Table1')
        cols = table.get_columns()
        self.assertEqual(len(cols), 3)
        self.assertEqual(cols[1].name, 'Series 1')

        # Round-trip
        data = xlsx.to_bytes()
        xlsx2 = XlsxPackage.from_bytes(data)
        ws2 = xlsx2.get_worksheet('Sheet1')
        self.assertEqual(ws2.get_cell('B2').value, 10)


# ---- Test with real Charts.pptx embedded XLSX ----

CHARTS_PPTX = r'C:\Dev\GitHub\Aspose.Slides-FOSS-for-Python\manual_tests\Charts.pptx'


@unittest.skipUnless(os.path.exists(CHARTS_PPTX), 'Charts.pptx not available')
class TestXlsxFromChartsPptx(unittest.TestCase):

    def _extract_xlsx_bytes(self, part_name: str) -> bytes:
        from aspose.slides_foss._internal.opc.opc_package import OpcPackage
        pptx = OpcPackage.open(CHARTS_PPTX)
        data = pptx.get_part(part_name)
        self.assertIsNotNone(data, f"Part {part_name} not found in Charts.pptx")
        return data

    def test_read_chart1_data(self):
        """Read the first embedded XLSX (multi-series chart)."""
        xlsx_bytes = self._extract_xlsx_bytes('ppt/embeddings/Microsoft_Excel_Worksheet1.xlsx')
        xlsx = XlsxPackage.from_bytes(xlsx_bytes)

        self.assertEqual(xlsx.get_sheet_names(), ['Sheet1'])
        ws = xlsx.get_worksheet('Sheet1')

        # Row 1 headers: " ", "Series 1", "Series 2", "Series 3"
        self.assertEqual(ws.get_cell('B1').value, 'Series 1')
        self.assertEqual(ws.get_cell('C1').value, 'Series 2')
        self.assertEqual(ws.get_cell('D1').value, 'Series 3')

        # Row 2: "Category 1", 4.3, 2.4, 2
        self.assertEqual(ws.get_cell('A2').value, 'Category 1')
        self.assertAlmostEqual(ws.get_cell('B2').value, 4.3)
        self.assertAlmostEqual(ws.get_cell('C2').value, 2.4)
        self.assertEqual(ws.get_cell('D2').value, 2)

    def test_read_chart2_data(self):
        """Read the second embedded XLSX (single-series pie chart)."""
        xlsx_bytes = self._extract_xlsx_bytes('ppt/embeddings/Microsoft_Excel_Worksheet2.xlsx')
        xlsx = XlsxPackage.from_bytes(xlsx_bytes)

        ws = xlsx.get_worksheet('Sheet1')

        # Headers
        self.assertEqual(ws.get_cell('B1').value, 'Sales')

        # Data
        self.assertEqual(ws.get_cell('A2').value, '1st Qtr')
        self.assertEqual(ws.get_cell('A3').value, '2nd Qtr')

    def test_modify_and_roundtrip(self):
        """Modify chart data and verify round-trip."""
        xlsx_bytes = self._extract_xlsx_bytes('ppt/embeddings/Microsoft_Excel_Worksheet1.xlsx')
        xlsx = XlsxPackage.from_bytes(xlsx_bytes)
        ws = xlsx.get_worksheet('Sheet1')

        # Modify a value
        ws.set_cell('B2', 99.9)

        # Round-trip
        new_bytes = xlsx.to_bytes()
        xlsx2 = XlsxPackage.from_bytes(new_bytes)
        ws2 = xlsx2.get_worksheet('Sheet1')
        self.assertAlmostEqual(ws2.get_cell('B2').value, 99.9)

        # Other values preserved
        self.assertEqual(ws2.get_cell('A2').value, 'Category 1')
        self.assertAlmostEqual(ws2.get_cell('C2').value, 2.4)


if __name__ == '__main__':
    unittest.main()
