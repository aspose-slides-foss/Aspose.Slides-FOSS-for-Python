# Aspose.Slides FOSS

The official open-source Python library by Aspose.Slides for creating, reading, and editing PowerPoint (`.pptx`) presentations.

---

## Installation

```bash
pip install aspose-slides-foss
```

**Requires:** Python 3.10 or later, and `lxml` (installed automatically as a
dependency). Continuous integration runs the full test suite on Python 3.10,
3.11, 3.12, 3.13 and 3.14, on Linux, Windows and macOS — fifteen jobs, and a
release is gated on all of them passing. Pure Python — there is nothing to
compile.

> **The latest release on PyPI predates this page.** `pip install` gets
> `26.8.0`, and the changes listed in
> [CHANGELOG.md](https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python/blob/main/CHANGELOG.md)
> under `## [Unreleased]` are not in it — including hyperlinks, which the
> example below needs, and the six distinct PowerPoint save formats. For the
> behaviour described here, install from the repository:
>
> ```bash
> pip install git+https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python.git
> ```

> The `aspose` name is a shared namespace package. If the **commercial**
> `aspose` package is installed in the same environment it takes the name over
> and this library becomes unimportable, with a bare
> `ModuleNotFoundError: No module named 'aspose.slides_foss'`. Install this one
> into its own virtual environment.

---

## Quick Start

```python
import aspose.slides_foss as slides
from aspose.slides_foss.export import SaveFormat

# Create a new presentation — needs no input file, so this runs as it stands
with slides.Presentation() as prs:
    slide = prs.slides[0]
    prs.save("new.pptx", SaveFormat.PPTX)

# Open an existing presentation
with slides.Presentation("new.pptx") as prs:
    print(f"Slides: {len(prs.slides)}")
    prs.save("output.pptx", SaveFormat.PPTX)
```

---

## Features

- **Presentation I/O** — Open, create, and save `.pptx` files. A deck PowerPoint authored re-saves with every part preserved; parts this library does not yet understand are carried through verbatim rather than dropped
- **Slides** — Add, remove, clone, hide, and iterate slides
- **Shapes** — AutoShapes, PictureFrames, Tables, Connectors, GroupShapes, and reordering within a slide
- **Text** — TextFrame, Paragraph, Portion with character, paragraph, and text frame formatting (including bullets)
- **Charts** — 73 chart types, series, categories, axes, trendlines, error bars, legend, titles, data labels, markers, series groups, 3D, each backed by a real embedded XLSX workbook
- **Animations** — Shape and text-level animations with sequences, effects, triggers, and motion paths
- **Slide transitions** — 57 transition types with per-slide timing, advance settings, and morph support
- **Themes** — Color schemes, font schemes, format schemes, master/override themes
- **Backgrounds** — Per-slide and master slide backgrounds with solid/gradient/pattern/picture fills
- **Fill** — Solid, gradient, pattern, and picture fills
- **Lines** — Width, dash style, arrows, join and alignment
- **Effects** — Outer shadow, inner shadow, glow, soft edge, reflection, blur, preset shadow, fill overlay
- **3D** — Bevel, camera, light rig, material, extrusion depth
- **Document properties** — Core, app, and custom properties
- **Notes slides** — Per-slide notes with header/footer management
- **Comments** — Classic and modern threaded comments with authors, timestamps, replies, and positions
- **Images** — Embed from bytes or any file-like object
- **Hyperlinks** — External links on a text portion or on a whole shape, on click or on mouse over
- **Markdown export** — Save presentation text as Markdown in 24 flavor dialects, with tables, lists, headings, comments, and chart data

---

## Usage Examples

### Shapes

```python
from aspose.slides_foss import ShapeType
import aspose.slides_foss as slides
from aspose.slides_foss.export import SaveFormat

with slides.Presentation() as prs:
    slide = prs.slides[0]
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 100)
    shape.add_text_frame("Hello, world!")
    prs.save("shapes.pptx", SaveFormat.PPTX)
```

### Text Formatting

