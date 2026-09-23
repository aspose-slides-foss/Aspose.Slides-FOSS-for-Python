"""Every transition must be written the way PowerPoint writes it.

Three things went wrong here, all invisible to a test that reads the type back
through this library:

* **Elements that do not exist.**  `TransitionType.ORBIT` and `ROTATE` were
  written as `<p14:orbit>` and `<p14:rotate>`.  The PowerPoint 2010 namespace
  defines no such elements: PowerPoint writes all four of Cube, Rotate, Box and
  Orbit as `<p14:prism>`, told apart by `@isContent` and `@isInverted`, and it
  showed no transition at all for the file this library wrote.  `BOX` was
  written with `@isContent`, which is PowerPoint's Rotate.
* **No fallback.**  A transition outside the ECMA-376 namespace (`p14`, `p15`,
  `p159`) is an extension.  PowerPoint writes it inside
  `<mc:AlternateContent>`: the extension in an `<mc:Choice>` that names its
  namespace in `@Requires`, and a plain `<p:fade/>` in `<mc:Fallback>` for a
  reader that does not know it.  Written bare, `<p159:morph>` is rejected by
  the Open XML SDK outright.
* **A second transition.**  A slide opened from a file PowerPoint wrote keeps
  its transition inside `<mc:AlternateContent>`.  Setting a type did not see
  it and added a second `<p:transition>` beside it, which `CT_Slide` does not
  allow (it has one optional transition).

The attribute values asserted below are what PowerPoint itself writes for each
transition, read from files PowerPoint saved.
"""

from __future__ import annotations

import os
import zipfile

import pytest

from aspose.slides_foss import Presentation, ShapeType
from aspose.slides_foss.animation import EffectSubtype, EffectTriggerType, EffectType
from aspose.slides_foss.export import SaveFormat
from aspose.slides_foss.slideshow import TransitionSpeed, TransitionType

from .harness import NS, assert_children_in_order, child_names, local_name, qname

SLIDE = "ppt/slides/slide1.xml"

#: The transition elements the PowerPoint 2010 namespace defines for
#: `p:transition` (MS-PPTX).  Anything else in that namespace is not a
#: transition, and PowerPoint discards it.
P14_TRANSITIONS = {
    "vortex", "switch", "flip", "ripple", "honeycomb", "prism", "doors",
    "window", "ferris", "gallery", "conveyor", "pan", "glitter", "warp",
    "flythrough", "flash", "shred", "reveal", "wheelReverse",
}

#: What PowerPoint writes for each of the four prism transitions.
PRISM = {
    TransitionType.CUBE: {},
    TransitionType.ROTATE: {"isContent": "1"},
    TransitionType.BOX: {"isInverted": "1"},
    TransitionType.ORBIT: {"isContent": "1", "isInverted": "1"},
}

#: A fade exactly as PowerPoint saves it.
POWERPOINT_FADE = (
    '<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
    '<mc:Choice xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" Requires="p14">'
    '<p:transition spd="slow" p14:dur="2000"><p:fade thruBlk="1"/></p:transition>'
    '</mc:Choice>'
    '<mc:Fallback><p:transition spd="slow"><p:fade thruBlk="1"/></p:transition></mc:Fallback>'
    '</mc:AlternateContent>'
)

#: A wipe as this library writes it: a bare `p:transition`.
BARE_WIPE = '<p:transition><p:wipe/></p:transition>'


def _transitions(slide):
    """``(container, transition)`` for every transition the slide carries.

    A transition is either a direct child of `p:sld` or wrapped in an
    `mc:AlternateContent` that is.
    """
    found = []
    for child in slide:
        if child.tag == qname("p:transition"):
            found.append((child, child))
        elif child.tag == qname("mc:AlternateContent"):
            inner = child.find("mc:Choice/p:transition", NS)
            if inner is not None:
                found.append((child, inner))
    return found


def _the_transition(pkg):
    slide = pkg.xml(SLIDE)
    found = _transitions(slide)
    assert len(found) == 1, (
        "CT_Slide allows one transition; the slide carries %d: %r"
        % (len(found), [local_name(container) for container, _ in found])
    )
    return slide, found[0]


def _effect(transition):
    effects = [c for c in transition if isinstance(c.tag, str)]
    assert effects, "<p:transition> has no effect element"
    return effects[0]


