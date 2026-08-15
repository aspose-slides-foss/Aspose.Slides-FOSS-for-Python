"""A harness for asserting on the *produced package*.

Every helper here works on the ``.pptx`` file after it has been written: it
unzips the package, parses the XML parts with ``lxml`` and asserts on the
elements, attributes and relationships that ECMA-376 requires.  Nothing here
asks the library to read its own output back — a reader and a writer that share
a bug agree with each other and disagree with PowerPoint, so a read-back
assertion cannot see that class of defect at all.

The public surface is:

``verify_library_not_shadowed()``
    Raise with a diagnosis if some other distribution has taken over the
    ``aspose`` namespace package.
``ProducedPackage``
    A saved ``.pptx``, opened for inspection.
``assert_children_in_order()`` / ``CHILD_ORDER``
    ECMA-376 child sequences for the element types these tests touch.
``open_with_python_pptx()``
    Third-party read-back, for the cases where an independent reader is the
    clearest statement of the failure.
"""

from __future__ import annotations

import posixpath
import re
import zipfile
from typing import Iterable, Iterator, Optional

import lxml.etree as ET

# --------------------------------------------------------------------------
# Namespaces
# --------------------------------------------------------------------------

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "p14": "http://schemas.microsoft.com/office/powerpoint/2010/main",
    "p15": "http://schemas.microsoft.com/office/powerpoint/2012/main",
    "p188": "http://schemas.microsoft.com/office/powerpoint/2018/8/main",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

R_NS = NS["r"]

#: Relationship types referenced by name in the tests.
REL_TYPE = {
    "image": R_NS + "/image",
    "hyperlink": R_NS + "/hyperlink",
    "slide": R_NS + "/slide",
    "slideLayout": R_NS + "/slideLayout",
    "slideMaster": R_NS + "/slideMaster",
    "notesSlide": R_NS + "/notesSlide",
    "notesMaster": R_NS + "/notesMaster",
    "comments": R_NS + "/comments",
    "chart": R_NS + "/chart",
    "theme": R_NS + "/theme",
}

#: Content types ECMA-376 (and the Microsoft extensions PowerPoint writes)
#: prescribe for the part paths these tests produce.  Only paths that are
#: unambiguous from their name appear here; anything else is merely required to
#: resolve *some* content type.
EXPECTED_CONTENT_TYPES = {
    r"^ppt/presentation\.xml$": (
        "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml",
        "application/vnd.ms-powerpoint.presentation.macroEnabled.main+xml",
        "application/vnd.openxmlformats-officedocument.presentationml.slideshow.main+xml",
        "application/vnd.ms-powerpoint.slideshow.macroEnabled.main+xml",
        "application/vnd.openxmlformats-officedocument.presentationml.template.main+xml",
        "application/vnd.ms-powerpoint.template.macroEnabled.main+xml",
    ),
    r"^ppt/slides/slide\d+\.xml$": (
        "application/vnd.openxmlformats-officedocument.presentationml.slide+xml",
    ),
    r"^ppt/slideLayouts/slideLayout\d+\.xml$": (
        "application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml",
    ),
    r"^ppt/slideMasters/slideMaster\d+\.xml$": (
        "application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml",
    ),
    r"^ppt/notesSlides/notesSlide\d+\.xml$": (
        "application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml",
    ),
    r"^ppt/notesMasters/notesMaster\d+\.xml$": (
        "application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml",
    ),
    r"^ppt/theme/theme\d+\.xml$": (
        "application/vnd.openxmlformats-officedocument.theme+xml",
    ),
    r"^ppt/comments/.*\.xml$": (
        "application/vnd.openxmlformats-officedocument.presentationml.comments+xml",
    ),
    r"^ppt/threadedComments/.*\.xml$": (
        "application/vnd.ms-powerpoint.threadedcomments+xml",
    ),
    r"^ppt/charts/chart\d+\.xml$": (
        "application/vnd.openxmlformats-officedocument.drawingml.chart+xml",
    ),
    r"^docProps/core\.xml$": (
        "application/vnd.openxmlformats-package.core-properties+xml",
    ),
    r"^docProps/app\.xml$": (
        "application/vnd.openxmlformats-officedocument.extended-properties+xml",
    ),
}

# --------------------------------------------------------------------------
# ECMA-376 child sequences
# --------------------------------------------------------------------------
#
# OOXML complex types are ``xsd:sequence``, so a consumer is entitled to reject
# a document whose children are in a different order — and PowerPoint often
# does.  Each entry below is the sequence from ECMA-376 Part 1 for one element,
# expressed as a list of *groups*: any name inside a group may take that slot,
# because the schema offers a choice there.  Names not listed are ignored by
# ``assert_children_in_order``, which only checks the relative order of the
# names it knows.