```python
from aspose.slides_foss import ShapeType, NullableBool, FillType
from aspose.slides_foss.drawing import Color
import aspose.slides_foss as slides
from aspose.slides_foss.export import SaveFormat

with slides.Presentation() as prs:
    shape = prs.slides[0].shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 150)
    tf = shape.add_text_frame("Formatted text")
    fmt = tf.paragraphs[0].portions[0].portion_format
    fmt.font_height = 24
    fmt.font_bold = NullableBool.TRUE
    fmt.fill_format.fill_type = FillType.SOLID
    fmt.fill_format.solid_fill_color.color = Color.from_argb(255, 0, 70, 127)
    prs.save("text.pptx", SaveFormat.PPTX)
```

### Hyperlinks

```python
import aspose.slides_foss as slides
from aspose.slides_foss import Hyperlink, ShapeType
from aspose.slides_foss.export import SaveFormat

with slides.Presentation() as prs:
    shape = prs.slides[0].shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 100)
    tf = shape.add_text_frame("Read the report")
    # On a single text portion ...
    tf.paragraphs[0].portions[0].portion_format.hyperlink_click = "https://example.com/report"
    # ... or on the whole shape, with a tooltip.
    shape.hyperlink_mouse_over = Hyperlink("https://example.com", tooltip="Home")
    prs.save("links.pptx", SaveFormat.PPTX)
```

Assigning `None` removes the link and the relationship it owns.

### Table

```python
import aspose.slides_foss as slides
from aspose.slides_foss.export import SaveFormat

with slides.Presentation() as prs:
    table = prs.slides[0].shapes.add_table(50, 50, [120.0, 120.0, 120.0], [40.0, 40.0])
    table.rows[0][0].text_frame.text = "Name"
    table.rows[0][1].text_frame.text = "Value"
    prs.save("table.pptx", SaveFormat.PPTX)
```

### Connector

```python
from aspose.slides_foss import ShapeType
import aspose.slides_foss as slides
from aspose.slides_foss.export import SaveFormat

with slides.Presentation() as prs:
    slide = prs.slides[0]
    box1 = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 100, 150, 60)
    box2 = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 350, 100, 150, 60)
    conn = slide.shapes.add_connector(ShapeType.BENT_CONNECTOR3, 0, 0, 10, 10)
    conn.start_shape_connected_to = box1
    conn.start_shape_connection_site_index = 3  # right
    conn.end_shape_connected_to = box2
    conn.end_shape_connection_site_index = 1    # left
    prs.save("connector.pptx", SaveFormat.PPTX)
```

### Fill

```python
from aspose.slides_foss import ShapeType, FillType
from aspose.slides_foss.drawing import Color
import aspose.slides_foss as slides
from aspose.slides_foss.export import SaveFormat

with slides.Presentation() as prs:
    shape = prs.slides[0].shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 150)
    shape.fill_format.fill_type = FillType.SOLID
    shape.fill_format.solid_fill_color.color = Color.from_argb(255, 30, 120, 200)
    prs.save("fill.pptx", SaveFormat.PPTX)
```

### Image

`add_image` takes the image **bytes**, or any object with a `.read()` method. It does not take a
file path — open the file yourself, which keeps the library out of the business of guessing
encodings and leaving handles open:

```python
import aspose.slides_foss as slides
from aspose.slides_foss import ShapeType
from aspose.slides_foss.export import SaveFormat

with slides.Presentation() as prs:
    with open("picture.png", "rb") as fh:
        image = prs.images.add_image(fh)      # or add_image(fh.read())
    prs.slides[0].shapes.add_picture_frame(ShapeType.RECTANGLE, 50, 50, 300, 200, image)
    prs.save("picture.pptx", SaveFormat.PPTX)
```

### Notes

```python
import aspose.slides_foss as slides
from aspose.slides_foss.export import SaveFormat

with slides.Presentation() as prs:
    notes = prs.slides[0].notes_slide_manager.add_notes_slide()
    notes.notes_text_frame.text = "Speaker notes go here."
    prs.save("notes.pptx", SaveFormat.PPTX)
```