def _assert_slide_order(slide):
    """`CT_Slide` order, reading a wrapped transition as the transition it wraps."""
    names = []
    for child in slide:
        name = local_name(child)
        if name == "mc:AlternateContent" and child.find("mc:Choice/p:transition", NS) is not None:
            name = "p:transition"
        names.append(name)
    shadow = slide.makeelement(slide.tag)
    for name in names:
        if name.startswith("{"):
            continue
        shadow.append(shadow.makeelement(qname(name)))
    assert_children_in_order(shadow)


def _assert_written_as_powerpoint_writes_it(slide, container, transition):
    """The markup rules PowerPoint follows, for any transition type."""
    effect = _effect(transition)
    namespace = effect.tag[1:].partition("}")[0]

    if namespace == NS["p"]:
        return

    if namespace == NS["p14"]:
        local = effect.tag.partition("}")[2]
        assert local in P14_TRANSITIONS, (
            "<p14:%s> is not a transition the PowerPoint 2010 namespace defines; "
            "PowerPoint discards it and shows no transition" % local
        )
    assert container.tag == qname("mc:AlternateContent"), (
        "<%s> is outside the ECMA-376 namespace and was written bare in "
        "<p:transition>; PowerPoint writes it in mc:AlternateContent with a "
        "fallback" % local_name(effect)
    )
    choice = transition.getparent()
    prefixes = [p for p, uri in choice.nsmap.items() if uri == namespace]
    requires = (choice.get("Requires") or "").split()
    assert prefixes and set(prefixes) & set(requires), (
        "mc:Choice/@Requires is %r, which does not name the namespace of <%s>"
        % (choice.get("Requires"), local_name(effect))
    )
    fallback = container.find("mc:Fallback/p:transition", NS)
    assert fallback is not None, "mc:AlternateContent has no mc:Fallback transition"
    fallback_effect = _effect(fallback)
    assert fallback_effect.tag.startswith("{%s}" % NS["p"]), (
        "the fallback carries <%s>; it must be an ECMA-376 transition a reader "
        "without the extension understands" % local_name(fallback_effect)
    )
    _assert_slide_order(slide)


@pytest.mark.parametrize("transition_type", list(PRISM), ids=lambda t: t.name)
def test_the_prism_transitions_are_written_as_powerpoint_writes_them(
    produced, transition_type
):
    """Cube, Rotate, Box and Orbit are one `p14:prism` with two flags."""
    pres = Presentation()
    pres.slides[0].slide_show_transition.type = transition_type
    pkg = produced(pres)

    slide, (container, transition) = _the_transition(pkg)
    prism = _effect(transition)
    assert local_name(prism) == "p14:prism", (
        "%s must be written as <p14:prism>; found <%s>"
        % (transition_type.name, local_name(prism))
    )
    flags = {k: v for k, v in prism.attrib.items() if k in ("isContent", "isInverted")}
    assert flags == PRISM[transition_type], (
        "%s: PowerPoint writes <p14:prism> with %r; found %r"
        % (transition_type.name, PRISM[transition_type], flags)
    )
    _assert_written_as_powerpoint_writes_it(slide, container, transition)


def test_morph_is_wrapped_as_powerpoint_wraps_it(produced):
    """`p159:morph` goes in an `mc:Choice` requiring `p159`, with a fade fallback."""
    pres = Presentation()
    pres.slides[0].slide_show_transition.type = TransitionType.MORPH
    pkg = produced(pres)

    slide, (container, transition) = _the_transition(pkg)
    _assert_written_as_powerpoint_writes_it(slide, container, transition)
    morph = _effect(transition)
    assert local_name(morph) == "p159:morph"
    assert morph.get("option") == "byObject"
    assert transition.getparent().get("Requires") == "p159"
    assert child_names(container.find("mc:Fallback/p:transition", NS)) == ["p:fade"]


@pytest.mark.parametrize(
    "transition_type",
    [t for t in TransitionType if t is not TransitionType.NONE],
    ids=lambda t: t.name,
)
def test_every_transition_type_is_written_as_powerpoint_writes_it(produced, transition_type):
    """One transition, a real element, wrapped when it is an extension."""
    pres = Presentation()
    pres.slides[0].slide_show_transition.type = transition_type
    pkg = produced(pres)

    slide, (container, transition) = _the_transition(pkg)
    _assert_written_as_powerpoint_writes_it(slide, container, transition)
    _assert_slide_order(slide)


