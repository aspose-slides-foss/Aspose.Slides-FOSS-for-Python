# Aspose.Slides FOSS — Guide for AI Agents

You are working with `aspose-slides-foss`, the official open-source Python library by Aspose.Slides for creating, reading, and editing PowerPoint (.pptx) presentations.

## Installation

```bash
pip install aspose-slides-foss
```

Requires Python 3.10+. The only runtime dependency is `lxml`.

**This document describes the default branch, not the latest PyPI release.** `26.8.0` on PyPI
predates the changes recorded under `## [Unreleased]` in
[CHANGELOG.md](https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python/blob/main/CHANGELOG.md),
which include hyperlinks and the six distinct PowerPoint save formats. To use what is described here,
install from the repository:

```bash
pip install git+https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python.git
```

## Core Concepts

- **`Presentation`** is the root object. It owns slides, masters, layouts, images, document properties, and comments.
- Always use `Presentation` as a context manager (`with` block) to ensure proper cleanup.
- Save with `prs.save("out.pptx", SaveFormat.PPTX)`. Seven of the twenty-one `SaveFormat` values are
  written: the six PowerPoint formats `PPTX`, `PPTM`, `PPSX`, `PPSM`, `POTX`, `POTM` — each producing
  a package that declares its own main-part content type — and `MD`, which writes Markdown text. The
  other fourteen raise `ValueError`.
- The file name and the `SaveFormat` are independent. `save("deck.pptx", SaveFormat.POTX)` writes a
  genuine template under a `.pptx` name, and PowerPoint refuses a file whose extension disagrees with
  the content type declared inside it. Give the file the extension of the format you asked for.
- Unknown XML parts are preserved verbatim on save — round-tripping is safe.

## Import Pattern

```python
import aspose.slides_foss as slides
from aspose.slides_foss import ShapeType, FillType, NullableBool
from aspose.slides_foss.export import SaveFormat
from aspose.slides_foss.drawing import Color, PointF, SizeF, Size
```

## Quick Reference

### Create a presentation

```python
with slides.Presentation() as prs:
    slide = prs.slides[0]  # first slide exists by default
    prs.save("new.pptx", SaveFormat.PPTX)
```

### Open an existing file

```python
with slides.Presentation("input.pptx") as prs:
    for slide in prs.slides:
        for shape in slide.shapes:
            print(shape.name)
    prs.save("output.pptx", SaveFormat.PPTX)
```

### Add shapes

```python
shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, x, y, width, height)
shape.add_text_frame("Hello")
```

Coordinates and dimensions are in points (1 point = 1/72 inch).

### Text formatting

```python
portion = shape.text_frame.paragraphs[0].portions[0]
fmt = portion.portion_format
fmt.font_height = 24
fmt.font_bold = NullableBool.TRUE
fmt.font_italic = NullableBool.TRUE
fmt.fill_format.fill_type = FillType.SOLID
fmt.fill_format.solid_fill_color.color = Color.from_argb(255, 0, 70, 127)
```

### Tables

```python
col_widths = [120.0, 120.0, 120.0]
row_heights = [40.0, 40.0]
table = slide.shapes.add_table(x, y, col_widths, row_heights)
table.rows[0][0].text_frame.text = "Header"
```

### Connectors

```python
conn = slide.shapes.add_connector(ShapeType.BENT_CONNECTOR3, 0, 0, 10, 10)
conn.start_shape_connected_to = shape_a
conn.start_shape_connection_site_index = 3  # 0=top, 1=left, 2=bottom, 3=right
conn.end_shape_connected_to = shape_b
conn.end_shape_connection_site_index = 1
```

### Fills

```python
shape.fill_format.fill_type = FillType.SOLID
shape.fill_format.solid_fill_color.color = Color.from_argb(255, 30, 120, 200)
```

Also supports: `FillType.GRADIENT`, `FillType.PATTERN`, `FillType.PICTURE`, `FillType.NO_FILL`.

### Images

