"""The conformance suite has to still be there for the build to mean anything.

A test suite reports on the tests it collects, not on the tests that were
written.  Delete ``tests/conformance/test_*.py`` and every job stays green: the
remaining tests pass, the exit code is 0, and nothing anywhere says that the
part of the suite that opens the produced ``.pptx`` and reads the XML inside it
is gone.  That is the same failure this directory exists to prevent, one level
up — a check that agrees with itself because the thing it was checking stopped
being asked.

So the count is asserted.  It is a floor, not an equality: adding tests must
never fail the build.  Raise ``FLOOR`` when the suite grows; do not lower it.
A test removed on purpose — because the behaviour it asserted is gone — is a
one-line change to this number, made deliberately, in a commit that says why.

The count is taken by collecting the directory in a child process rather than
by counting ``def test_`` in the sources, because most of these tests are
parameterised and the number that matters is the number that runs.  A child
process also makes the answer independent of what this session was asked to
run, so ``pytest tests/test_conformance_suite_is_present.py`` gives the same
verdict as a full run.
"""
import pathlib
import re
import subprocess
import sys

CONFORMANCE = pathlib.Path(__file__).parent / "conformance"

#: The number of conformance tests that must be collectable.  Also stated in
#: CONTRIBUTING.md, where it is an expectation; here it is the assertion.
FLOOR = 82


def test_the_conformance_suite_still_collects_every_test_it_had():
    assert CONFORMANCE.is_dir(), f"the conformance suite is missing entirely: {CONFORMANCE}"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(CONFORMANCE),
            "--collect-only",
            "-q",
            "-p",
            "no:cacheprovider",
        ],
        capture_output=True,
        text=True,
        timeout=600,
    )
    # Exit code 5 is pytest's "no tests collected", which is the very case this
    # check exists for: it has to become a count of zero rather than an error
    # about running pytest.
    if result.returncode == 5:
        collected = 0
    else:
        assert result.returncode == 0, (
            "collecting the conformance suite failed with exit code "
            f"{result.returncode}:\n{result.stdout}\n{result.stderr}"
        )
        match = re.search(r"(\d+) tests? collected", result.stdout)
        assert match, (
            "could not read a collected count out of pytest's output:\n" + result.stdout
        )
        collected = int(match.group(1))

    assert collected >= FLOOR, (
        f"the conformance suite collects {collected} tests; it had {FLOOR}. "
        "Tests that assert on the produced package are the only ones that can "
        "see a writer bug, so losing them silently is the failure this check "
        "exists to catch. If the removal was deliberate, lower FLOOR in this "
        "file and say why in the commit."
    )