def test_a_wrapped_transition_goes_before_the_animation_timing(produced):
    """The wrapper takes the transition's place in `CT_Slide`: before `p:timing`."""
    pres = Presentation()
    slide = pres.slides[0]
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50.0, 50.0, 200.0, 100.0)
    slide.timeline.main_sequence.add_effect(
        shape, EffectType.FADE, EffectSubtype.NONE, EffectTriggerType.ON_CLICK
    )
    slide.slide_show_transition.type = TransitionType.VORTEX
    pkg = produced(pres)

    root = pkg.xml(SLIDE)
    assert child_names(root)[-2:] == ["mc:AlternateContent", "p:timing"], child_names(root)
    _assert_slide_order(root)


@pytest.mark.parametrize("set_speed_first", [False, True], ids=["type-first", "speed-first"])
def test_a_wrapped_transition_carries_its_speed_in_both_branches(produced, set_speed_first):
    """A reader that takes the fallback must see the same speed PowerPoint does."""
    pres = Presentation()
    transition = pres.slides[0].slide_show_transition
    if set_speed_first:
        transition.speed = TransitionSpeed.SLOW
        transition.type = TransitionType.ORBIT
    else:
        transition.type = TransitionType.ORBIT
        transition.speed = TransitionSpeed.SLOW
    pkg = produced(pres)

    _, (container, choice_transition) = _the_transition(pkg)
    fallback = container.find("mc:Fallback/p:transition", NS)
    assert choice_transition.get("spd") == "slow"
    assert fallback is not None and fallback.get("spd") == "slow", (
        "the fallback transition does not carry the speed: %r"
        % (dict(fallback.attrib) if fallback is not None else None)
    )


def _deck_with_existing_transition(directory, markup):
    """A saved deck whose first slide already carries ``markup`` as its transition."""
    source = os.path.join(directory, "source.pptx")
    pres = Presentation()
    pres.save(source, SaveFormat.PPTX)
    pres.dispose()

    edited = os.path.join(directory, "with-transition.pptx")
    with zipfile.ZipFile(source) as src, zipfile.ZipFile(edited, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == SLIDE:
                text = data.decode("utf-8")
                assert text.count("</p:clrMapOvr>") == 1, "fixture: no colour map override"
                text = text.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + markup)
                data = text.encode("utf-8")
            dst.writestr(item, data)
    return edited


@pytest.mark.parametrize(
    "existing", [POWERPOINT_FADE, BARE_WIPE], ids=["powerpoint-fade", "bare-wipe"]
)
@pytest.mark.parametrize(
    "new_type",
    [TransitionType.PUSH, TransitionType.VORTEX, TransitionType.MORPH],
    ids=lambda t: t.name,
)
def test_setting_a_transition_on_an_opened_deck_replaces_the_one_it_had(
    produced, tmp_path, existing, new_type
):
    """The slide ends with one transition, the new one, not two."""
    path = _deck_with_existing_transition(str(tmp_path), existing)
    pres = Presentation(path)
    pres.slides[0].slide_show_transition.type = new_type
    pkg = produced(pres, name="edited.pptx")

    slide, (container, transition) = _the_transition(pkg)
    _assert_written_as_powerpoint_writes_it(slide, container, transition)
    _assert_slide_order(slide)
    effect = _effect(transition)
    expected = {
        TransitionType.PUSH: "p:push",
        TransitionType.VORTEX: "p14:vortex",
        TransitionType.MORPH: "p159:morph",
    }[new_type]
    assert local_name(effect) == expected, (
        "the slide's transition is <%s>, not the <%s> just set"
        % (local_name(effect), expected)
    )


def test_an_opened_deck_keeps_its_transition_speed_when_the_type_changes(produced, tmp_path):
    """Replacing the effect is not a licence to drop the transition's attributes."""
    path = _deck_with_existing_transition(str(tmp_path), POWERPOINT_FADE)
    pres = Presentation(path)
    pres.slides[0].slide_show_transition.type = TransitionType.VORTEX
    pkg = produced(pres, name="edited.pptx")

    _, (container, transition) = _the_transition(pkg)
    fallback = container.find("mc:Fallback/p:transition", NS)
    assert transition.get("spd") == "slow", dict(transition.attrib)
    assert transition.get(qname("p14:dur")) == "2000", dict(transition.attrib)
    assert fallback is not None and fallback.get("spd") == "slow"
    assert fallback.get(qname("p14:dur")) is None, (
        "the fallback is for a reader without the p14 namespace; it must not "
        "carry a p14 attribute"
    )
