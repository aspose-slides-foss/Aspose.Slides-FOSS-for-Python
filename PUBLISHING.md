# Publishing a release

`aspose-slides-foss` is published to [PyPI](https://pypi.org/project/aspose-slides-foss/)
by `.github/workflows/publish.yml`. There is no API token in this repository
and there is not meant to be one: the workflow authenticates with **PyPI
Trusted Publishing**, an OpenID Connect exchange in which GitHub mints a
short-lived token describing the workflow that asked for it, and PyPI trades
that for upload rights valid for a few minutes. Nothing long-lived exists to
leak and nothing has to be rotated.

## Before the first release: two things a maintainer must do by hand

Neither can be done from inside this repository, and until both are done the
publish workflow fails at the upload step.

### 1. Register the trusted publisher on PyPI

Go to
<https://pypi.org/manage/project/aspose-slides-foss/settings/publishing/>
and add a GitHub publisher with exactly these values. Every field is compared
literally against a claim in the OIDC token; a mismatch anywhere produces an
`invalid-publisher` error and no upload.

| Field | Value |
| --- | --- |
| PyPI Project Name | `aspose-slides-foss` |
| Owner | `aspose-slides-foss` |
| Repository name | `Aspose.Slides-FOSS-for-Python` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

The workflow name is the *filename* of the workflow that performs the upload,
not the `name:` inside it.

### 2. Create the `pypi` environment in this repository

Settings → Environments → New environment → `pypi`.

The environment is not decoration: PyPI is told to accept tokens only from
jobs running in an environment of that name, so a workflow added later that
skips it cannot publish. Required reviewers or a branch restriction can be
attached here if releases should need a second pair of eyes.

## Before every release: the version must not already exist

PyPI refuses to overwrite a released file, and it does not allow a deleted
version to be re-uploaded. `version` in `pyproject.toml` must therefore name a
version that has never been published, or the upload fails with
`File already exists`.

At the time of writing, `pyproject.toml` says `26.8.0`, and `26.8.0` is
already on PyPI. **Bump it before cutting the first release through this
workflow.**

The workflow now says so itself rather than letting you find out at the end.
Its first job asks PyPI whether the version in `pyproject.toml` exists and
refuses to go on if it does, which takes seconds; the whole build only starts
after that passes. The same job compares the release tag against
`pyproject.toml`, so a mismatched tag also fails before the build rather than
after it.

## Cutting a release

1. Bump `version` in `pyproject.toml` and commit it.
2. Tag the commit and push the tag. The tag may be `v<version>` or
   `<version>`; the workflow strips a leading `v` before comparing, and
   refuses to publish if what is left does not match the version it built.
3. Publish a GitHub Release from that tag.

Publishing the release starts `publish.yml`, which:

1. checks, before anything is built, that the tag names the version in
   `pyproject.toml` and that PyPI does not already have that version;
2. runs `ci.yml` in full — the whole test suite on Linux, Windows and macOS
   across Python 3.10 to 3.14, a `mypy` run against the recorded baseline, then
   a build, `twine check --strict`, an inventory of the wheel and sdist
   contents, a run of the suite against the installed wheel, and a CycloneDX
   SBOM;
3. downloads the distributions those jobs produced — the release uploads the
   artefact that was tested, not a rebuild;
4. checks the release tag against the built version, which is the last thing
   that can still disagree;
5. uploads to PyPI with PEP 740 attestations.

If any of that fails, nothing is uploaded.

## Checking it worked

- The project page shows the new version, the README rendered as Markdown, and
  the licence as MIT.
- Each file on <https://pypi.org/project/aspose-slides-foss/#files> shows a
  provenance link. Releases made before this workflow existed have none, and
  cannot be given any retroactively.
- `pip download aspose-slides-foss==<version>` in a clean environment fetches
  the wheel and installs `lxml` and nothing else.

## Building and checking locally

The same steps CI runs, minus the upload:

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check --strict dist/*
```

Do not run `twine upload` by hand. A manual upload has no attestations, is not
tied to a tested commit, and would need an API token — the thing this setup
exists to avoid.