### Comments

```python
from aspose.slides_foss.drawing import PointF
from datetime import datetime
import aspose.slides_foss as slides
from aspose.slides_foss.export import SaveFormat

with slides.Presentation() as prs:
    author = prs.comment_authors.add_author("Jane Smith", "JS")
    slide = prs.slides[0]
    author.comments.add_comment("Review this slide", slide, PointF(2.0, 2.0), datetime.now())
    prs.save("comments.pptx", SaveFormat.PPTX)
```

### Document Properties

```python
import aspose.slides_foss as slides
from aspose.slides_foss.export import SaveFormat

with slides.Presentation() as prs:
    prs.document_properties.title = "Q1 Results"
    prs.document_properties.author = "Finance Team"
    prs.document_properties.set_custom_property_value("Version", 3)
    prs.save("deck.pptx", SaveFormat.PPTX)
```

### Chart

Build a chart from scratch by populating its backing workbook:

```python
from aspose.slides_foss.charts import ChartType
import aspose.slides_foss as slides
from aspose.slides_foss.export import SaveFormat

with slides.Presentation() as prs:
    slide = prs.slides[0]

    # Pass has_default_data=False to start with an empty workbook
    chart = slide.shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 600, 400, False)
    chart.chart_title.add_text_frame_for_overriding("Quarterly Sales")

    cd = chart.chart_data
    wb = cd.chart_data_workbook  # embedded XLSX workbook backing the chart

    cd.series.clear()
    cd.categories.clear()

    # Workbook layout (worksheet 0):
    #          col 0   col 1      col 2
    #  row 0            "Revenue"  "Expenses"   <- series name row
    #  row 1   "Q1"     1200       800
    #  row 2   "Q2"     1500       900
    #  row 3   "Q3"     1800       1000
    #  row 4   "Q4"     2100       1100

    # Categories — column 0, rows 1..4
    for row, name in enumerate(["Q1", "Q2", "Q3", "Q4"], start=1):
        cd.categories.add(wb.get_cell(0, row, 0, name))

    # Series 1 (Revenue) — name at (row 0, col 1), values at (rows 1..4, col 1)
    s1 = cd.series.add(wb.get_cell(0, 0, 1, "Revenue"), chart.type)
    for row, value in enumerate([1200, 1500, 1800, 2100], start=1):
        s1.data_points.add_data_point_for_bar_series(wb.get_cell(0, row, 1, value))

    # Series 2 (Expenses) — name at (row 0, col 2), values at (rows 1..4, col 2)
    s2 = cd.series.add(wb.get_cell(0, 0, 2, "Expenses"), chart.type)
    for row, value in enumerate([800, 900, 1000, 1100], start=1):
        s2.data_points.add_data_point_for_bar_series(wb.get_cell(0, row, 2, value))

    prs.save("chart.pptx", SaveFormat.PPTX)
```

`wb.get_cell(worksheet_index, row, column, value)` writes the value to the embedded
XLSX and returns a cell reference that the chart series and categories bind to.

### Slide Transition

```python
from aspose.slides_foss.slideshow import TransitionType
import aspose.slides_foss as slides
from aspose.slides_foss.export import SaveFormat

with slides.Presentation() as prs:
    slide = prs.slides[0]
    slide.slide_show_transition.type = TransitionType.CIRCLE
    slide.slide_show_transition.advance_on_click = True
    slide.slide_show_transition.advance_after_time = 3000  # ms
    prs.save("transition.pptx", SaveFormat.PPTX)
```

### Group Shape

```python
from aspose.slides_foss import ShapeType
import aspose.slides_foss as slides
from aspose.slides_foss.export import SaveFormat

with slides.Presentation() as prs:
    slide = prs.slides[0]
    group = slide.shapes.add_group_shape()
    group.shapes.add_auto_shape(ShapeType.RECTANGLE, 300, 100, 100, 100)
    group.shapes.add_auto_shape(ShapeType.RECTANGLE, 500, 100, 100, 100)
    group.name = "TwoRectangles"
    prs.save("group.pptx", SaveFormat.PPTX)
```

