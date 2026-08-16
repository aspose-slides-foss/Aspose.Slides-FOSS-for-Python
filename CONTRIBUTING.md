# Contributing

Thank you for considering a contribution. This document is specific to the **Python** edition of
Aspose.Slides FOSS; the .NET, Java and C++ editions live in their own repositories, have a different
API surface, and have their own conventions.

## The one rule that is particular to this project

**A fix to a writer ships with a test that asserts on the produced `.pptx` package — not on what the
library reads back.**

A library agrees with itself for free. If a writer emits `<a:graphicFrameLocking>` where ECMA-376
says `<a:graphicFrameLocks>`, and the matching reader looks for `<a:graphicFrameLocking>`, then every
property reads back exactly what was set, every round-trip test passes, and the file is still one
PowerPoint silently discards the element from. That defect was real and it lived in this repository:
every table and every chart carried it, and no test in a suite of 583 could see it, because none of
them unzipped an output file.

The same shape of mistake hides a relationship id that is never written into the `.rels`, a part with
no content type, an element written in the wrong position of an `xsd:sequence`, and a value the
in-memory object remembers but the writer never emits. Ask the library and the feature is there; look
in the file and it is not.

So: object-model tests are welcome and we have many, but they cannot close a writer bug. Put the
assertion in `tests/conformance/`, where it opens the file as a ZIP archive and reads the XML.

## Prerequisites

Python 3.10 or later, and nothing else. The library is pure Python with one runtime dependency,
`lxml`; there is no compilation step and no build to run before the tests.

