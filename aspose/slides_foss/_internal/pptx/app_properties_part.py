"""
Parse and serialize docProps/app.xml (extended properties).

Handles: Application, AppVersion, Company, Manager, PresentationFormat,
Template, TotalTime, Slides, HiddenSlides, Notes, Paragraphs, Words,
MMClips, ScaleCrop, LinksUpToDate, SharedDoc, HyperlinksChanged,
HyperlinkBase, HeadingPairs, TitlesOfParts.
"""

from __future__ import annotations

from typing import Optional

from lxml import etree

from .constants import NAMESPACES

PART_NAME = 'docProps/app.xml'

_NS_EP = NAMESPACES['ep']
_NS_VT = 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'

_EP = f'{{{_NS_EP}}}'
_VT = f'{{{_NS_VT}}}'

_NSMAP = {
    None: _NS_EP,
    'vt': _NS_VT,
}


class HeadingPairData:
    """Internal representation of a heading pair."""
    def __init__(self, name: str, count: int):
        self.name = name
        self.count = count


class AppPropertiesPart:
    """Parse/serialize docProps/app.xml."""

    def __init__(self, package):
        self._package = package
        self._root = None
        self._dirty = False

        # String properties
        self.application: Optional[str] = None
        self.app_version: Optional[str] = None
        self.company: Optional[str] = None
        self.manager: Optional[str] = None
        self.presentation_format: Optional[str] = None
        self.template: Optional[str] = None
        self.hyperlink_base: Optional[str] = None

        # Integer properties
        self.total_time: Optional[int] = None
        self.slides: Optional[int] = None
        self.hidden_slides: Optional[int] = None
        self.notes: Optional[int] = None
        self.paragraphs: Optional[int] = None
        self.words: Optional[int] = None
        self.mm_clips: Optional[int] = None

        # Boolean properties
        self.scale_crop: Optional[bool] = None
        self.links_up_to_date: Optional[bool] = None
        self.shared_doc: Optional[bool] = None
        self.hyperlinks_changed: Optional[bool] = None

        # Vector properties
        self.heading_pairs: list[HeadingPairData] = []
        self.titles_of_parts: list[str] = []

        self._parse()

    def _parse(self):
        data = self._package.get_part(PART_NAME)
        if data is None:
            return

        self._root = etree.fromstring(data)

        self.application = self._get_text('Application')
        self.app_version = self._get_text('AppVersion')
        self.company = self._get_text('Company')
        self.manager = self._get_text('Manager')
        self.presentation_format = self._get_text('PresentationFormat')
        self.template = self._get_text('Template')
        self.hyperlink_base = self._get_text('HyperlinkBase')

        self.total_time = self._get_int('TotalTime')
        self.slides = self._get_int('Slides')
        self.hidden_slides = self._get_int('HiddenSlides')
        self.notes = self._get_int('Notes')
        self.paragraphs = self._get_int('Paragraphs')
        self.words = self._get_int('Words')
        self.mm_clips = self._get_int('MMClips')

        self.scale_crop = self._get_bool('ScaleCrop')
        self.links_up_to_date = self._get_bool('LinksUpToDate')
        self.shared_doc = self._get_bool('SharedDoc')
        self.hyperlinks_changed = self._get_bool('HyperlinksChanged')

        self._parse_heading_pairs()
        self._parse_titles_of_parts()

    def _get_text(self, local_name: str) -> Optional[str]:
        if self._root is None:
            return None
        el = self._root.find(f'{_EP}{local_name}')
        if el is not None and el.text:
            return el.text
        return None

    def _get_int(self, local_name: str) -> Optional[int]:
        text = self._get_text(local_name)
        if text is not None:
            try:
                return int(text)
            except ValueError:
                pass
        return None

    def _get_bool(self, local_name: str) -> Optional[bool]:
        text = self._get_text(local_name)
        if text is not None:
            return text.lower() in ('true', '1')
        return None

    def _parse_heading_pairs(self):
        """Parse HeadingPairs from vt:vector."""
        if self._root is None:
            return
        hp_el = self._root.find(f'{_EP}HeadingPairs')
        if hp_el is None:
            return
        vector = hp_el.find(f'{_VT}vector')
        if vector is None:
            return

        variants = vector.findall(f'{_VT}variant')
        # Pairs come as (name_variant, count_variant) alternating
        i = 0
        while i + 1 < len(variants):
            name_variant = variants[i]
            count_variant = variants[i + 1]

            name_el = name_variant.find(f'{_VT}lpstr')
            count_el = count_variant.find(f'{_VT}i4')

            if name_el is not None and count_el is not None:
                name = name_el.text or ''
                try:
                    count = int(count_el.text)
                except (ValueError, TypeError):
                    count = 0
                self.heading_pairs.append(HeadingPairData(name, count))
            i += 2

    def _parse_titles_of_parts(self):
        """Parse TitlesOfParts from vt:vector."""
        if self._root is None:
            return
        tp_el = self._root.find(f'{_EP}TitlesOfParts')
        if tp_el is None:
            return
        vector = tp_el.find(f'{_VT}vector')
        if vector is None:
            return

        for lpstr in vector.findall(f'{_VT}lpstr'):
            self.titles_of_parts.append(lpstr.text or '')

    def mark_dirty(self):
        self._dirty = True

    def save(self):
        """Serialize back to the package."""
        if not self._dirty and self._root is not None:
            return

        root = etree.Element(f'{_EP}Properties', nsmap=_NSMAP)

        self._set_text(root, 'Application', self.application)
        self._set_text(root, 'AppVersion', self.app_version)
        self._set_text(root, 'Company', self.company)
        self._set_text(root, 'Manager', self.manager)
        self._set_text(root, 'PresentationFormat', self.presentation_format)
        self._set_text(root, 'Template', self.template)
        self._set_text(root, 'HyperlinkBase', self.hyperlink_base)

        self._set_int(root, 'TotalTime', self.total_time)
        self._set_int(root, 'Slides', self.slides)
        self._set_int(root, 'HiddenSlides', self.hidden_slides)
        self._set_int(root, 'Notes', self.notes)
        self._set_int(root, 'Paragraphs', self.paragraphs)
        self._set_int(root, 'Words', self.words)
        self._set_int(root, 'MMClips', self.mm_clips)

        self._set_bool(root, 'ScaleCrop', self.scale_crop)
        self._set_bool(root, 'LinksUpToDate', self.links_up_to_date)
        self._set_bool(root, 'SharedDoc', self.shared_doc)
        self._set_bool(root, 'HyperlinksChanged', self.hyperlinks_changed)

        if self.heading_pairs:
            self._write_heading_pairs(root)
        if self.titles_of_parts:
            self._write_titles_of_parts(root)

        xml_bytes = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
        self._package.set_part(PART_NAME, xml_bytes)
        self._dirty = False

    def _set_text(self, root, local_name, value):
        if value is not None:
            el = etree.SubElement(root, f'{_EP}{local_name}')
            el.text = value

    def _set_int(self, root, local_name, value):
        if value is not None:
            el = etree.SubElement(root, f'{_EP}{local_name}')
            el.text = str(value)

    def _set_bool(self, root, local_name, value):
        if value is not None:
            el = etree.SubElement(root, f'{_EP}{local_name}')
            el.text = 'true' if value else 'false'

    def _write_heading_pairs(self, root):
        hp_el = etree.SubElement(root, f'{_EP}HeadingPairs')
        vector = etree.SubElement(hp_el, f'{_VT}vector', attrib={
            'size': str(len(self.heading_pairs) * 2),
            'baseType': 'variant',
        })
        for pair in self.heading_pairs:
            v1 = etree.SubElement(vector, f'{_VT}variant')
            lpstr = etree.SubElement(v1, f'{_VT}lpstr')
            lpstr.text = pair.name

            v2 = etree.SubElement(vector, f'{_VT}variant')
            i4 = etree.SubElement(v2, f'{_VT}i4')
            i4.text = str(pair.count)

    def _write_titles_of_parts(self, root):
        tp_el = etree.SubElement(root, f'{_EP}TitlesOfParts')
        vector = etree.SubElement(tp_el, f'{_VT}vector', attrib={
            'size': str(len(self.titles_of_parts)),
            'baseType': 'lpstr',
        })
        for title in self.titles_of_parts:
            lpstr = etree.SubElement(vector, f'{_VT}lpstr')
            lpstr.text = title

    def clear(self):
        """Reset all properties to None/empty."""
        self.application = None
        self.app_version = None
        self.company = None
        self.manager = None
        self.presentation_format = None
        self.template = None
        self.hyperlink_base = None
        self.total_time = None
        self.slides = None
        self.hidden_slides = None
        self.notes = None
        self.paragraphs = None
        self.words = None
        self.mm_clips = None
        self.scale_crop = None
        self.links_up_to_date = None
        self.shared_doc = None
        self.hyperlinks_changed = None
        self.heading_pairs = []
        self.titles_of_parts = []
        self._dirty = True
