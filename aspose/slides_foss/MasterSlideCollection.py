from __future__ import annotations
import re
from typing import TYPE_CHECKING, Any, Optional
from .IMasterSlideCollection import IMasterSlideCollection

if TYPE_CHECKING:
    from .IMasterSlide import IMasterSlide
    from .MasterSlide import MasterSlide
    from .IPresentation import IPresentation
    from ._internal.opc import OpcPackage
    from ._internal.pptx.presentation_part import PresentationPart

from ._internal.base_collection import BaseCollection
class MasterSlideCollection(BaseCollection, IMasterSlideCollection):
    """Represents a collection of master slides."""

    def _init_internal(self, presentation: IPresentation, package: OpcPackage,
                       presentation_part: PresentationPart,
                       master_slides: list = None) -> None:
        """
        Internal initialization for the master slide collection.

        Args:
            presentation: The parent Presentation object.
            package: The OPC package.
            presentation_part: The PresentationPart managing presentation.xml.
            master_slides: List of MasterSlide objects.
        """
        self._presentation = presentation
        self._package = package
        self._presentation_part = presentation_part
        self._masters: list = master_slides or []

    @property
    def as_i_collection(self) -> list:
        if hasattr(self, '_masters'):
            return list(self._masters)
        raise NotImplementedError("This feature is not yet available in this version.")

    @property
    def as_i_enumerable(self) -> Any:
        if hasattr(self, '_masters'):
            return iter(self._masters)
        raise NotImplementedError("This feature is not yet available in this version.")




    def add_clone(self, source_master) -> IMasterSlide:
        """
        Clone a master slide from another presentation and add it to this collection.

        Args:
            source_master: The master slide to clone.

        Returns:
            The cloned MasterSlide.
        """
        if not hasattr(self, '_masters'):
            raise NotImplementedError("This feature is not yet available in this version.")

        from .MasterSlide import MasterSlide
        from .LayoutSlide import LayoutSlide
        from ._internal.pptx.master_slide_part import MasterSlidePart
        from ._internal.pptx.layout_slide_part import LayoutSlidePart
        from ._internal.opc import RelationshipsManager, ContentTypesManager
        from ._internal.opc.relationships import REL_TYPES
        from ._internal.opc.content_types import CONTENT_TYPES

        source_package = source_master._package
        source_master_part_name = source_master._part_name

        # Determine next master slide number
        next_num = self._get_next_master_file_number()
        dest_master_part_name = f'ppt/slideMasters/slideMaster{next_num}.xml'

        # Get source master's layout relationships to track r:id mapping
        source_master_rels = RelationshipsManager(source_package, source_master_part_name)
        source_layout_rids = {}  # source_layout_part_name -> source_rid
        for rel in source_master_rels.get_all_relationships():
            if rel.type == REL_TYPES['slide_layout']:
                from ._internal.pptx.slide_part import SlidePart
                layout_path = SlidePart._resolve_target_static(source_master_part_name, rel.target)
                source_layout_rids[layout_path] = rel.id

        # Clone the master slide part (without layouts - they're handled separately)
        layout_rid_mapping = self._clone_master_part(
            source_package, source_master_part_name,
            self._package, dest_master_part_name
        )

        # Clone all layouts associated with this master
        source_layouts = list(source_master.layout_slides)
        cloned_layouts = []
        layout_part_mapping = {}  # old_part_name -> new_part_name

        for source_layout in source_layouts:
            source_layout_part_name = source_layout._part_name
            next_layout_num = self._get_next_layout_file_number()
            dest_layout_part_name = f'ppt/slideLayouts/slideLayout{next_layout_num}.xml'

            self._clone_layout_part(
                source_package, source_layout_part_name,
                self._package, dest_layout_part_name,
                dest_master_part_name
            )

            layout_part_mapping[source_layout_part_name] = dest_layout_part_name

            # Create LayoutSlide object
            layout_part = LayoutSlidePart(self._package, dest_layout_part_name)
            layout_slide = LayoutSlide()
            layout_slide._init_internal(
                presentation=self._presentation,
                package=self._package,
                part_name=dest_layout_part_name,
                layout_part=layout_part,
                master_resolver=lambda pn: self._masters[-1] if self._masters else None,
            )
            cloned_layouts.append(layout_slide)

            # Register layout in presentation's layout map
            if hasattr(self._presentation, '_layout_slides_map'):
                self._presentation._layout_slides_map[dest_layout_part_name] = layout_slide

        # Update master's relationships and XML to point to cloned layouts
        self._update_master_layout_relationships(
            source_package, source_master_part_name,
            dest_master_part_name, layout_part_mapping, source_layout_rids
        )

        # Add relationship from presentation to the new master
        pres_rels = RelationshipsManager(self._package, self._presentation_part.PART_NAME)
        relative_target = f'slideMasters/slideMaster{next_num}.xml'
        rel_id = pres_rels.add_relationship(REL_TYPES['slide_master'], relative_target)
        pres_rels.save()

        # Add master reference to presentation.xml
        master_ref = self._presentation_part.add_master_reference(rel_id)

        # Create MasterSlide object
        master_part = MasterSlidePart(self._package, dest_master_part_name)
        master_slide = MasterSlide()
        master_slide._init_internal(
            presentation=self._presentation,
            package=self._package,
            part_name=dest_master_part_name,
            master_part=master_part,
            layout_slides=cloned_layouts,
        )

        # Register in presentation's master map
        if hasattr(self._presentation, '_master_slides_map'):
            self._presentation._master_slides_map[dest_master_part_name] = master_slide

        self._masters.append(master_slide)
        return master_slide

    def _get_next_master_file_number(self) -> int:
        """Find the next available master slide file number."""
        existing_nums = set()
        for part_name in self._package.get_part_names():
            m = re.match(r'ppt/slideMasters/slideMaster(\d+)\.xml$', part_name)
            if m:
                existing_nums.add(int(m.group(1)))
        num = 1
        while num in existing_nums:
            num += 1
        return num

    def _get_next_layout_file_number(self) -> int:
        """Find the next available layout slide file number."""
        existing_nums = set()
        for part_name in self._package.get_part_names():
            m = re.match(r'ppt/slideLayouts/slideLayout(\d+)\.xml$', part_name)
            if m:
                existing_nums.add(int(m.group(1)))
        num = 1
        while num in existing_nums:
            num += 1
        return num

    def _clone_master_part(self, source_package, source_part_name,
                           dest_package, dest_part_name) -> dict:
        """
        Clone a master slide part and its related resources (except layouts).

        Returns:
            rid_mapping dict for non-layout relationships.
        """
        from ._internal.pptx.slide_part import SlidePart
        from ._internal.opc import RelationshipsManager, ContentTypesManager
        from ._internal.opc.relationships import REL_TYPES
        from ._internal.opc.content_types import CONTENT_TYPES
        import lxml.etree as ET
        import copy

        # Copy master XML
        source_content = source_package.get_part(source_part_name)
        if not source_content:
            raise ValueError(f"Master slide not found: {source_part_name}")

        source_root = ET.fromstring(source_content)
        dest_root = copy.deepcopy(source_root)

        # Copy relationships (theme, images, etc.) - but not layouts (handled separately)
        source_rels = RelationshipsManager(source_package, source_part_name)
        dest_rels = RelationshipsManager(dest_package, dest_part_name)
        rid_mapping = {}

        for rel in source_rels.get_all_relationships():
            if rel.type == REL_TYPES['slide_layout']:
                # Skip layouts - they're handled separately
                continue
            elif rel.target_mode == 'External':
                new_rid = dest_rels.add_relationship(
                    rel.type, rel.target, target_mode='External'
                )
            else:
                # Clone related parts (theme, images)
                source_target = SlidePart._resolve_target_static(source_part_name, rel.target)
                dest_target = SlidePart._clone_related_part(
                    source_package, source_target,
                    dest_package, dest_part_name, rel.type
                )
                relative_target = SlidePart._compute_relative_target(dest_part_name, dest_target)
                new_rid = dest_rels.add_relationship(rel.type, relative_target)
            rid_mapping[rel.id] = new_rid

        # Update r:id references in master XML (only for non-layout refs)
        SlidePart._update_rid_references(dest_root, rid_mapping)

        # Save master XML (will be updated again later with layout refs)
        xml_bytes = ET.tostring(
            dest_root, pretty_print=True, xml_declaration=True,
            encoding='UTF-8', standalone=True
        )
        dest_package.set_part(dest_part_name, xml_bytes)
        dest_rels.save()

        # Add content type
        ct_manager = ContentTypesManager(dest_package)
        ct_manager.add_override(dest_part_name, CONTENT_TYPES['slide_master'])
        ct_manager.save()

        return rid_mapping

    def _clone_layout_part(self, source_package, source_part_name,
                           dest_package, dest_part_name,
                           dest_master_part_name) -> None:
        """Clone a layout slide part."""
        from ._internal.pptx.slide_part import SlidePart
        from ._internal.opc import RelationshipsManager, ContentTypesManager
        from ._internal.opc.relationships import REL_TYPES
        from ._internal.opc.content_types import CONTENT_TYPES
        import lxml.etree as ET
        import copy

        # Copy layout XML
        source_content = source_package.get_part(source_part_name)
        if not source_content:
            raise ValueError(f"Layout slide not found: {source_part_name}")

        source_root = ET.fromstring(source_content)
        dest_root = copy.deepcopy(source_root)

        # Copy relationships
        source_rels = RelationshipsManager(source_package, source_part_name)
        dest_rels = RelationshipsManager(dest_package, dest_part_name)
        rid_mapping = {}

        for rel in source_rels.get_all_relationships():
            if rel.type == REL_TYPES['slide_master']:
                # Point to the cloned master
                relative_target = SlidePart._compute_relative_target(
                    dest_part_name, dest_master_part_name
                )
                new_rid = dest_rels.add_relationship(rel.type, relative_target)
            elif rel.target_mode == 'External':
                new_rid = dest_rels.add_relationship(
                    rel.type, rel.target, target_mode='External'
                )
            else:
                source_target = SlidePart._resolve_target_static(source_part_name, rel.target)
                dest_target = SlidePart._clone_related_part(
                    source_package, source_target,
                    dest_package, dest_part_name, rel.type
                )
                relative_target = SlidePart._compute_relative_target(dest_part_name, dest_target)
                new_rid = dest_rels.add_relationship(rel.type, relative_target)
            rid_mapping[rel.id] = new_rid

        # Update r:id references
        SlidePart._update_rid_references(dest_root, rid_mapping)

        # Save layout XML
        xml_bytes = ET.tostring(
            dest_root, pretty_print=True, xml_declaration=True,
            encoding='UTF-8', standalone=True
        )
        dest_package.set_part(dest_part_name, xml_bytes)
        dest_rels.save()

        # Add content type
        ct_manager = ContentTypesManager(dest_package)
        ct_manager.add_override(dest_part_name, CONTENT_TYPES['slide_layout'])
        ct_manager.save()

    def _get_max_master_layout_id_in_presentation(self) -> int:
        """
        Find the maximum ID across all master slide IDs and layout IDs.

        In PPTX, sldMasterIdLst and sldLayoutIdLst share the same ID space.

        Returns:
            The maximum ID found, or 2147483647 if none exist.
        """
        import lxml.etree as ET

        max_id = 2147483647  # One below the PPTX convention start
        ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'

        # Check master IDs from presentation.xml
        for ref in self._presentation_part.master_references:
            if ref.master_id > max_id:
                max_id = ref.master_id

        # Check layout IDs from all master slide XML files
        for part_name in self._package.get_part_names():
            if part_name.startswith('ppt/slideMasters/') and part_name.endswith('.xml'):
                content = self._package.get_part(part_name)
                if content:
                    root = ET.fromstring(content)
                    for elem in root.iter(f'{{{ns_p}}}sldLayoutId'):
                        layout_id = int(elem.get('id', '0'))
                        if layout_id > max_id:
                            max_id = layout_id

        return max_id

    def _update_master_layout_relationships(self, source_package, source_master_part_name,
                                             dest_master_part_name,
                                             layout_mapping: dict,
                                             source_layout_rids: dict) -> None:
        """
        Update master's relationships and XML to point to cloned layouts.

        Args:
            source_package: Source OPC package.
            source_master_part_name: Source master's part name.
            dest_master_part_name: Destination master's part name.
            layout_mapping: Dict of old_layout_path -> new_layout_path.
            source_layout_rids: Dict of source_layout_path -> source_rid.
        """
        from ._internal.opc import RelationshipsManager
        from ._internal.opc.relationships import REL_TYPES
        from ._internal.pptx.slide_part import SlidePart
        import lxml.etree as ET

        master_rels = RelationshipsManager(self._package, dest_master_part_name)

        # Track source r:id -> new r:id mapping for layout relationships
        layout_rid_mapping = {}

        for old_layout_path, new_layout_path in layout_mapping.items():
            relative_target = SlidePart._compute_relative_target(
                dest_master_part_name, new_layout_path
            )
            new_rid = master_rels.add_relationship(REL_TYPES['slide_layout'], relative_target)

            # Map old rid to new rid
            old_rid = source_layout_rids.get(old_layout_path)
            if old_rid:
                layout_rid_mapping[old_rid] = new_rid

        master_rels.save()

        # Update the master XML's sldLayoutIdLst references
        master_content = self._package.get_part(dest_master_part_name)
        if master_content:
            master_root = ET.fromstring(master_content)

            # Update r:id references in sldLayoutIdLst
            SlidePart._update_rid_references(master_root, layout_rid_mapping)

            # Renumber layout IDs to avoid conflicts with existing masters
            ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
            next_layout_id = self._get_max_master_layout_id_in_presentation() + 1
            for elem in master_root.iter(f'{{{ns_p}}}sldLayoutId'):
                elem.set('id', str(next_layout_id))
                next_layout_id += 1

            # Save updated master XML
            xml_bytes = ET.tostring(
                master_root, pretty_print=True, xml_declaration=True,
                encoding='UTF-8', standalone=True
            )
            self._package.set_part(dest_master_part_name, xml_bytes)


    def __getitem__(self, index: int) -> MasterSlide:
        if hasattr(self, '_masters'):
            return self._masters[index]
        raise NotImplementedError("This feature is not yet available in this version.")

    def __len__(self) -> int:
        if hasattr(self, '_masters'):
            return len(self._masters)
        raise NotImplementedError("This feature is not yet available in this version.")

    def __iter__(self):
        if hasattr(self, '_masters'):
            return iter(self._masters)
        raise NotImplementedError("This feature is not yet available in this version.")