```python
with open("photo.png", "rb") as f:
    image = prs.images.add_image(f)
slide.shapes.add_picture_frame(ShapeType.RECTANGLE, x, y, w, h, image)
```

### Notes

```python
notes = slide.notes_slide_manager.add_notes_slide()
notes.notes_text_frame.text = "Speaker notes here."
```

### Comments

```python
from datetime import datetime

author = prs.comment_authors.add_author("Jane Smith", "JS")
author.comments.add_comment("Review this", slide, PointF(2.0, 2.0), datetime.now())
```

### Document properties

```python
prs.document_properties.title = "Quarterly Report"
prs.document_properties.author = "Finance Team"
prs.document_properties.set_custom_property_value("Version", 3)
```

### Slide operations

```python
prs.slides.add_empty_slide(prs.layout_slides[0])  # add slide
prs.slides.remove_at(1)                             # remove by index
cloned = prs.slides.add_clone(prs.slides[0])        # clone slide
slide.hidden = True                                  # hide slide
```

### Effects and 3D

```python
from aspose.slides_foss import BevelPresetType

# Outer shadow
ef = shape.effect_format
ef.enable_outer_shadow_effect()
ef.outer_shadow_effect.blur_radius = 10
ef.outer_shadow_effect.distance = 5

# 3D bevel
td = shape.three_d_format
td.bevel_top.bevel_type = BevelPresetType.CIRCLE
td.bevel_top.height = 6
td.bevel_top.width = 6
```

### Line formatting

```python
from aspose.slides_foss import LineDashStyle

lf = shape.line_format
lf.width = 2.5
lf.dash_style = LineDashStyle.DASH_DOT
lf.fill_format.fill_type = FillType.SOLID
lf.fill_format.solid_fill_color.color = Color.red
```

### Hyperlinks

External links, on click or on mouse over, on a text portion or on a whole shape.

```python
from aspose.slides_foss import Hyperlink

portion = shape.text_frame.paragraphs[0].portions[0]
portion.portion_format.hyperlink_click = "https://example.com/report"
shape.hyperlink_mouse_over = Hyperlink("https://example.com", tooltip="Home")
```

Assigning `None` removes the link and the relationship it owns. A string is accepted as shorthand for
a `Hyperlink` with no tooltip.

### Group shapes

```python
group = slide.shapes.add_group_shape()
group.shapes.add_auto_shape(ShapeType.RECTANGLE, 300, 100, 100, 100)
group.name = "TwoRectangles"
```

`group.line_format` and `group.three_d_format` are `None`: `CT_GroupShapeProperties` has no outline
and no 3-D element. Shapes *inside* the group keep both.

### Slide transitions

```python
from aspose.slides_foss.slideshow import TransitionType

slide.slide_show_transition.type = TransitionType.CIRCLE
slide.slide_show_transition.advance_on_click = True
slide.slide_show_transition.advance_after_time = 3000  # ms
```

### Charts

A chart is backed by a real embedded XLSX workbook; build it by writing cells and binding series and
categories to them.

```python
from aspose.slides_foss.charts import ChartType

chart = slide.shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50, 50, 600, 400, False)
cd = chart.chart_data
wb = cd.chart_data_workbook
cd.series.clear()
cd.categories.clear()
cd.categories.add(wb.get_cell(0, 1, 0, "Q1"))
series = cd.series.add(wb.get_cell(0, 0, 1, "Revenue"), chart.type)
series.data_points.add_data_point_for_bar_series(wb.get_cell(0, 1, 1, 1200))
```

`wb.get_cell(worksheet_index, row, column, value)` writes the value and returns the cell reference the
series and categories bind to.

### Markdown export

```python
from aspose.slides_foss.export import MarkdownSaveOptions, Flavor, NewLineType

options = MarkdownSaveOptions()
options.flavor = Flavor.GITHUB
options.new_line_type = NewLineType.UNIX
options.show_slide_number = True
prs.save("out.md", SaveFormat.MD, options)
prs.save("subset.md", [2, 1], SaveFormat.MD, options)   # 1-based; order and repeats respected
```

