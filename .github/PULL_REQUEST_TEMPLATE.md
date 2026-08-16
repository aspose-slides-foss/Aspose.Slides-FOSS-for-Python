<!--
Thank you for the pull request. CONTRIBUTING.md has the detail; this template is the short form.
Delete any section that genuinely does not apply, rather than leaving it blank.
-->

## What this changes

<!-- One or two sentences. If it changes what ends up in the .pptx, name the part and the element:
     "writes <a:graphicFrameLocks> instead of <a:graphicFrameLocking> in ppt/slides/slide1.xml". -->

Closes #

## Why

<!-- The user-visible problem. What did someone see happen, and what did they expect? -->

## How it was verified

<!-- Paste the failing test output from BEFORE the fix, and the passing run after it. A test that
     has never failed has not been shown to test anything. -->

```
```

## Checklist

- [ ] `python -m pytest -q` passes in a clean virtual environment. Warnings are errors here
      (`filterwarnings = ["error"]`), so this is pass or fail, not a judgement call.
- [ ] **If this changes what is written to the file**, there is a test in `tests/conformance/` that
      opens the produced `.pptx` as a ZIP archive and asserts on its XML. A test that reads the
      value back through this library does not count — a writer bug and a matching reader bug
      cancel out.
- [ ] The test is named after the user-visible failure, not after the element or the method.
- [ ] The file is produced through the public API only — no underscore-prefixed members in the test
      setup.
- [ ] New or changed public members carry type annotations. The package ships `py.typed`, so these
      are what a consumer's type checker sees.
- [ ] `CHANGELOG.md` is updated under `## [Unreleased]` if a caller can observe this change.
- [ ] No new runtime dependency. `lxml` is the only one; test-only tools belong in the `test` extra.
- [ ] No build output or generated files in the diff — `dist/`, `build/`, `*.egg-info/`,
      `__pycache__/`, or a `.pptx` a test wrote outside `tmp_path`.
- [ ] If this touches packaging, the data files still ship: `py.typed`,
      `_internal/pptx/Template.pptx` and `_internal/xlsx/template.xlsx`. CI asserts this, and a
      wheel without them imports fine and fails on first use.

## Anything a reviewer should look at closely

<!-- A decision you were unsure about, a case you did not cover, a behaviour you changed on
     purpose. Say it here rather than letting it be found. -->