CHILD_ORDER = {
    # CT_TextCharacterProperties (ECMA-376 Part 1, 20.1.2.3.9 / a:rPr, a:defRPr)
    "a:rPr": [
        ["a:ln"],
        ["a:noFill", "a:solidFill", "a:gradFill", "a:blipFill", "a:pattFill", "a:grpFill"],
        ["a:effectLst", "a:effectDag"],
        ["a:highlight"],
        ["a:uLnTx", "a:uLn"],
        ["a:uFillTx", "a:uFill"],
        ["a:latin"],
        ["a:ea"],
        ["a:cs"],
        ["a:sym"],
        ["a:hlinkClick"],
        ["a:hlinkMouseOver"],
        ["a:rtl"],
        ["a:extLst"],
    ],
    # CT_ShapeProperties (20.1.2.2.35 / p:spPr)
    "p:spPr": [
        ["a:xfrm"],
        ["a:custGeom", "a:prstGeom"],
        ["a:noFill", "a:solidFill", "a:gradFill", "a:blipFill", "a:pattFill", "a:grpFill"],
        ["a:ln"],
        ["a:effectLst", "a:effectDag"],
        ["a:scene3d"],
        ["a:sp3d"],
        ["a:extLst"],
    ],
    # CT_EffectList (20.1.8.26 / a:effectLst)
    "a:effectLst": [
        ["a:blur"],
        ["a:fillOverlay"],
        ["a:glow"],
        ["a:innerShdw"],
        ["a:outerShdw"],
        ["a:prstShdw"],
        ["a:reflection"],
        ["a:softEdge"],
    ],
    # CT_Scene3D (20.1.4.1.26 / a:scene3d)
    "a:scene3d": [["a:camera"], ["a:lightRig"], ["a:backdrop"], ["a:extLst"]],
    # CT_Slide (19.3.1.38 / p:sld)
    "p:sld": [["p:cSld"], ["p:clrMapOvr"], ["p:transition"], ["p:timing"], ["p:extLst"]],
    # CT_RegularTextRun (21.1.2.3.8 / a:r)
    "a:r": [["a:rPr"], ["a:t"]],
    # CT_TextParagraph (21.1.2.2.6 / a:p)
    "a:p": [["a:pPr"], ["a:r", "a:br", "a:fld"], ["a:endParaRPr"]],
    # CT_LineProperties (20.1.2.2.24 / a:ln)
    "a:ln": [
        ["a:noFill", "a:solidFill", "a:gradFill", "a:pattFill"],
        ["a:prstDash", "a:custDash"],
        ["a:round", "a:bevel", "a:miter"],
        ["a:headEnd"],
        ["a:tailEnd"],
        ["a:extLst"],
    ],
}


def qname(prefixed: str) -> str:
    """``"a:rPr"`` -> ``"{http://...drawingml/2006/main}rPr"``."""
    prefix, _, local = prefixed.partition(":")
    if not local:
        return prefixed
    return "{%s}%s" % (NS[prefix], local)


def local_name(element_or_tag) -> str:
    """Return an element's tag as ``prefix:local`` using the table in :data:`NS`."""
    tag = getattr(element_or_tag, "tag", element_or_tag)
    if not isinstance(tag, str):  # comments, processing instructions
        return ""
    if not tag.startswith("{"):
        return tag
    uri, _, local = tag[1:].partition("}")
    for prefix, known in NS.items():
        if known == uri:
            return "%s:%s" % (prefix, local)
    return "{%s}%s" % (uri, local)


def child_names(element) -> list[str]:
    """The element's children as ``prefix:local`` names, in document order."""
    return [n for n in (local_name(c) for c in element) if n]


def assert_children_in_order(element, order: Optional[list[list[str]]] = None) -> None:
    """Assert the element's children follow their ECMA-376 sequence.

    ``order`` defaults to the entry in :data:`CHILD_ORDER` for the element's own
    name.  Children whose names are not mentioned in the sequence are ignored,
    so a partially specified sequence still catches inversions between the names
    it does list.
    """
    name = local_name(element)
    if order is None:
        assert name in CHILD_ORDER, (
            "no ECMA-376 child sequence recorded for <%s>; add one to "
            "harness.CHILD_ORDER before asserting on it" % name
        )
        order = CHILD_ORDER[name]

    rank = {}
    for index, group in enumerate(order):
        for member in group:
            rank[member] = index

    seen: list[tuple[str, int]] = []
    for child in child_names(element):
        if child in rank:
            seen.append((child, rank[child]))

    ranks = [r for _, r in seen]
    if ranks != sorted(ranks):
        expected = " -> ".join("|".join(group) for group in order)
        raise AssertionError(
            "children of <%s> are out of ECMA-376 sequence.\n"
            "  found:    %s\n"
            "  expected: %s" % (name, " -> ".join(child_names(element)), expected)
        )


