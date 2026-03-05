"""
Parse and serialize docProps/custom.xml.

Each custom property is stored as:
<property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="N" name="...">
    <vt:type>value</vt:type>
</property>

Type mapping: str->lpwstr, int->i4, float->r8, bool->bool, datetime->filetime.
PIDs start at 2. The file is created on demand only when custom properties are added.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from lxml import etree

PART_NAME = 'docProps/custom.xml'

_NS_CUSTOM = 'http://schemas.openxmlformats.org/officeDocument/2006/custom-properties'
_NS_VT = 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'

_CUSTOM = f'{{{_NS_CUSTOM}}}'
_VT = f'{{{_NS_VT}}}'

_NSMAP = {
    None: _NS_CUSTOM,
    'vt': _NS_VT,
}

_FMTID = '{D5CDD505-2E9C-101B-9397-08002B2CF9AE}'

# Datetime epoch for FILETIME (Jan 1, 1601)
_FILETIME_EPOCH = datetime(1601, 1, 1, tzinfo=timezone.utc)


class CustomPropertiesPart:
    """Parse/serialize docProps/custom.xml."""

    def __init__(self, package):
        self._package = package
        self._properties: dict[str, Any] = {}  # name -> value (typed)
        self._dirty = False
        self._parse()

    def _parse(self):
        data = self._package.get_part(PART_NAME)
        if data is None:
            return

        root = etree.fromstring(data)
        for prop_el in root.findall(f'{_CUSTOM}property'):
            name = prop_el.get('name')
            if name is None:
                continue
            value = self._read_value(prop_el)
            if value is not None:
                self._properties[name] = value

    def _read_value(self, prop_el) -> Any:
        """Read a typed value from a property element."""
        for child in prop_el:
            tag = child.tag
            text = child.text or ''

            if tag == f'{_VT}lpwstr':
                return text
            elif tag == f'{_VT}i4':
                try:
                    return int(text)
                except ValueError:
                    return 0
            elif tag == f'{_VT}r8':
                try:
                    return float(text)
                except ValueError:
                    return 0.0
            elif tag == f'{_VT}bool':
                return text.lower() in ('true', '1')
            elif tag == f'{_VT}filetime':
                return self._parse_filetime(text)
        return None

    def _parse_filetime(self, text: str) -> Optional[datetime]:
        """Parse a filetime string (ISO 8601 format in OOXML)."""
        if not text:
            return None
        try:
            if text.endswith('Z'):
                text = text[:-1] + '+00:00'
            return datetime.fromisoformat(text)
        except (ValueError, TypeError):
            return None

    @property
    def count(self) -> int:
        return len(self._properties)

    def contains(self, name: str) -> bool:
        return name in self._properties

    def get_name(self, index: int) -> str:
        names = list(self._properties.keys())
        if 0 <= index < len(names):
            return names[index]
        raise IndexError(f"Index {index} out of range")

    def get_value(self, name: str) -> Any:
        return self._properties.get(name)

    def set_value(self, name: str, value: Any) -> None:
        self._properties[name] = value
        self._dirty = True

    def remove(self, name: str) -> bool:
        if name in self._properties:
            del self._properties[name]
            self._dirty = True
            return True
        return False

    def clear(self):
        if self._properties:
            self._properties.clear()
            self._dirty = True

    def save(self):
        """Serialize back to the package. Only writes if there are properties."""
        if not self._dirty:
            return

        if not self._properties:
            # Remove the part if no custom properties remain
            self._package.delete_part(PART_NAME)
            self._dirty = False
            return

        root = etree.Element(f'{_CUSTOM}Properties', nsmap=_NSMAP)

        pid = 2
        for name, value in self._properties.items():
            prop_el = etree.SubElement(root, f'{_CUSTOM}property', attrib={
                'fmtid': _FMTID,
                'pid': str(pid),
                'name': name,
            })
            self._write_value(prop_el, value)
            pid += 1

        xml_bytes = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
        self._package.set_part(PART_NAME, xml_bytes)

        # Ensure content type and relationship exist
        self._ensure_content_type()
        self._ensure_relationship()
        self._dirty = False

    def _write_value(self, prop_el, value):
        """Write a typed value element."""
        if isinstance(value, bool):
            el = etree.SubElement(prop_el, f'{_VT}bool')
            el.text = 'true' if value else 'false'
        elif isinstance(value, int):
            el = etree.SubElement(prop_el, f'{_VT}i4')
            el.text = str(value)
        elif isinstance(value, float):
            el = etree.SubElement(prop_el, f'{_VT}r8')
            el.text = str(value)
        elif isinstance(value, datetime):
            el = etree.SubElement(prop_el, f'{_VT}filetime')
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            el.text = value.strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            el = etree.SubElement(prop_el, f'{_VT}lpwstr')
            el.text = str(value)

    def _ensure_content_type(self):
        """Ensure [Content_Types].xml has an entry for custom.xml."""
        ct_data = self._package.get_part('[Content_Types].xml')
        if ct_data is None:
            return
        ct_root = etree.fromstring(ct_data)
        ct_ns = 'http://schemas.openxmlformats.org/package/2006/content-types'
        ct_tag = f'{{{ct_ns}}}'

        # Check if override already exists
        for override in ct_root.findall(f'{ct_tag}Override'):
            if override.get('PartName') == '/docProps/custom.xml':
                return

        etree.SubElement(ct_root, f'{ct_tag}Override', attrib={
            'PartName': '/docProps/custom.xml',
            'ContentType': 'application/vnd.openxmlformats-officedocument.custom-properties+xml',
        })
        self._package.set_part('[Content_Types].xml',
                               etree.tostring(ct_root, xml_declaration=True, encoding='UTF-8', standalone=True))

    def _ensure_relationship(self):
        """Ensure _rels/.rels has a relationship for custom.xml."""
        rels_data = self._package.get_part('_rels/.rels')
        if rels_data is None:
            return
        rels_ns = 'http://schemas.openxmlformats.org/package/2006/relationships'
        rels_root = etree.fromstring(rels_data)

        rel_type = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/custom-properties'

        # Check if relationship already exists
        for rel in rels_root:
            if rel.get('Type') == rel_type:
                return

        # Find next rId
        max_id = 0
        for rel in rels_root:
            rid = rel.get('Id', '')
            if rid.startswith('rId'):
                try:
                    max_id = max(max_id, int(rid[3:]))
                except ValueError:
                    pass

        etree.SubElement(rels_root, 'Relationship', attrib={
            'Id': f'rId{max_id + 1}',
            'Type': rel_type,
            'Target': 'docProps/custom.xml',
        })
        self._package.set_part('_rels/.rels',
                               etree.tostring(rels_root, xml_declaration=True, encoding='UTF-8', standalone=True))
