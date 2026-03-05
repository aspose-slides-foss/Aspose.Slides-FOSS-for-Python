# Aspose.Slides FOSS — Guide for AI Agents

You are working with `aspose-slides-foss`, the official open-source Python library by Aspose.Slides for creating, reading, and editing PowerPoint (.pptx) presentations. The API is compatible with [Aspose.Slides for Python via .NET](https://pypi.org/project/Aspose.Slides/).

## Installation

```bash
pip install aspose-slides-foss
```

Requires Python 3.10+. The only runtime dependency is `lxml`.

## Core Concepts

- **`Presentation`** is the root object. It owns slides, masters, layouts, images, document properties, and comments.
- Always use `Presentation` as a context manager (`with` block) to ensure proper cleanup.
- Save with `prs.save("out.pptx", SaveFormat.PPTX)`. Only PPTX output is supported.
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
lf = shape.line_format
lf.width = 2.5
lf.dash_style = LineDashStyle.DASH_DOT
lf.fill_format.fill_type = FillType.SOLID
lf.fill_format.solid_fill_color.color = Color.red
```

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
    drawing/             # Color, PointF, SizeF, Size
    export/              # SaveFormat
    effects/             # Effect-related enums
    theme/               # Theme-related types
```

## Do

- Always wrap `Presentation` in a `with` block
- Use `SaveFormat.PPTX` when saving — it is the only supported format
- Use `Color.from_argb(a, r, g, b)` or named constants like `Color.red`, `Color.blue`
- Access slides via `prs.slides[index]` — slides are 0-indexed
- Use `NullableBool` enum (`NullableBool.FALSE`, `NullableBool.TRUE`, `NullableBool.NOT_DEFINED`) for boolean formatting properties like `font_bold`
- Import drawing types from `aspose.slides_foss.drawing`

## Don't

- Don't import from `aspose.slides_foss._internal` — it is a private implementation detail
- Don't attempt PDF, HTML, SVG, or image export — only PPTX is supported
- Don't use charts, SmartArt, animations, or VBA — they are not yet implemented and will raise `NotImplementedError`
- Don't modify the public API class signatures — they are fixed

## Limitations

Not yet implemented (will raise `NotImplementedError`):

- Charts, SmartArt, OLE objects, mathematical text
- Animations and slide transitions
- Export to PDF, HTML, SVG, or images
- VBA macros, digital signatures
- Hyperlinks and action settings

## Links

- [GitHub](https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python)
- [Issue Tracker](https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python/issues)
- [PyPI](https://pypi.org/project/aspose-slides-foss/)
- [Aspose.Slides](https://products.aspose.org/slides/)