# --------------------------------------------------------------------------
# The import-shadowing guard
# --------------------------------------------------------------------------

_SHADOW_MESSAGE = """\
The `aspose` namespace is shadowed: `aspose.slides_foss` cannot be imported
because another distribution owns `aspose/__init__.py` at

    {origin}

That package makes `aspose` a regular package and sets `aspose.__path__ = []`,
which hides every other `aspose.*` namespace portion, including this library.
The two cannot share an interpreter.

Run the tests in a virtual environment that does not have the other
distribution installed:

    python -m venv .venv
    .venv/Scripts/pip install -e ".[test]"     # POSIX: .venv/bin/pip
    .venv/Scripts/python -m pytest

Refusing to continue: without this check the suite would silently test
whatever else answers to the name `aspose`.
"""


def verify_library_not_shadowed() -> None:
    """Fail loudly, with a diagnosis, if `aspose.slides_foss` is unimportable.

    Import order alone decides this and the losing side gets a bare
    ``ModuleNotFoundError``, which reads like a broken checkout rather than
    like a package collision.  Turn it into a sentence that says what happened.
    """
    import importlib

    try:
        importlib.import_module("aspose.slides_foss")
        return
    except ImportError as exc:
        origin = "<not found>"
        try:
            aspose = importlib.import_module("aspose")
            origin = getattr(aspose, "__file__", None) or "<namespace package>"
        except ImportError:
            pass
        raise RuntimeError(_SHADOW_MESSAGE.format(origin=origin)) from exc


# --------------------------------------------------------------------------
# The produced package
# --------------------------------------------------------------------------

_R_ATTRS = ("id", "embed", "link", "pict", "dm", "lo", "qs", "cs")


