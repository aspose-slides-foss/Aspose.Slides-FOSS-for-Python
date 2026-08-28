# Security policy

## Supported versions

Security fixes are made on the default branch of this repository and released from it. There is no
long-term support branch and no backporting to an older release.

| Version | Supported |
|---|---|
| The default branch | yes |
| `26.8.0` (latest on PyPI) | fixes land in the next release, not as a patch to this one |
| `26.4.0` and earlier | no — upgrade |

Check what you have with:

```bash
python -m pip show aspose-slides-foss
```

Note that the changes recorded at the top of [CHANGELOG.md](CHANGELOG.md) under `## [Unreleased]`
are not in `26.8.0`. If you are testing something you read about there, install from a checkout
rather than from PyPI:

```bash
pip install git+https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python.git
```

## Reporting a vulnerability

**Do not open a public issue for a security problem, and do not attach a proof-of-concept file to
one.**

Use GitHub's private vulnerability reporting on this repository:
[**Report a vulnerability**](https://github.com/aspose-slides-foss/Aspose.Slides-FOSS-for-Python/security/advisories/new).
It opens a private advisory only the maintainers can read, and it lets you attach files and discuss a
fix before anything becomes public.

If that page is not available to you, open a public issue containing **only** the sentence "I would
like to report a security issue privately" and no details at all, and wait to be contacted.

Please include, as far as you can:

- the version or commit you tested (`python -m pip show aspose-slides-foss`, or `git rev-parse HEAD`),
- the Python version and operating system (`python -VV` and your platform),
- a minimal script, and the `.pptx` it needs — attach the file, or give a script that generates it,
- what happens, and what you expected instead,
- the impact you believe it has.

You will get an acknowledgement. We cannot promise a fix deadline for a project with no paid support
contract behind it, but you will be told what is happening and when a fix lands, and you will be
credited in the advisory unless you ask not to be.

## What is in scope

This library parses untrusted input. A `.pptx` is a ZIP archive full of XML, and both layers are
attacker-controlled when the file came from outside. Reports about the handling of a malicious or
malformed presentation are in scope, including:

- a crafted archive or XML that causes a crash, an unbounded allocation or an infinite loop —
  including archive entries that expand enormously relative to their compressed size,
- a part name or relationship target that escapes the package and reaches the file system when a
  presentation is opened or saved,
- XML processing that reaches the network or the local disk — external entity resolution, external
  DTD or schema fetching, XInclude,
- anything that lets a presentation influence the process beyond the object model it is parsed into.

Because parsing is done with `lxml`, a report about XML entity handling should say whether it
reproduces against this library's own parser configuration; that is the part we can fix here.

## What is out of scope

- **Missing capabilities.** `save` raising `ValueError` for a format it does not write, and the gaps
  listed under *Limitations* in the README, are documented behaviour rather than vulnerabilities.
- **The `aspose` namespace collision.** The commercial `aspose` package installs an
  `aspose/__init__.py` that sets `aspose.__path__ = []` and hides this library. That is a packaging
  incompatibility, it is documented in [CONTRIBUTING.md](CONTRIBUTING.md), and the fix is a separate
  virtual environment.
- **Vulnerabilities in `lxml`, in `libxml2` or in CPython itself.** Report those to their own
  maintainers. If a fix here would mitigate one, say so and we will look at it.
- **Vulnerabilities in the commercial Aspose.Slides product**, which is different software. Report
  those through [Aspose support](https://forum.aspose.com/c/slides/11).
- **Findings from an automated scanner with no demonstrated impact on this library**, including
  dependency alerts for a version this project does not require.
