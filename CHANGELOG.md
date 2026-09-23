# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
uses a CalVer version scheme — `YY.M.PATCH`, matching the other language editions of the library.

## [Unreleased]

The latest release on PyPI is `26.8.0`, and **none of the changes below are in it.** They are on the
default branch and will go out in the next release.

The theme of this entry is that the library now writes packages other software can read. Several of
the defects it repairs were invisible to the test suite, because a test that reads a value back
through the same library that wrote it agrees with a writer that is wrong. The new conformance suite
unzips the file instead.

**If you built against an earlier commit, read *Changed* first — calls that used to succeed now
raise, and files this version writes are not byte-identical to the ones the last one wrote.**

### Changed

- **The six PowerPoint formats produce genuinely different packages.** `save(path,
  SaveFormat.POTX)` and its siblings previously wrote a package whose `/ppt/presentation.xml` was
  still declared as a *presentation*, so the file contradicted its own extension and PowerPoint
  reported "PowerPoint can't open this file because its file extension has changed". Each of `PPTX`,
  `PPTM`, `PPSX`, `PPSM`, `POTX` and `POTM` now declares its own main-part content type. An ordinary
  `.pptx` save is unaffected *by this change* — `PPTX` declares the content type it always did. It is
  not byte-for-byte identical to what the previous version wrote, because two of the changes below
  rewrite `docProps/core.xml` and `docProps/app.xml` on every save.
- **A refused save says what to ask for instead.** Saving to one of the fourteen `SaveFormat` values
  this library does not write still raises `ValueError`, as it always has, but the message now names
  the seven that do work: `Export format 'Pdf' is not supported; this library writes Md, Potm, Potx,
  Ppsm, Ppsx, Pptm, Pptx`.
- **Assigning to a property an object does not have raises `AttributeError`** instead of being
  accepted and silently discarded, so a misspelt property name fails where it is written:
  `AutoShape has no property 'definitely_not_a_property'; the assignment would have been accepted and
  then silently discarded`. Names beginning with an underscore are unaffected. This is the change
  most likely to surface a latent bug in existing code — an assignment that never did anything now
  says so.
- **The same check now covers the objects most code touches first.** It was at first applied to
  shapes and the format objects only, and `Presentation`, `Slide`, `LayoutSlide`, `MasterSlide`,
  `NotesSlide`, `TextFrame`, `Paragraph`, `Portion`, `Cell`, `SlideShowTransition` and `Hyperlink`
  still accepted a misspelt name — `portion.txt = "Hello"` succeeded and wrote nothing. Each of
  them now raises `AttributeError` in the same way. Code that stored its own public attributes on
  these objects must use a name beginning with an underscore, or keep the data elsewhere.
- **`line_format` and `three_d_format` on a group shape return `None`.** `CT_GroupShapeProperties`
  has no outline and no 3-D element, and setting either produced a file PowerPoint refuses to open
  from a call that reported success. The assignment now fails where it is made rather than at the far
  end of a save. Shapes *inside* a group are unaffected and keep both.
- **`dcterms:modified` is stamped on every save.** It was previously updated only if the caller had
  touched `document_properties` for some other reason, so an ordinary save left the bundled
  template's build date in place and the file claimed it had not been modified since.
- **`docProps/app.xml` is regenerated on save.** It was copied from the bundled template and never
  recomputed, so every deck reported one slide, zero paragraphs and the template's own slide title
  whatever it actually contained. The counts and the slide titles are now read back out of the
  package after it is written.
- **A comment reply is written as a threaded comment.** It was previously written as a `parentCmId`
  attribute, which is not in the schema, which no consumer reads, and which did not reach the file
  anyway — so a reply was saved as a second, unrelated comment. Replies now go to
  `ppt/threadedComments/` and `ppt/authors.xml`, alongside the classic list, which is still written
  for older readers with its replies linked through the `p15:threadingInfo` extension.
- **Source-incompatible:** `IHyperlinkContainer` was an empty abstract base class and now declares
  `hyperlink_click` and `hyperlink_mouse_over` as abstract properties. A third-party class inheriting
  from it without defining both no longer instantiates — at construction, not at assignment, which is
  the point: the interface now states what implementing it means.
- **Transitions introduced in PowerPoint 2010 and later are written inside `mc:AlternateContent`**,
  as PowerPoint writes them. The 35 transition types whose element is outside the ECMA-376
  namespace — Vortex, Ripple, Cube, Curtains, Morph and the rest of the `p14`, `p15` and `p159`
  types — were written bare inside `p:transition`, where a reader that does not know the extension
  has no fallback and the Open XML SDK rejects Morph outright. Each now goes in an `mc:Choice` that
  requires its namespace, with a `p:fade` in `mc:Fallback` carrying the same speed and advance
  settings. The 21 standard transitions are written as before. Code that inspects the slide XML
  directly will find these transitions one level deeper.
