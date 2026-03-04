"""
Layout slide part handling for PPTX format.

Manages ppt/slideLayouts/slideLayoutN.xml parts (read-only for now).
"""

from __future__ import annotations
import lxml.etree as ET
from typing import Optional, TYPE_CHECKING

from .constants import NS, Elements, NAMESPACES
from ..opc import RelationshipsManager
from ..opc.relationships import REL_TYPES

if TYPE_CHECKING:
    from ..opc import OpcPackage

# OOXML layout type values mapped to SlideLayoutType enum values
_LAYOUT_TYPE_MAP = {
    'blank': 'Blank',
    'chart': 'Chart',
    'chartAndTx': 'ChartAndText',
    'clipArtAndTx': 'ClipArtAndText',
    'clipArtAndVertTx': 'ClipArtAndVerticalText',
    'cust': 'Custom',
    'dgm': 'Diagram',
    'fourObj': 'FourObjects',
    'mediaAndTx': 'MediaAndText',
    'obj': 'TitleAndObject',
    'objAndTx': 'ObjectAndText',
    'objAndTwoObj': 'ObjectAndTwoObject',
    'objOnly': 'Object',
    'objOverTx': 'ObjectOverText',
    'objTx': 'TextAndObject',
    'picTx': 'PictureAndCaption',
    'secHead': 'SectionHeader',
    'tbl': 'Table',
    'title': 'Title',
    'titleOnly': 'TitleOnly',
    'tx': 'Text',
    'txAndChart': 'TextAndChart',
    'txAndClipArt': 'TextAndClipArt',
    'txAndMedia': 'TextAndMedia',
    'txAndObj': 'TextAndObject',
    'txAndTwoObj': 'TextAndTwoObjects',
    'txOverObj': 'TextOverObject',
    'twoColTx': 'TwoColumnText',
    'twoObj': 'TwoObjects',
    'twoObjAndObj': 'TwoObjectsAndObject',
    'twoObjAndTx': 'TwoObjectsAndText',
    'twoObjOverTx': 'TwoObjectsOverText',
    'twoTxTwoObj': 'TwoTextAndTwoObjects',
    'vertTitleAndTx': 'VerticalTitleAndText',
    'vertTitleAndTxOverChart': 'VerticalTitleAndTextOverChart',
    'vertTx': 'VerticalText',
}


class LayoutSlidePart:
    """
    Manages a layout slide XML part (ppt/slideLayouts/slideLayoutN.xml).

    Read-only for now; provides access to layout properties.
    """

    def __init__(self, package: OpcPackage, part_name: str):
        """
        Initialize a layout slide part.

        Args:
            package: The OPC package containing the layout.
            part_name: The part path (e.g., 'ppt/slideLayouts/slideLayout1.xml').
        """
        self._package = package
        self._part_name = part_name
        self._root: Optional[ET._Element] = None
        self._rels_manager = RelationshipsManager(package, part_name)
        self._load()

    def _load(self) -> None:
        """Load and parse the layout slide XML."""
        content = self._package.get_part(self._part_name)
        if content:
            self._root = ET.fromstring(content)
        else:
            raise ValueError(f"Layout slide part not found: {self._part_name}")

    @property
    def part_name(self) -> str:
        """Get the part name of this layout slide."""
        return self._part_name

    @property
    def name(self) -> str:
        """Get the layout name from <p:cSld name='...'>."""
        csld = self._root.find(f".//{Elements.C_SLD}")
        if csld is not None:
            return csld.get('name', '')
        return ''

    @name.setter
    def name(self, value: str) -> None:
        """Set the layout name on <p:cSld name='...'>."""
        csld = self._root.find(f".//{Elements.C_SLD}")
        if csld is not None:
            csld.set('name', value)

    @property
    def layout_type_raw(self) -> str:
        """Get the raw layout type string from <p:sldLayout type='...'>."""
        return self._root.get('type', 'cust')

    @property
    def layout_type_value(self) -> str:
        """Get the SlideLayoutType enum value string for this layout."""
        raw = self.layout_type_raw
        return _LAYOUT_TYPE_MAP.get(raw, 'Custom')

    @property
    def master_part_name(self) -> Optional[str]:
        """Resolve the master slide part name from the layout's relationships."""
        rels = self._rels_manager.get_relationships_by_type(REL_TYPES['slide_master'])
        if rels:
            target = rels[0].target
            return self._resolve_target(target)
        return None

    def _resolve_target(self, target: str) -> str:
        """Resolve a relative target path to an absolute part name."""
        if target.startswith('/'):
            return target.lstrip('/')
        base_dir = self._part_name.rsplit('/', 1)[0] if '/' in self._part_name else ''
        parts = (base_dir + '/' + target).split('/')
        resolved = []
        for part in parts:
            if part == '..':
                if resolved:
                    resolved.pop()
            elif part and part != '.':
                resolved.append(part)
        return '/'.join(resolved)

    def save(self) -> None:
        """Save the layout slide XML back to the package."""
        xml_bytes = ET.tostring(
            self._root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True
        )
        self._package.set_part(self._part_name, xml_bytes)
        self._rels_manager.save()
