"""
Parse and serialize docProps/core.xml (Dublin Core metadata).

Handles: title, subject, creator (author), keywords, description (comments),
category, contentStatus, contentType, lastModifiedBy, revision, created, modified, lastPrinted.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from lxml import etree

from .constants import NAMESPACES

PART_NAME = 'docProps/core.xml'

_NS_CP = NAMESPACES['cp']
_NS_DC = 'http://purl.org/dc/elements/1.1/'
_NS_DCTERMS = 'http://purl.org/dc/terms/'
_NS_XSI = 'http://www.w3.org/2001/XMLSchema-instance'

_NSMAP = {
    'cp': _NS_CP,
    'dc': _NS_DC,
    'dcterms': _NS_DCTERMS,
    'dcmitype': 'http://purl.org/dc/dcmitype/',
    'xsi': _NS_XSI,
}

# Tags with their full namespace
_DC = f'{{{_NS_DC}}}'
_CP = f'{{{_NS_CP}}}'
_DCTERMS = f'{{{_NS_DCTERMS}}}'
_XSI = f'{{{_NS_XSI}}}'


def _parse_w3cdtf(text: Optional[str]) -> Optional[datetime]:
    """Parse a W3CDTF datetime string to a datetime object."""
    if not text or not text.strip():
        return None
    text = text.strip()
    try:
        # Try ISO format with Z suffix
        if text.endswith('Z'):
            text = text[:-1] + '+00:00'
        return datetime.fromisoformat(text)
    except (ValueError, TypeError):
        return None


def _format_w3cdtf(dt: Optional[datetime]) -> Optional[str]:
    """Format a datetime as W3CDTF string."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


class CorePropertiesPart:
    """Parse/serialize docProps/core.xml."""

    def __init__(self, package):
        self._package = package
        self._root = None
        self._parsed = False
        self._dirty = False

        # String properties
        self.title: Optional[str] = None
        self.subject: Optional[str] = None
        self.creator: Optional[str] = None
        self.keywords: Optional[str] = None
        self.description: Optional[str] = None
        self.category: Optional[str] = None
        self.content_status: Optional[str] = None
        self.content_type: Optional[str] = None
        self.last_modified_by: Optional[str] = None
        self.revision: Optional[str] = None

        # Date properties
        self.created: Optional[datetime] = None
        self.modified: Optional[datetime] = None
        self.last_printed: Optional[datetime] = None

        self._parse()

    def _parse(self):
        """Parse core.xml from the package."""
        data = self._package.get_part(PART_NAME)
        if data is None:
            self._parsed = True
            return

        self._root = etree.fromstring(data)
        self._parsed = True

        self.title = self._get_text(f'{_DC}title')
        self.subject = self._get_text(f'{_DC}subject')
        self.creator = self._get_text(f'{_DC}creator')
        self.keywords = self._get_text(f'{_CP}keywords')
        self.description = self._get_text(f'{_DC}description')
        self.category = self._get_text(f'{_CP}category')
        self.content_status = self._get_text(f'{_CP}contentStatus')
        self.content_type = self._get_text(f'{_CP}contentType')
        self.last_modified_by = self._get_text(f'{_CP}lastModifiedBy')
        self.revision = self._get_text(f'{_CP}revision')

        self.created = _parse_w3cdtf(self._get_text(f'{_DCTERMS}created'))
        self.modified = _parse_w3cdtf(self._get_text(f'{_DCTERMS}modified'))
        self.last_printed = _parse_w3cdtf(self._get_text(f'{_CP}lastPrinted'))

    def _get_text(self, tag: str) -> Optional[str]:
        """Get text content of a child element."""
        if self._root is None:
            return None
        el = self._root.find(tag)
        if el is not None and el.text:
            return el.text
        return None

    def mark_dirty(self):
        self._dirty = True

    def save(self):
        """Serialize back to the package."""
        if not self._dirty and self._root is not None:
            return

        root = etree.Element(f'{_CP}coreProperties', nsmap=_NSMAP)

        self._set_dc(root, 'title', self.title)
        self._set_dc(root, 'subject', self.subject)
        self._set_dc(root, 'creator', self.creator)
        self._set_cp(root, 'keywords', self.keywords)
        self._set_dc(root, 'description', self.description)
        self._set_cp(root, 'category', self.category)
        self._set_cp(root, 'contentStatus', self.content_status)
        self._set_cp(root, 'contentType', self.content_type)
        self._set_cp(root, 'lastModifiedBy', self.last_modified_by)
        self._set_cp(root, 'revision', self.revision)

        self._set_dcterms_date(root, 'created', self.created)
        self._set_dcterms_date(root, 'modified', self.modified)
        if self.last_printed is not None:
            self._set_cp(root, 'lastPrinted', _format_w3cdtf(self.last_printed))

        xml_bytes = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
        self._package.set_part(PART_NAME, xml_bytes)
        self._dirty = False

    def _set_dc(self, root, local_name, value):
        if value is not None:
            el = etree.SubElement(root, f'{_DC}{local_name}')
            el.text = value

    def _set_cp(self, root, local_name, value):
        if value is not None:
            el = etree.SubElement(root, f'{_CP}{local_name}')
            el.text = value

    def _set_dcterms_date(self, root, local_name, dt):
        if dt is not None:
            el = etree.SubElement(root, f'{_DCTERMS}{local_name}')
            el.set(f'{_XSI}type', 'dcterms:W3CDTF')
            el.text = _format_w3cdtf(dt)

    def clear(self):
        """Reset all properties to None."""
        self.title = None
        self.subject = None
        self.creator = None
        self.keywords = None
        self.description = None
        self.category = None
        self.content_status = None
        self.content_type = None
        self.last_modified_by = None
        self.revision = None
        self.created = None
        self.modified = None
        self.last_printed = None
        self._dirty = True