- **`TransitionType.BOX` writes a different element, and some files read back a different type.**
  `BOX` was written as `p14:prism isContent="1"`, which is what PowerPoint writes for *Rotate*; it
  is now `isInverted="1"`, PowerPoint's Box. Reading a file, `p14:prism isContent="1"` — including
  every Box this library wrote before — now reads as `TransitionType.ROTATE`, which is how PowerPoint
  itself shows it.

### Added

- **Hyperlinks on text portions and on whole shapes**, on click and on mouse over. The properties
  existed and stored a value; nothing wrote it, so the link was simply absent from the file. A link
  is now written inside `a:rPr` for a portion — `a:hlinkClick` or `a:hlinkMouseOver` — and inside
  `p:cNvPr` for a shape, where `CT_NonVisualDrawingProps` names the mouse-over element
  `a:hlinkHover`. Each carries an `r:id` resolving to an external relationship in the owning part's
  `.rels`. Assigning `None` removes the element and the relationship together.
- **A conformance test suite** — 335 tests that write a file through the public API, open it as a ZIP
  archive and assert on the XML inside, never asking the library to read its own output back. See
  `tests/conformance/README.md`.
- **A `py.typed` marker.** The package declared `Typing :: Typed` and shipped no marker, so every
  type checker read it as untyped and inferred `Any` throughout — `mypy` reported "module is
  installed, but missing library stubs or py.typed marker". The marker now ships, so the annotations
  that are there reach a consumer's type checker. **Coverage is partial**: roughly two thirds of the
  parameters and of the return types carry an annotation, and some of the most-used entry points do
  not — `Presentation.save` is `(*args, **kwargs) -> None`, `IImageCollection.add_image` and
  `ShapeCollection.add_picture_frame` take unannotated parameters. An unannotated parameter degrades
  to `Any` rather than to an error, so the marker does not make a consumer's checker fail; it does
  mean "no annotation" now reads as `Any` rather than as "this package has no type information".
  CI runs `mypy` over the package and fails if the error count grows, so the gap closes and does not
  widen.
- **A source distribution whose tests can actually be run.** setuptools collected `tests/test_*.py`
  by itself but not `conftest.py`, not the conformance suite and not the binary fixtures, so the
  sdist shipped a suite that could not even be collected.
- **Continuous integration** — the full suite on Linux, Windows and macOS across Python 3.10 to 3.14,
  a `mypy` run that fails if the error count rises above the recorded baseline, then a build of both
  distributions, `twine check --strict`, an assertion that the wheel and sdist contain the data files
  and the documents the metadata and the README imply, a second run of the suite against the
  *installed* wheel, and a CycloneDX SBOM.
- **A floor under the conformance suite.** Deleting `tests/conformance/test_*.py` used to leave every
  job green: the rest of the suite passed, the exit code was 0, and nothing said the tests that read
  the produced package were gone. `tests/test_conformance_suite_is_present.py` now collects that
  directory and fails if the count has dropped.
- **A release workflow** using PyPI Trusted Publishing with PEP 740 attestations rather than a
  long-lived API token. See `PUBLISHING.md`.
- **Community documentation** — this changelog, `CONTRIBUTING.md`, `SECURITY.md`,
  `CODE_OF_CONDUCT.md`, issue forms and a pull request template.

### Fixed

- **Graphic frames lock correctly.** The element was written as `a:graphicFrameLocking`, which is the
  name of the *type*, not of the element `CT_NonVisualGraphicFrameProperties` accepts. Every table
  and every chart was schema-invalid, and because PowerPoint tolerates an unknown element and
  discards it, no frame was ever actually locked against grouping. It is now `a:graphicFrameLocks`.
- **A newly enabled effect carries the attributes the schema requires.**
  `enable_outer_shadow_effect()` and its siblings inserted an empty element and stopped —
  `<a:outerShdw/>` with no colour, `<a:softEdge/>` with no `rad`, `<a:prstShdw/>` with no `prst`,
  `<a:fillOverlay/>` with no blend and no fill. PowerPoint refuses the whole file rather than
  ignoring an incomplete effect, so a deck carrying only an enabled outer shadow would not open. An
  effect that already exists is left exactly as the caller configured it.
- **Setting any 3-D property writes a complete `a:scene3d`.** `CT_Scene3D` requires both a camera and
  a light rig; touching only the camera produced a scene with no light rig, and setting depth,
  extrusion height or contour width wrote `a:sp3d` with no scene at all, so the shape had no camera
  and no lighting and rendered flat.