The export is text-only: text frames, tables, lists, titles as headings, comments and chart data.
Images, media and SmartArt are skipped.

## Package Structure

```
aspose/
  slides_foss/           # Main package
    __init__.py          # Public API re-exports
    Presentation.py      # Root object
    Slide.py             # Slide, LayoutSlide, MasterSlide
    ShapeCollection.py   # Shape management
    AutoShape.py         # AutoShape with text frames
    Table.py             # Tables, rows, columns, cells
    Connector.py         # Shape-to-shape connectors
    TextFrame.py         # Text content model
    FillFormat.py        # Fill styling
    LineFormat.py        # Line styling
    EffectFormat.py      # Visual effects
    ThreeDFormat.py      # 3D formatting
    Comment.py           # Slide comments
    DocumentProperties.py
    _internal/           # Implementation internals (do not import directly)
    animation/           # Sequences, effects, triggers, motion paths
    charts/              # ChartType, chart data, the embedded workbook
    drawing/             # Color, PointF, SizeF, Size
    effects/             # Effect-related enums
    export/              # SaveFormat, MarkdownSaveOptions, Flavor, NewLineType
    slideshow/           # TransitionType and slide-show transition types
    theme/               # Theme-related types
```

## Do

- Always wrap `Presentation` in a `with` block
- Give a saved file the extension of the `SaveFormat` you passed
- Use `Color.from_argb(a, r, g, b)` or named constants like `Color.red`, `Color.blue`
- Access slides via `prs.slides[index]` — slides are 0-indexed
- Use `NullableBool` enum (`NullableBool.FALSE`, `NullableBool.TRUE`, `NullableBool.NOT_DEFINED`) for boolean formatting properties like `font_bold`
- Import drawing types from `aspose.slides_foss.drawing`

## Don't

- Don't import from `aspose.slides_foss._internal` — it is a private implementation detail
- Don't attempt PDF, HTML, SVG, or image export. There is no renderer: this library writes OOXML, it
  does not lay out or rasterize
- Don't use SmartArt, OLE objects, or VBA macros — they are not implemented
- Don't modify the public API class signatures — they are fixed

## How an unsupported thing fails

Do not catch `NotImplementedError` for an absent capability. Exactly one method in the package raises
it — `aspose.slides_foss.animation.TextAnimation.add_effect` — and nothing else does. Everything else
fails in one of two ways, and an agent should expect the right one:

- **A `SaveFormat` this library does not write** raises `ValueError` from `save`, with a message
  naming the seven that do work: `Export format 'Pdf' is not supported; this library writes Md,
  Potm, Potx, Ppsm, Ppsx, Pptm, Pptx`.
- **A member that does not exist** is simply absent, so reading it raises `AttributeError` — and so
  does *assigning* to it. An assignment to a property a shape or a formatting object does not have is
  not accepted and discarded; it fails where it is written, which is what makes a misspelt property
  name visible. Names beginning with an underscore are unaffected.

## Limitations

Absent rather than present and inert — the API member does not exist:

- Rendering and conversion of any kind: no PDF, HTML, XPS or image export
- The binary `.ppt` family, OpenDocument, and `XML` as save formats
- SmartArt, OLE objects, mathematical text
- VBA macros, digital signatures, encryption
- Action settings other than external hyperlinks
- Presentation sections — `Presentation.sections` does not exist
- Slide size — no public API reads or changes it, so a new deck is whatever the bundled template says
  (16:9, 12192000 × 6858000 EMU)

Comment threads are rebuilt from the classic comment list on save. A deck authored in PowerPoint can
carry resolved status, @-mentions and reply chains the classic list cannot express; those are lost if
the presentation's comment authors are touched before saving. Loading and saving without going near
comments leaves the file's own threads alone.

## Links

- [GitHub](https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python)
- [Issue Tracker](https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python/issues)
- [PyPI](https://pypi.org/project/aspose-slides-foss/)
- [Aspose.Slides](https://products.aspose.org/slides/)

