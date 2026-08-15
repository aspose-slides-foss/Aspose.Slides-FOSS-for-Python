# Conformance tests

These tests assert on the `.pptx` **package** this library produces: they write
a file, unzip it, parse the XML parts and check the elements, attributes,
relationships and content types that ECMA-376 requires.

## Why not just read the file back?

Because a reader and a writer that share a mistake agree with each other.

If the writer emits an element with the wrong name and the reader looks for that
same wrong name, a round-trip test passes, the property comes back exactly as it
was set, and the file is still one PowerPoint refuses to open. The same is true
of a value the writer never emits but the in-memory object still remembers: ask
the library and it says the feature is there; look in the file and it is not.

So the rule for everything in this directory is:

> **Assert on the produced package, never on the library's own read-back.**

A test that calls this library to check this library does not belong here. Put
those in the suite one level up, where they are useful for a different purpose.

Where an independent opinion helps, the harness opens the file with
[`python-pptx`](https://python-pptx.readthedocs.io/) — a separate
implementation with its own idea of what a valid package is. It is a test-only
dependency:

```
pip install -e ".[test]"
```

## What the harness checks

`harness.py` is the whole instrument. Its pieces:

**`ProducedPackage`** — a saved file, opened for inspection.

| method | what it does |
| --- | --- |
| `read(part)` / `text(part)` / `xml(part)` | raw bytes, text, or a parsed `lxml` root for one part |
| `namelist`, `parts_matching(regex)` | what is in the ZIP |
| `findall(part, xpath)`, `find_one(part, xpath)` | XPath with the OOXML prefixes already bound (see `NS`) |
| `assert_element(part, xpath, attrs=, children=, child_order=)` | the element exists, carries the attributes, has the children, and its children are in ECMA-376 sequence |
| `relationships(part)`, `relationship(part, id)` | that part's `_rels`, as a dict |
| `content_types()`, `content_type_of(part)` | what a consumer resolves for a part |
| `open_with_python_pptx()` | third-party read-back |

**Three package-level rules**, each of which has caught a real defect, and all
three together as `assert_package_is_consistent()`:

1. `assert_relationship_ids_resolve()` — every `r:id`, `r:embed` and `r:link` in
   every part resolves to a `Relationship` in *that part's* `.rels`. A dangling
   reference is the classic failure: the image bytes are in the package, the
   element that points at them is in the package, and the relationship joining
   them is not.
2. `assert_relationship_targets_exist()` — no relationship names a part that has
   been deleted.
3. `assert_content_types_resolve()` — every part resolves a content type through
   an `Override` or a `Default`, no `Override` names a missing part, and where
   the part path determines the type (a slide, a layout, a theme, the
   presentation itself) it is the right one. ISO/IEC 29500-2 §10.1.2 makes the
   content type the part's *identity*: a slide part that falls through to
   `<Default Extension="xml"/>` is an `application/xml` part, and a strict
   consumer will not treat it as a slide.

**Child order.** OOXML complex types are `xsd:sequence`, so `<a:rPr>` written
with its children in a different order is invalid even though every child is
correct. `CHILD_ORDER` holds the sequences from ECMA-376 for the elements these
tests touch, and `assert_children_in_order()` reports the found order against
the expected one. Add a sequence there before asserting on a new element type.

**The import guard.** `aspose` is a namespace package. Another distribution
installed under the same name can make it a regular package and set
`aspose.__path__ = []`, which hides this library completely; the import then
fails with a bare `ModuleNotFoundError` that reads like a broken checkout.
`verify_library_not_shadowed()` turns that into a sentence saying what happened
and how to get a clean environment. It runs from both `conftest.py` files, so
the whole suite refuses to start rather than silently testing something else.

## Fixtures

| fixture | what you get |
| --- | --- |
| `produced` | `produced(pres)` saves, disposes the presentation and returns a `ProducedPackage`. Takes an optional `SaveFormat` and filename. Disposing is deliberate: it removes the temptation to fall back on the in-memory object. |
| `blank_presentation` | a one-slide deck from the bundled template |
| `shape_on_blank_slide` | `shape_on_blank_slide(with_text="…")` → `(presentation, shape)` |
| `python_pptx` | the third-party reader, skipped with a useful message if absent |
| `test_data_dir` | `tests/test_data/`, from the suite-wide `conftest.py` |

## Adding a case

1. **Name the test after the user-visible failure**, not after the element.
   `test_a_comment_reply_survives_being_saved` says what a user loses;
   `test_parent_cm_id_attribute` does not.
2. **Write the docstring for someone who has not read the schema.** State what
   the user does, what happens instead, and which clause of ECMA-376 settles it.
   The comment at the top of each module is where the explanation goes.
3. **Produce the file through the public API only.** If the test needs an
   internal to set something up, that is a missing public API and worth saying
   so.
4. **Assert on the package.** Use `find_one` and `assert_element`, and make the
   assertion message print what was found — a failure should be readable without
   opening the file.
5. **Run it against the unfixed code first.** A conformance test that passes the
   moment it is written is either testing something else or documenting
   behaviour that is already correct; the second is fine, but say so in the
   docstring, as `test_package_baseline.py` does.
6. **Never weaken an assertion to make a test pass.** If an existing test
   asserts the broken behaviour, that test is itself the defect report.