### Markdown Export

```python
import aspose.slides_foss as slides
from aspose.slides_foss.export import SaveFormat, MarkdownSaveOptions, Flavor, NewLineType

with slides.Presentation("input.pptx") as prs:
    # Save the whole presentation with default options
    prs.save("output.md", SaveFormat.MD)

    # Or customize the output
    options = MarkdownSaveOptions()
    options.flavor = Flavor.GITHUB
    options.new_line_type = NewLineType.UNIX
    options.show_slide_number = True
    options.slide_number_format = "## Slide {0}"
    options.show_hidden_slides = True
    options.show_comments = True
    prs.save("custom.md", SaveFormat.MD, options)

    # Save only selected slides (1-based, order and repeats respected)
    prs.save("subset.md", [2, 1], SaveFormat.MD, options)
```

Text frames, tables, lists, titles/subtitles (as headings), comments, and chart
data are exported; the export is text-only, so images, media, and SmartArt are skipped.

---

## Limitations

`SaveFormat` declares 21 values. **Seven are written.** The six PowerPoint
formats — `PPTX`, `PPTM`, `PPSX`, `PPSM`, `POTX` and `POTM` — each produce a
distinct package declaring its own main-part content type, rather than one
presentation package under six names; `MD` writes Markdown text.

The other **fourteen raise `ValueError`**, naming the seven that work, rather
than writing a mislabelled file: `PPT`, `PPS`, `POT` (the binary PowerPoint
family), `PDF`, `XPS`, `HTML`, `HTML5`, `SWF`, `TIFF`, `GIF` (rendering and
conversion), `ODP`, `OTP`, `FODP` (OpenDocument) and `XML`.

The following are not implemented, and the API member is absent rather than
present and inert:

- **Rendering and conversion of any kind** — no PDF, HTML, XPS or image export.
  This is a design boundary, not a gap: the library writes OOXML, it does not
  lay out or rasterize.
- **Presentation sections** — `Presentation.sections` does not exist.
- **Slide size** — there is no public API to read or change it, so a new deck
  is whatever the bundled template says (16:9, 12192000 × 6858000 EMU).
- SmartArt, OLE objects, mathematical text
- VBA macros, digital signatures, encryption
- Action settings other than external hyperlinks

`add_image` accepts image bytes or a file-like object, not a file path. Open
the file and pass the handle or its bytes.

`SaveFormat` and the file name are independent: `save("deck.pptx",
SaveFormat.POTX)` writes a genuine template under a `.pptx` name, and
PowerPoint refuses to open a file whose extension disagrees with the format
declared inside it. Give the file the extension of the format you asked for.

Assigning to a property a shape or a formatting object does not have raises
`AttributeError` rather than being accepted and discarded, so a misspelt
property name fails where it is written. Names beginning with an underscore
are unaffected.

Comment threads are written from the classic comment list on save. A deck
authored in PowerPoint can carry resolved status, @-mentions and reply chains
that the classic list cannot express; those are lost if the presentation's
comment authors are touched before saving. Loading and saving without going
near comments preserves the file's own threads untouched.

Unknown XML parts encountered during load are preserved verbatim on save —
opening and re-saving a file will never strip content this library does not yet understand.

---

## Links

- [GitHub Repository](https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python)
- [Issue Tracker](https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python/issues)
- [Changelog](https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python/blob/main/CHANGELOG.md) — what changed, and what changed in a way you will notice
- [Contributing](https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python/blob/main/CONTRIBUTING.md) — how to build, how to run the tests, and how to report a fix
- [Security policy](https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python/blob/main/SECURITY.md) — how to report a vulnerability privately
- [Code of conduct](https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python/blob/main/CODE_OF_CONDUCT.md)

---

## License

[MIT License](https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python/blob/main/LICENSE)