class ProducedPackage:
    """A ``.pptx`` that has been written, opened for inspection as bytes.

    Nothing in here calls back into the library that produced the file.
    """

    def __init__(self, path: str):
        self.path = str(path)
        with open(self.path, "rb") as handle:
            self.blob = handle.read()
        self._zip = zipfile.ZipFile(self.path)
        self.namelist = self._zip.namelist()

    def close(self) -> None:
        """Release the open archive.

        Windows will not remove a directory that still has an open handle in
        it, so a package left open outlives the test and breaks ``tmp_path``
        teardown rather than the test itself.
        """
        self._zip.close()

    def __enter__(self) -> "ProducedPackage":
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()

    # -- raw access -------------------------------------------------------

    def __contains__(self, part: str) -> bool:
        return part in self.namelist

    def read(self, part: str) -> bytes:
        assert part in self.namelist, (
            "part %r is not in the package; it has %d parts:\n  %s"
            % (part, len(self.namelist), "\n  ".join(sorted(self.namelist)))
        )
        return self._zip.read(part)

    def text(self, part: str) -> str:
        return self.read(part).decode("utf-8")

    def xml(self, part: str):
        """Parse a part and return its root element."""
        return ET.fromstring(self.read(part))

    def parts_matching(self, pattern: str) -> list[str]:
        rx = re.compile(pattern)
        return sorted(n for n in self.namelist if rx.match(n))

    # -- XPath ------------------------------------------------------------

    def findall(self, part: str, xpath: str) -> list:
        return self.xml(part).xpath(xpath, namespaces=NS)

    def find_one(self, part: str, xpath: str):
        """Return the single element matching ``xpath``, asserting there is one."""
        hits = self.findall(part, xpath)
        assert len(hits) == 1, (
            "expected exactly one match for %r in %s, found %d\n%s"
            % (xpath, part, len(hits), self.text(part))
        )
        return hits[0]

    def assert_element(
        self,
        part: str,
        xpath: str,
        attrs: Optional[dict] = None,
        child_order: Optional[list] = None,
        children: Optional[Iterable[str]] = None,
    ):
        """Assert an XPath-addressed element exists, and check it.

        ``attrs``
            Attribute name (``"prst"`` or ``"r:embed"``) to expected value.  A
            value of :data:`Ellipsis` asserts only that the attribute is
            present.
        ``children``
            Names that must appear among the element's children.
        ``child_order``
            Sequence to check with :func:`assert_children_in_order`; pass
            ``True`` to use the table entry for the element's own name.
        """
        element = self.find_one(part, xpath)

        for name, expected in (attrs or {}).items():
            key = qname(name) if ":" in name else name
            assert key in element.attrib, (
                "<%s> in %s has no @%s; it has %r"
                % (local_name(element), part, name, dict(element.attrib))
            )
            if expected is not Ellipsis:
                actual = element.get(key)
                assert actual == expected, (
                    "<%s>/@%s in %s is %r, expected %r"
                    % (local_name(element), name, part, actual, expected)
                )

        for required in children or ():
            assert required in child_names(element), (
                "<%s> in %s has no <%s> child; it has %r"
                % (local_name(element), part, required, child_names(element))
            )

        if child_order is not None:
            assert_children_in_order(
                element, None if child_order is True else child_order
            )
        return element

    # -- relationships ----------------------------------------------------

    @staticmethod
    def rels_part_for(part: str) -> str:
        directory, _, filename = part.rpartition("/")
        return posixpath.join(directory, "_rels", filename + ".rels")

    def relationships(self, part: str) -> dict:
        """Return ``{Id: {"type", "target", "mode"}}`` for one part's ``.rels``."""
        rels_part = self.rels_part_for(part)
        if rels_part not in self.namelist:
            return {}
        root = ET.fromstring(self.read(rels_part))
        out = {}
        for rel in root.xpath("/pr:Relationships/pr:Relationship", namespaces=NS):
            out[rel.get("Id")] = {
                "type": rel.get("Type"),
                "target": rel.get("Target"),
                "mode": rel.get("TargetMode"),
            }
        return out

    def relationship(self, part: str, rel_id: str) -> dict:
        rels = self.relationships(part)
        assert rel_id in rels, (
            "relationship %r is referenced from %s but %s declares only %r"
            % (rel_id, part, self.rels_part_for(part), sorted(rels))
        )
        return rels[rel_id]

    def _referenced_rel_ids(self, part: str) -> Iterator[tuple[str, str, str]]:
        """Yield ``(element name, attribute, id)`` for every relationship reference."""
        for element in self.xml(part).iter():
            if not isinstance(element.tag, str):
                continue
            for attribute, value in element.attrib.items():
                if attribute.startswith("{%s}" % R_NS):
                    local = attribute.split("}", 1)[1]
                    if local in _R_ATTRS and value:
                        yield local_name(element), "r:" + local, value

    def assert_relationship_ids_resolve(self) -> None:
        """Every ``r:id``/``r:embed``/``r:link`` resolves in its own part's ``.rels``.

        A dangling reference is the single most common way these packages break:
        the image bytes are present, the element that points at them is present,
        and the relationship that joins them is not.
        """
        failures = []
        for part in self.namelist:
            if not part.endswith(".xml") or "/_rels/" in part or part.startswith("_rels/"):
                continue
            declared = self.relationships(part)
            for element, attribute, rel_id in self._referenced_rel_ids(part):
                if rel_id not in declared:
                    failures.append(
                        "  %s: <%s %s=%r> does not resolve; %s declares %r"
                        % (part, element, attribute, rel_id,
                           self.rels_part_for(part), sorted(declared))
                    )
        assert not failures, "dangling relationship references:\n" + "\n".join(failures)

    @classmethod
    def _resolve_target(cls, rels_part: str, target: str) -> str:
        """Absolute part name for a relationship target declared in ``rels_part``."""
        if target.startswith("/"):
            return target.lstrip("/")
        owner_dir = posixpath.dirname(posixpath.dirname(rels_part))
        return posixpath.normpath(posixpath.join(owner_dir, target))

    def _internal_targets(self, rels_part: str) -> Iterator[str]:
        root = ET.fromstring(self.read(rels_part))
        for rel in root.xpath("/pr:Relationships/pr:Relationship", namespaces=NS):
            if rel.get("TargetMode") == "External":
                continue
            yield self._resolve_target(rels_part, rel.get("Target") or "")

    def assert_every_part_is_reachable(self) -> None:
        """Every part is reachable by walking relationships from ``_rels/.rels``.

        ISO/IEC 29500-2 §9.3 makes the relationship graph the only way into a
        package: a consumer starts at the package relationships and follows
        them part by part.  A part nothing points at is therefore not in the
        document at all — but it is still in the ZIP, still shipped, and still
        readable by anyone who opens the file with a zip tool.

        This is the rule that catches an orphan, which the other three cannot:
        an orphaned part with its own ``Override`` breaks no reference and
        resolves its content type perfectly well.
        """
        reached = {"[Content_Types].xml"}
        pending = ["_rels/.rels"]
        while pending:
            rels_part = pending.pop()
            if rels_part in reached or rels_part not in self.namelist:
                continue
            reached.add(rels_part)
            for target in self._internal_targets(rels_part):
                if target in reached:
                    continue
                reached.add(target)
                pending.append(self.rels_part_for(target))

        unreachable = sorted(set(self.namelist) - reached)
        assert not unreachable, (
            "parts no relationship names, so no consumer can reach them "
            "although they ship in the file:\n  %s" % "\n  ".join(unreachable)
        )

    def assert_relationship_targets_exist(self) -> None:
        """Every internal relationship names a part that is in the package."""
        failures = []
        for part in self.namelist:
            if not part.endswith(".rels"):
                continue
            owner_dir = posixpath.dirname(posixpath.dirname(part))
            root = ET.fromstring(self.read(part))
            for rel in root.xpath("/pr:Relationships/pr:Relationship", namespaces=NS):
                if rel.get("TargetMode") == "External":
                    continue
                target = rel.get("Target")
                if target.startswith("/"):
                    resolved = target.lstrip("/")
                else:
                    resolved = posixpath.normpath(posixpath.join(owner_dir, target))
                if resolved not in self.namelist:
                    failures.append(
                        "  %s: %s -> %r resolves to %r, which is not in the package"
                        % (part, rel.get("Id"), target, resolved)
                    )
        assert not failures, "relationships pointing at missing parts:\n" + "\n".join(failures)

    # -- content types ----------------------------------------------------

    def content_types(self) -> tuple[dict, dict]:
        """Return ``({extension: type}, {"/part/name": type})``."""
        root = ET.fromstring(self.read("[Content_Types].xml"))
        defaults = {
            d.get("Extension").lower(): d.get("ContentType")
            for d in root.xpath("/ct:Types/ct:Default", namespaces=NS)
        }
        overrides = {
            o.get("PartName"): o.get("ContentType")
            for o in root.xpath("/ct:Types/ct:Override", namespaces=NS)
        }
        return defaults, overrides

    def content_type_of(self, part: str) -> Optional[str]:
        """The content type a consumer resolves for ``part``, or ``None``."""
        defaults, overrides = self.content_types()
        if "/" + part in overrides:
            return overrides["/" + part]
        _, _, extension = part.rpartition(".")
        return defaults.get(extension.lower())

    def assert_content_types_resolve(self) -> None:
        """Every part resolves a content type, and every ``Override`` names a real part.

        ISO/IEC 29500-2 §10.1.2 makes the content type the part's *identity*: a
        slide part that falls through to ``<Default Extension="xml"/>`` is an
        ``application/xml`` part, and a strict consumer will not treat it as a
        slide.  PowerPoint is lenient here; the Open XML SDK and python-pptx are
        not, which is the worst place for a user to find out.
        """
        defaults, overrides = self.content_types()

        missing = [
            part for part in self.namelist
            if part != "[Content_Types].xml" and self.content_type_of(part) is None
        ]
        assert not missing, (
            "parts with no content type (no Override and no matching Default):\n  %s\n"
            "declared Defaults: %r" % ("\n  ".join(sorted(missing)), sorted(defaults))
        )

        dangling = [
            name for name in overrides if name.lstrip("/") not in self.namelist
        ]
        assert not dangling, (
            "Override entries naming parts that are not in the package:\n  %s"
            % "\n  ".join(sorted(dangling))
        )

        wrong = []
        for part in self.namelist:
            actual = self.content_type_of(part)
            for pattern, allowed in EXPECTED_CONTENT_TYPES.items():
                if re.match(pattern, part) and actual not in allowed:
                    wrong.append(
                        "  %s resolves %r; ECMA-376 requires one of %r"
                        % (part, actual, list(allowed))
                    )
        assert not wrong, "parts with the wrong content type:\n" + "\n".join(wrong)

    def assert_package_is_consistent(self) -> None:
        """All four package-level rules at once."""
        self.assert_relationship_ids_resolve()
        self.assert_relationship_targets_exist()
        self.assert_content_types_resolve()
        self.assert_every_part_is_reachable()

    # -- third-party read-back -------------------------------------------

    def open_with_python_pptx(self):
        """Open the file with ``python-pptx`` and return its ``Presentation``.

        An independent reader with its own idea of what a valid package is.  It
        is deliberately *not* the library under test: when it and PowerPoint
        agree that a feature is missing, the library's own read-back saying
        otherwise is the defect.
        """
        import pptx

        return pptx.Presentation(self.path)


def load(path) -> ProducedPackage:
    return ProducedPackage(path)