The test extra adds `pytest` and [`python-pptx`](https://python-pptx.readthedocs.io/).

What keeps a writer bug from being concealed by a matching reader bug is not `python-pptx` — it is
that the conformance harness unzips the produced file and reads its XML with XPath, never asking this
library to read its own output back. `python-pptx` is a second opinion available where an independent
reader states a failure most clearly, and one conformance test uses it today. Uninstall it and the
suite still passes; that test skips.

## A virtual environment is not optional here

**Install into a fresh virtual environment, always.** This is not the usual generic advice — there is
a specific collision that will otherwise cost you an afternoon.

`aspose` is a [PEP 420](https://peps.python.org/pep-0420/) namespace package: this distribution owns
`aspose/slides_foss/` and ships no `aspose/__init__.py`, which is what lets several `aspose.*`
distributions share the name. The commercial `aspose` package is not built that way. It installs a
real `aspose/__init__.py` that sets

```python
aspose.__path__ = []
```

which turns `aspose` into a regular package with an empty search path and hides **every** other
`aspose.*` portion, this library included. The two cannot share an interpreter, and nothing about the
resulting failure points at the cause: `import aspose.slides_foss` raises a bare
`ModuleNotFoundError`, which reads exactly like a broken checkout.

Rather than let you debug that, the suite refuses to start. `verify_library_not_shadowed()` in
`tests/conformance/harness.py` runs from both `conftest.py` files, and when it detects a captured
namespace it raises a `RuntimeError` beginning:

```
The `aspose` namespace is shadowed: `aspose.slides_foss` cannot be imported
because another distribution owns `aspose/__init__.py` at

    <the path to the file that captured the name>
```

**If you see that message, the test suite is not broken.** It has correctly detected a second
distribution and stopped rather than silently testing whatever else answers to the name `aspose`. The
fix is a clean environment, not a change to the tests:

```bash
python -m venv .venv
.venv/Scripts/pip install -e ".[test]"     # POSIX: .venv/bin/pip
.venv/Scripts/python -m pytest             # POSIX: .venv/bin/python
```

The guard is deliberately narrow. It only speaks up when `aspose` has a `__file__`, which is true of
a regular package that has captured the name and false of a namespace portion. Any other
`ImportError` — a missing `lxml`, a syntax error in the library itself — is re-raised untouched, so
the message never sends you to the wrong problem.

## Build

There is nothing to build to run the tests. To produce the distributions:

```bash
git clone https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python.git
cd Aspose.Slides-FOSS-for-Python
python -m venv .venv
.venv/Scripts/pip install -e ".[test]"
python -m pip install build
python -m build
```

Two things about the packaging are easy to break and worth knowing:

- **The library reads two data files at run time** — `aspose/slides_foss/_internal/pptx/Template.pptx`
  and `aspose/slides_foss/_internal/xlsx/template.xlsx`. `Presentation()` cannot create a deck
  without the first and `add_chart` cannot build a workbook without the second. They are declared in
  `[tool.setuptools.package-data]`, and a packaging change that drops them produces a wheel that
  imports fine and fails on first use. CI asserts both are in the wheel, along with `py.typed`.
- **The sdist ships the whole test suite**, via `graft tests` in `MANIFEST.in`. setuptools collects
  `tests/test_*.py` on its own but not `conftest.py`, not `tests/conformance/` and not the binary
  fixtures in `tests/test_data/`, so without the graft the sdist carries a suite that cannot even be
  collected. Anyone verifying a build from source needs it to run.

## Test

```bash
python -m pytest -q
```

Expect **666 passed, 5 skipped**. The five skips are chart tests that need a `Charts.pptx` fixture
which is not in the repository; they report `Charts.pptx not available` and are not a failure.

The conformance suite is **82 of those tests** and can be run on its own:

```bash
python -m pytest tests/conformance -q
```

That 82 is asserted, not just expected. `tests/test_conformance_suite_is_present.py` collects the
conformance directory in a child process and fails if the count has dropped, because the tests that
open the produced package are exactly the ones whose absence nothing else can see: delete them and
every remaining test passes, the exit code is 0, and the build is green with the instrument removed.
If you delete a conformance test on purpose, lower the floor in that file in the same commit and say
why.

**Warnings are errors.** `filterwarnings = ["error"]` is set in `pyproject.toml` rather than passed
on the command line, so a local run and a CI run reach the same verdict. The suite is clean under it,
which means a new `DeprecationWarning` from a future interpreter or a `ResourceWarning` from a file a
test forgot to close fails the build instead of scrolling past. If a third-party dependency starts
warning about its own internals, add a narrowly targeted `ignore:` line there — do not delete the
rule.

`tests/conftest.py` puts the repository root at the front of `sys.path`, so the suite runs against
the checkout even when a copy of the package is also installed.

### The conformance suite

`tests/conformance/README.md` is the full description. The short version is that `harness.py` is the
whole instrument:

| Piece | What it gives you |
|---|---|
| `ProducedPackage` | a saved file opened as a ZIP: `read`/`text`/`xml` for one part, `namelist`, `parts_matching`, `findall`/`find_one` with the OOXML prefixes already bound, `relationships`, `content_type_of` |
| `assert_element(part, xpath, attrs=, children=, child_order=)` | the element exists, carries the attributes, has the children, and its children are in ECMA-376 sequence |
| `assert_package_is_consistent()` | the package-level rules below, together |
| `open_with_python_pptx()` | third-party read-back, for when an independent reader states the failure most clearly |
| `verify_library_not_shadowed()` | the import guard described above |

The package-level rules each caught a real defect:

1. **Every `r:id`, `r:embed` and `r:link` resolves** in that part's own `.rels`. The classic failure
   is an image whose bytes are in the package, whose `<a:blip r:embed>` is in the package, and whose
   joining relationship is not.
2. **No relationship targets a part that is missing.**
3. **Every part resolves a content type** through an `Override` or a `Default`, and where the path
   determines the type it is the right one. ISO/IEC 29500-2 §10.1.2 makes the content type a part's
   *identity*: a slide that falls through to `<Default Extension="xml"/>` is an `application/xml`
   part, and a strict consumer will not treat it as a slide.
4. **Every part is reachable** by walking relationships from `_rels/.rels`. This is the only rule that
   can see an orphan — a part nothing points at, carrying its own `Override` so that nothing dangles
   and no other check objects.

**Child order matters.** OOXML complex types are `xsd:sequence`, so `<a:rPr>` with its children in
the wrong order is invalid even though every child is correct. `CHILD_ORDER` holds the sequences from
ECMA-376 for the elements these tests touch; add a sequence there before asserting on a new element
type.

`python-pptx` is a dependency of the `test` extra **only**. It must never become a runtime dependency
of the library: this library writes OOXML by hand, and validating that output with another library
bundled into the same package would prove much less than it appears to.

## What a good pull request looks like

1. **It fixes one thing.** A pull request that repairs a writer and also reformats three modules is
   two pull requests.
2. **It has a failing test first.** Write the test against the unfixed code, watch it fail, and put
   that failure message in the pull request description. A test that has never failed has not been
   shown to test anything.
3. **The test names the user-visible failure**, in the words a user would use:
   `test_a_comment_reply_survives_being_saved`, not `test_parent_cm_id_attribute`. The name is the
   bug report.
4. **It writes its file through the public API only.** If a case needs an underscore-prefixed member
   to set it up, that is a missing public API and worth saying so in the pull request.
5. **It says what it changed about the file.** "Writes `<a:graphicFrameLocks>` instead of
   `<a:graphicFrameLocking>` in `ppt/slides/slide1.xml`" is reviewable. "Fixed tables" is not.
6. **It updates `CHANGELOG.md`** under `## [Unreleased]`, in the language a caller would use, if the
   change is one a caller can observe.
7. **It does not add a runtime dependency.** `lxml` is the only one, and keeping it that way is a
   property worth having. Test-only tools go in the `test` extra. If you believe a runtime dependency
   is genuinely necessary, open an issue and make the case before writing the code.
8. **It leaves no build output in the diff** — no `dist/`, no `build/`, no `*.egg-info/`, no
   `__pycache__/`, and no `.pptx` a test wrote. Tests write into `tmp_path`.

### Style

Follow the layout and naming of the code you are changing. There is no formatter configuration and no
linter configuration in this repository, so tooling will not decide it for you.

Public API names follow Python convention — `snake_case` methods and properties on `PascalCase`
classes — while mirroring the shared cross-edition API. That is why you see `add_auto_shape` rather
than `AddAutoShape`, and why the interface classes are named `IShape`, `IPresentation` and so on.
Annotate what you write. The package ships a `py.typed` marker, so every annotation in it is what a
consumer's type checker sees — and every parameter without one is an `Any` that checker will not
question. Coverage today is partial, roughly two thirds of parameters and return types, so a new or
edited signature is the cheapest place to close the gap. CI runs `mypy` over the package and fails if
the error count rises above the recorded baseline, which is what stops the gap widening; lowering
that number is welcome in its own pull request.

### Behaviour that is deliberate, not a bug

Before filing a fix for one of these, please open an issue instead — they are decisions with
reasoning behind them:

- **`save` raises `ValueError` for the fourteen `SaveFormat` values it does not write.** It will not
  write a presentation package under a name claiming to be PDF, ODP or HTML. The message names the
  seven formats that do work.
- **The file name and the `SaveFormat` are independent.** `save("deck.pptx", SaveFormat.POTX)` writes
  a genuine template under a `.pptx` name, and PowerPoint refuses a file whose extension disagrees
  with the content type declared inside it. Give the file the extension of the format you asked for.
- **Assigning to a property an object does not have raises `AttributeError`** rather than being
  accepted and discarded. A misspelt property name fails where it is written. Names beginning with an
  underscore are unaffected. This is what made a missing hyperlink writer invisible for as long as it
  was.
- **Comment threads are rebuilt from the classic comment list on save.** A PowerPoint-authored deck
  can carry resolved status, @-mentions and reply-to-a-reply chains that the classic list cannot
  express; those are lost if the presentation's comment authors are touched before saving. Loading
  and saving without going near comments leaves the file's own threads alone.
- **Unknown parts are preserved verbatim** on load and save. Opening and re-saving never strips
  content this library does not yet understand.

## Continuous integration

Every push and pull request runs the full suite on `ubuntu-latest`, `windows-latest` and
`macos-latest` against Python 3.10, 3.11, 3.12, 3.13 and 3.14 — fifteen jobs, the whole cross product
of what the packaging metadata claims. `requires-python` is `>=3.10` and the classifiers name those
five versions; anything dropped from the matrix has to be dropped from those claims at the same time.

A second job then builds the sdist and the wheel, runs `twine check --strict`, asserts that the
distributions contain the data files and the documents the metadata and the README imply, **installs
the wheel into a throwaway environment and runs the suite again against it**, and emits a CycloneDX
SBOM. The matrix tests the checkout; that job tests what a user actually gets.

A third job runs `mypy` over the package with a pinned version, and fails if the error count is
higher than the baseline recorded in the workflow. It is not a clean-tree gate — the count is not
zero — it is a ratchet, so the number can only go down.

If CI is red the pull request is not ready, including when the failure is on a platform or an
interpreter you did not use.

## Licence

By contributing you agree that your contribution is licensed under the
[MIT License](LICENSE), the same terms as the rest of the project.