- **Lazily created children are inserted at their position in the schema sequence.** These types are
  `xsd:sequence`, and children were appended in the order the caller happened to set the properties —
  so the same formatting expressed in a different order produced a valid file or an invalid one. For
  `a:rPr`, five of the six orderings of latin font, highlight and fill were invalid. One table of
  ECMA-376 sequences now covers text character properties, shape properties, line properties, table
  cell and table properties, background properties, `a:scene3d` and group shape properties.
- **`p:transition` is written after `p:clrMapOvr`**, the position `CT_Slide` gives it.
- **A shape's mouse-over hyperlink is named `a:hlinkHover`.** It was written as `a:hlinkMouseOver`,
  which is the correct name for the same link inside run properties but not inside
  `CT_NonVisualDrawingProps`, so PowerPoint read no mouse-over action from the shape at all. Text
  portions keep `a:hlinkMouseOver`, which is right there.
- **A group shape gets the `p:grpSpPr` element `CT_GroupShapeProperties` defines**, a shorter sequence
  than the one for an ordinary shape. Without an entry for it, a lazily created fill or effect landed
  wherever the caller's order put it: 22 of the 24 permutations of setting a fill, an outline, an
  effect and a depth on a group produced an out-of-sequence `p:grpSpPr`; none now does.
- **A slide's threaded comment part is reused instead of orphaned on every save.** A presentation
  with one comment, saved four times, ended up with four `ppt/threadedComments/` parts, three of them
  unreferenced — and because each orphan carried its own content-type `Override`, nothing dangled and
  no consistency check objected. Worse, deleting a comment left its text in the shipped package in
  full, in a part nothing points at. Emptying the comment list now removes the part, its `Override`
  and its relationship, and any thread part no relationship names is cleaned up on save — so opening
  and re-saving a package that already carries orphans repairs it.
- **3-D bevels and colours survive whatever order they are set in.** `bevel_top`, `bevel_bottom`,
  `extrusion_color` and `contour_color` each create a child of `a:sp3d`, and each was appended, so
  the file took the order the caller happened to use. `CT_Shape3D` is a sequence — `bevelT`,
  `bevelB`, `extrusionClr`, `contourClr` — and 23 of the 24 possible orders were invalid: setting the
  contour colour before the top bevel gave a shape that PowerPoint shows with no bevels and a white
  extrusion. The four children now go where the schema puts them, whatever the order of the calls.
- **A text warp survives an autofit set before it.** `text_frame_format.autofit_type` and
  `.transform` appended their elements to `a:bodyPr`, whose `CT_TextBodyProperties` sequence puts the
  warp first, then the autofit, then the 3-D text elements. Setting the autofit before the warp — or
  either of them after `three_d_format` — wrote an out-of-sequence `a:bodyPr`, 20 of the 24 orders
  of those settings, and PowerPoint kept the autofit and showed the text unwarped. Both elements are
  now inserted at their schema position.
- **A text effect survives formatting set before it.** `portion_format.effect_format` created
  `a:effectLst` by the rule for shape properties — before any 3-D element, otherwise at the end — so
  in run properties it landed after the highlight, underline, fonts or hyperlink already set there.
  `CT_TextCharacterProperties` puts the effect list before all of those; four orders in five of a
  typical set of run formatting were invalid, and a shadow enabled after the font was dropped by
  PowerPoint. The effect list now goes where its container's sequence puts it, for run properties,
  shape properties and the others alike.
- **The Orbit, Rotate and Box transitions are the ones PowerPoint shows.** `TransitionType.ORBIT`
  and `ROTATE` were written as `p14:orbit` and `p14:rotate`, which the PowerPoint 2010 namespace
  does not define, so PowerPoint showed no transition at all; `BOX` was written the way PowerPoint
  writes Rotate. PowerPoint writes all four of Cube, Rotate, Box and Orbit as one `p14:prism`
  element told apart by `isContent` and `isInverted`, and the library now writes exactly what
  PowerPoint does for each.
- **Setting a transition on a slide opened from a PowerPoint file replaces the one it had.**
  PowerPoint saves every transition inside `mc:AlternateContent`, which the library did not look
  inside: the slide's transition read as `NONE`, and setting a type added a second `p:transition`
  beside the existing one, which `CT_Slide` does not allow — PowerPoint refuses to open the result.
  The existing transition is now read, and setting a type replaces it, keeping its speed, advance
  settings and duration.

### Known limitations

Not defects, and not scheduled: rendering and conversion of any kind (PDF, HTML, XPS, images), the
binary `.ppt` family, OpenDocument, SmartArt, OLE objects, mathematical text, VBA macros, digital
signatures, encryption, action settings other than external hyperlinks, presentation sections, and a
public API for the slide size. The README lists these with the detail.

[Unreleased]: https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python/commits/main
