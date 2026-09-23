from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import lxml.etree as ET
from ..ISlideShowTransition import ISlideShowTransition

if TYPE_CHECKING:
    from .ITransitionValueBase import ITransitionValueBase
    from .TransitionSpeed import TransitionSpeed
    from .TransitionType import TransitionType


class SlideShowTransition(ISlideShowTransition):
    """Represents slide show transition."""

    def __init__(self):
        self._slide_part = None
        self._transition_elem: Optional[ET._Element] = None
        self._fallback_elem: Optional[ET._Element] = None
        self._value_obj = None
        self._type_cache = None

    def _init_internal(self, slide_part):
        """Initialize with the slide part. Reads existing <p:transition> if present.

        PowerPoint saves a transition inside mc:AlternateContent, with the
        transition it means in mc:Choice and a plain one in mc:Fallback, so the
        transition is looked for there as well as directly under the slide.
        """
        from .._internal.pptx.constants import Elements
        from .._internal.pptx.transition_mappings import MC_PREFIX
        self._slide_part = slide_part
        root = slide_part._root
        self._transition_elem = root.find(Elements.P_TRANSITION)
        if self._transition_elem is None:
            for wrapper in root.findall(f'{MC_PREFIX}AlternateContent'):
                chosen = wrapper.find(f'{MC_PREFIX}Choice/{Elements.P_TRANSITION}')
                if chosen is not None:
                    self._transition_elem = chosen
                    self._fallback_elem = wrapper.find(
                        f'{MC_PREFIX}Fallback/{Elements.P_TRANSITION}'
                    )
                    break
        if self._transition_elem is not None:
            self._parse_value()

    def _ensure_transition_elem(self) -> ET._Element:
        """Get or create the <p:transition> element on the slide.

        CT_Slide is the sequence cSld, clrMapOvr?, transition?, timing?,
        extLst?, so the transition goes after the colour map override when the
        slide has one and after cSld when it does not.
        """
        if self._transition_elem is not None:
            return self._transition_elem
        from .._internal.pptx.constants import Elements
        from .._internal.pptx.child_order import insert_in_order
        self._transition_elem = insert_in_order(
            self._slide_part._root, ET.Element(Elements.P_TRANSITION)
        )
        return self._transition_elem

    @staticmethod
    def _container(elem: ET._Element) -> ET._Element:
        """The slide's child that holds ``elem``: itself, or its mc:AlternateContent."""
        from .._internal.pptx.transition_mappings import MC_PREFIX
        parent = elem.getparent()
        if parent is not None and parent.tag == f'{MC_PREFIX}Choice':
            return parent.getparent()
        return elem

    def _place(self, extension_ns: Optional[str]) -> None:
        """Put the transition on the slide bare, or wrapped the way PowerPoint wraps it.

        ``extension_ns`` is the namespace of a transition element that is not
        in ECMA-376 (p14, p15, p159), or None.  PowerPoint writes such an
        element in an mc:Choice that requires its namespace, with a fade in
        mc:Fallback for a reader that does not know it.  The result takes the
        place of whatever held the transition before, so the slide never
        carries two.
        """
        from .._internal.pptx.constants import Elements
        from .._internal.pptx.transition_mappings import (
            EXTENSION_PREFIXES, MC_NS, MC_PREFIX, P_PREFIX,
        )
        elem = self._ensure_transition_elem()
        container = self._container(elem)
        slide = container.getparent()
        choice = None
        if extension_ns is None:
            replacement = elem
            self._fallback_elem = None
        else:
            prefix = EXTENSION_PREFIXES[extension_ns]
            replacement = ET.Element(f'{MC_PREFIX}AlternateContent', nsmap={'mc': MC_NS})
            choice = ET.SubElement(
                replacement, f'{MC_PREFIX}Choice', nsmap={prefix: extension_ns}
            )
            choice.set('Requires', prefix)
            fallback = ET.SubElement(
                ET.SubElement(replacement, f'{MC_PREFIX}Fallback'), Elements.P_TRANSITION
            )
            # The fallback is for a reader without the extension, so it gets
            # the ECMA-376 attributes only, as PowerPoint writes it.
            for name, value in elem.attrib.items():
                if not name.startswith('{'):
                    fallback.set(name, value)
            ET.SubElement(fallback, f'{P_PREFIX}fade')
            self._fallback_elem = fallback
        if container is not elem:
            elem.getparent().remove(elem)
        if replacement is not container:
            slide.replace(container, replacement)
        if choice is not None:
            choice.append(elem)

    def _set_attribute(self, name: str, value: Optional[str]) -> None:
        """Set a transition attribute, or remove it for None, in the fallback too."""
        elem = self._ensure_transition_elem()
        for target in (elem, self._fallback_elem):
            if target is None:
                continue
            if value is None:
                target.attrib.pop(name, None)
            else:
                target.set(name, value)

    def _parse_value(self):
        """Parse the transition child element to determine type and value object."""
        from .._internal.pptx.transition_mappings import get_transition_type_from_element
        from .TransitionType import TransitionType as TT

        if self._transition_elem is None or len(self._transition_elem) == 0:
            self._type_cache = TT.NONE
            self._value_obj = None
            return

        # Find the first child element (the transition type element)
        child = None
        for ch in self._transition_elem:
            if isinstance(ch.tag, str):  # skip comments
                child = ch
                break

        if child is None:
            self._type_cache = TT.NONE
            self._value_obj = None
            return

        type_str = get_transition_type_from_element(child)
        if type_str is None:
            self._type_cache = TT.NONE
            self._value_obj = None
            return

        self._type_cache = TT(type_str)
        self._value_obj = self._create_value_obj(type_str, child)

    def _create_value_obj(self, type_str: str, element):
        """Create the appropriate transition value object for the given type."""
        from .._internal.pptx.transition_mappings import get_transition_info
        info = get_transition_info(type_str)
        if info is None:
            return None

        _, cls_name, _ = info
        cls = self._get_value_class(cls_name)
        obj = cls()
        obj._init_internal(element, self._slide_part)
        return obj

    @staticmethod
    def _get_value_class(cls_name: str):
        """Import and return the transition value class by name."""
        from . import (
            EmptyTransition, OptionalBlackTransition, SideDirectionTransition,
            EightDirectionTransition, CornerDirectionTransition, OrientationTransition,
            InOutTransition, SplitTransition, WheelTransition, MorphTransition,
            GlitterTransition, FlyThroughTransition, ShredTransition,
            RevealTransition, RippleTransition, LeftRightDirectionTransition,
        )
        classes = {
            'EmptyTransition': EmptyTransition,
            'OptionalBlackTransition': OptionalBlackTransition,
            'SideDirectionTransition': SideDirectionTransition,
            'EightDirectionTransition': EightDirectionTransition,
            'CornerDirectionTransition': CornerDirectionTransition,
            'OrientationTransition': OrientationTransition,
            'InOutTransition': InOutTransition,
            'SplitTransition': SplitTransition,
            'WheelTransition': WheelTransition,
            'MorphTransition': MorphTransition,
            'GlitterTransition': GlitterTransition,
            'FlyThroughTransition': FlyThroughTransition,
            'ShredTransition': ShredTransition,
            'RevealTransition': RevealTransition,
            'RippleTransition': RippleTransition,
            'LeftRightDirectionTransition': LeftRightDirectionTransition,
        }
        return classes[cls_name]

    # ----- Properties -----

    @property
    def advance_on_click(self) -> bool:
        """Specifies whether a mouse click will advance the slide or not. If this attribute is not specified then a value of true is assumed. Read/write ."""
        if self._transition_elem is not None:
            return self._transition_elem.get('advClick', '1') != '0'
        return True

    @advance_on_click.setter
    def advance_on_click(self, value: bool):
        self._set_attribute('advClick', '1' if value else '0')

    @property
    def advance_after(self) -> bool:
        """This attribute specifies if the slideshow will move to the next slide after a certain time. Read/write ."""
        if self._transition_elem is not None:
            return 'advTm' in self._transition_elem.attrib
        return False

    @advance_after.setter
    def advance_after(self, value: bool):
        elem = self._ensure_transition_elem()
        if value:
            # If no advTm set yet, default to 0
            if 'advTm' not in elem.attrib:
                self._set_attribute('advTm', '0')
        else:
            self._set_attribute('advTm', None)

    @property
    def advance_after_time(self) -> int:
        """Specifies the time, in milliseconds, after which the transition should start. This setting may be used in conjunction with the advClick attribute. If this attribute is not specified then it is assumed that no auto-advance will occur. Read/write ."""
        if self._transition_elem is not None:
            val = self._transition_elem.get('advTm')
            if val is not None:
                return int(val)
        return 0

    @advance_after_time.setter
    def advance_after_time(self, value: int):
        self._set_attribute('advTm', str(value))

    @property
    def speed(self) -> TransitionSpeed:
        """Specifies the transition speed that is to be used when transitioning from the current slide to the next. Read/write ."""
        from .TransitionSpeed import TransitionSpeed
        from .._internal.pptx.transition_mappings import SPEED_FROM_XML
        if self._transition_elem is not None:
            xml_val = self._transition_elem.get('spd', 'fast')
            enum_val = SPEED_FROM_XML.get(xml_val, 'Fast')
            return TransitionSpeed(enum_val)
        return TransitionSpeed.FAST

    @speed.setter
    def speed(self, value: TransitionSpeed):
        from .._internal.pptx.transition_mappings import SPEED_TO_XML
        xml_val = SPEED_TO_XML.get(value.value, 'fast')
        self._set_attribute('spd', xml_val)

    @property
    def value(self) -> ITransitionValueBase:
        """Slide show transition value. Read-only ."""
        return self._value_obj

    @property
    def type(self) -> TransitionType:
        """Type of transition. Read/write ."""
        from .TransitionType import TransitionType as TT
        if self._type_cache is not None:
            return self._type_cache
        return TT.NONE

    @type.setter
    def type(self, value: TransitionType):
        from .TransitionType import TransitionType as TT
        from .._internal.pptx.transition_mappings import (
            get_transition_info, EXTENSION_PREFIXES, P14_NS, P15_NS, P159_NS,
        )

        self._type_cache = value

        elem = self._ensure_transition_elem()

        # Remove existing transition type child elements
        for child in list(elem):
            if isinstance(child.tag, str):
                elem.remove(child)

        info = None if value == TT.NONE else get_transition_info(value.value)
        if info is None:
            self._place(None)
            self._value_obj = None
            return

        full_tag, cls_name, extra_attrs = info
        namespace = full_tag[1:].partition('}')[0]

        # Register namespaces before creating elements so prefixes are correct
        if P14_NS in full_tag:
            ET.register_namespace('p14', P14_NS)
        if P15_NS in full_tag:
            ET.register_namespace('p15', P15_NS)
        if P159_NS in full_tag:
            ET.register_namespace('p159', P159_NS)

        self._place(namespace if namespace in EXTENSION_PREFIXES else None)

        # Create the transition type child element
        child_elem = ET.SubElement(elem, full_tag)
        for attr_name, attr_val in extra_attrs.items():
            child_elem.set(attr_name, attr_val)

        # Create the value object
        cls = self._get_value_class(cls_name)
        obj = cls()
        obj._init_internal(child_elem, self._slide_part)
        self._value_obj = obj

    @property
    def duration(self) -> int:
        """Gets or sets the duration of the slide transition effect in milliseconds. Read/write ."""
        if self._transition_elem is not None:
            # Duration can be in p14:dur attribute or dur attribute
            p14_ns = 'http://schemas.microsoft.com/office/powerpoint/2010/main'
            dur = self._transition_elem.get(f'{{{p14_ns}}}dur')
            if dur is not None:
                return int(dur)
            dur = self._transition_elem.get('dur')
            if dur is not None:
                return int(dur)
        return 0

    @duration.setter
    def duration(self, value: int):
        p14_ns = 'http://schemas.microsoft.com/office/powerpoint/2010/main'
        elem = self._ensure_transition_elem()
        elem.set(f'{{{p14_ns}}}dur', str(value))
        ET.register_namespace('p14', p14_ns)
