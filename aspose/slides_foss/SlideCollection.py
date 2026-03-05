from __future__ import annotations
import re
from typing import overload, Optional, TYPE_CHECKING, Any
from .ISlideCollection import ISlideCollection

if TYPE_CHECKING:
    from .ISlide import ISlide
    from .Slide import Slide
    from .IPresentation import IPresentation
    from ._internal.opc import OpcPackage
    from ._internal.pptx.presentation_part import PresentationPart

from ._internal.base_collection import BaseCollection
class SlideCollection(BaseCollection, ISlideCollection):
    """Represents a collection of a slides."""

    def _init_internal(self, presentation: IPresentation, package: OpcPackage,
                       presentation_part: PresentationPart,
                       layout_resolver=None) -> None:
        """
        Internal initialization for the slide collection.

        Args:
            presentation: The parent Presentation object.
            package: The OPC package.
            presentation_part: The PresentationPart managing presentation.xml.
            layout_resolver: Callable(part_name) -> LayoutSlide.
        """
        from .Slide import Slide as SlideClass
        from ._internal.pptx.slide_part import SlidePart
        from ._internal.pptx.presentation_part import PresentationPart as PresPart
        from ._internal.opc import RelationshipsManager
        from ._internal.opc.relationships import REL_TYPES

        self._presentation = presentation
        self._package = package
        self._presentation_part = presentation_part
        self._layout_resolver = layout_resolver
        self._slides: list[SlideClass] = []

        # Resolve the presentation's relationships to find slide targets
        pres_rels = RelationshipsManager(package, PresPart.PART_NAME)

        for slide_ref in presentation_part.slide_references:
            rel = pres_rels.get_relationship(slide_ref.rel_id)
            if rel is None:
                continue

            # Resolve the target path relative to ppt/
            target = rel.target
            if target.startswith('/'):
                part_name = target.lstrip('/')
            else:
                part_name = 'ppt/' + target

            slide_part = SlidePart(package, part_name)
            slide = SlideClass()
            slide._init_internal(
                presentation=presentation,
                package=package,
                part_name=part_name,
                slide_ref=slide_ref,
                slide_part=slide_part,
                layout_resolver=layout_resolver,
            )
            self._slides.append(slide)

    @property
    def as_i_collection(self) -> list:
        if hasattr(self, '_slides'):
            return list(self._slides)
        raise ValueError("Unsupported arguments for this method.")

    @property
    def as_i_enumerable(self) -> Any:
        if hasattr(self, '_slides'):
            return iter(self._slides)
        raise ValueError("Unsupported arguments for this method.")





    def add_clone(self, *args, **kwargs) -> ISlide:
        """
        Clone a slide and add it to the end of the collection.

        Overloads:
            add_clone(source_slide) -> ISlide
            add_clone(source_slide, section) -> ISlide
            add_clone(source_slide, dest_layout) -> ISlide
            add_clone(source_slide, dest_master, allow_clone_missing_layout) -> ISlide
        """
        if not hasattr(self, '_slides'):
            raise ValueError("Unsupported arguments for this method.")

        from .ISection import ISection
        from .ILayoutSlide import ILayoutSlide
        from .IMasterSlide import IMasterSlide

        if len(args) == 1:
            # add_clone(source_slide)
            source_slide = args[0]
            return self._clone_slide_internal(source_slide, index=-1)

        elif len(args) == 2:
            source_slide = args[0]
            second_arg = args[1]

            # Determine if second arg is section or layout
            if hasattr(second_arg, 'section_id'):
                # add_clone(source_slide, section)
                # Clone to end of section - for now, clone to end of presentation
                return self._clone_slide_internal(source_slide, index=-1)
            else:
                # add_clone(source_slide, dest_layout)
                return self._clone_slide_internal(
                    source_slide, index=-1, dest_layout=second_arg
                )

        elif len(args) == 3:
            # add_clone(source_slide, dest_master, allow_clone_missing_layout)
            source_slide = args[0]
            dest_master = args[1]
            allow_clone_missing_layout = args[2]
            return self._clone_slide_internal(
                source_slide, index=-1,
                dest_master=dest_master,
                allow_clone_missing_layout=allow_clone_missing_layout
            )

        raise ValueError("Unsupported arguments for this method.")




    def insert_clone(self, *args, **kwargs) -> ISlide:
        """
        Clone a slide and insert it at a specific position.

        Overloads:
            insert_clone(index, source_slide) -> ISlide
            insert_clone(index, source_slide, dest_layout) -> ISlide
            insert_clone(index, source_slide, dest_master, allow_clone_missing_layout) -> ISlide
        """
        if not hasattr(self, '_slides'):
            raise ValueError("Unsupported arguments for this method.")

        if len(args) == 2:
            # insert_clone(index, source_slide)
            index = args[0]
            source_slide = args[1]
            return self._clone_slide_internal(source_slide, index=index)

        elif len(args) == 3:
            # insert_clone(index, source_slide, dest_layout)
            index = args[0]
            source_slide = args[1]
            dest_layout = args[2]
            return self._clone_slide_internal(
                source_slide, index=index, dest_layout=dest_layout
            )

        elif len(args) == 4:
            # insert_clone(index, source_slide, dest_master, allow_clone_missing_layout)
            index = args[0]
            source_slide = args[1]
            dest_master = args[2]
            allow_clone_missing_layout = args[3]
            return self._clone_slide_internal(
                source_slide, index=index,
                dest_master=dest_master,
                allow_clone_missing_layout=allow_clone_missing_layout
            )

        raise ValueError("Unsupported arguments for this method.")



    def to_array(self, *args, **kwargs) -> list[ISlide]:
        if not hasattr(self, '_slides'):
            raise ValueError("Unsupported arguments for this method.")
        if len(args) == 0:
            return list(self._slides)
        elif len(args) == 2:
            start_index, count = args
            return list(self._slides[start_index:start_index + count])
        raise ValueError("Unsupported arguments for this method.")























    def add_empty_slide(self, layout) -> ISlide:
        if not hasattr(self, '_slides'):
            raise ValueError("Unsupported arguments for this method.")
        return self._add_empty_slide_internal(layout, index=-1)

    def insert_empty_slide(self, index, layout) -> ISlide:
        if not hasattr(self, '_slides'):
            raise ValueError("Unsupported arguments for this method.")
        return self._add_empty_slide_internal(layout, index=index)

    def _add_empty_slide_internal(self, layout, index: int = -1) -> ISlide:
        """
        Internal implementation for adding/inserting an empty slide.

        Args:
            layout: The layout slide to use for the new slide.
            index: Position to insert at. -1 means append at end.

        Returns:
            The newly created Slide.
        """
        from .Slide import Slide as SlideClass
        from .LayoutSlide import LayoutSlide
        from .ILayoutSlide import ILayoutSlide
        from ._internal.pptx.slide_part import SlidePart
        from ._internal.opc import RelationshipsManager
        from ._internal.opc.relationships import REL_TYPES

        # Validate that layout is actually a LayoutSlide, not a Slide
        if not isinstance(layout, (LayoutSlide, ILayoutSlide)):
            # Check if it has slideLayout in the part name
            if hasattr(layout, '_part_name') and 'slideLayout' not in layout._part_name:
                raise TypeError(
                    f"Expected a LayoutSlide, but got {type(layout).__name__}. "
                    "Use presentation.layout_slides[index] to get a layout slide."
                )

        # Determine the next available slide number in the file system
        next_num = self._get_next_slide_file_number()
        part_name = f'ppt/slides/slide{next_num}.xml'

        # Get the layout's part name
        layout_part_name = layout._part_name

        # Create the empty slide XML + rels + content type
        slide_part = SlidePart.create_empty(self._package, part_name, layout_part_name)

        # Add relationship from presentation to the new slide
        pres_rels = RelationshipsManager(self._package, self._presentation_part.PART_NAME)
        relative_target = 'slides/slide' + str(next_num) + '.xml'
        rel_id = pres_rels.add_relationship(REL_TYPES['slide'], relative_target)
        pres_rels.save()

        # Add slide reference to presentation.xml
        slide_ref = self._presentation_part.add_slide_reference(rel_id, index=index)

        # Create Slide object
        slide = SlideClass()
        slide._init_internal(
            presentation=self._presentation,
            package=self._package,
            part_name=part_name,
            slide_ref=slide_ref,
            slide_part=slide_part,
            layout_resolver=self._layout_resolver,
        )

        # Add to internal list
        if index < 0 or index >= len(self._slides):
            self._slides.append(slide)
        else:
            self._slides.insert(index, slide)

        return slide

    def _get_next_slide_file_number(self) -> int:
        """Find the next available slide file number."""
        existing_nums = set()
        for part_name in self._package.get_part_names():
            m = re.match(r'ppt/slides/slide(\d+)\.xml$', part_name)
            if m:
                existing_nums.add(int(m.group(1)))
        num = 1
        while num in existing_nums:
            num += 1
        return num

    def _clone_slide_internal(
        self,
        source_slide,
        index: int = -1,
        dest_layout=None,
        dest_master=None,
        allow_clone_missing_layout: bool = False
    ) -> ISlide:
        """
        Internal implementation for cloning a slide.

        Args:
            source_slide: The slide to clone.
            index: Position to insert at. -1 means append at end.
            dest_layout: Optional destination layout slide.
            dest_master: Optional destination master slide.
            allow_clone_missing_layout: If True and layout not found, clone
                                        the source layout to destination.

        Returns:
            The cloned Slide.
        """
        from .Slide import Slide as SlideClass
        from ._internal.pptx.slide_part import SlidePart
        from ._internal.opc import RelationshipsManager
        from ._internal.opc.relationships import REL_TYPES

        # Get source package and part name
        source_package = source_slide._package
        source_part_name = source_slide._part_name

        # Determine the next available slide number in destination
        next_num = self._get_next_slide_file_number()
        dest_part_name = f'ppt/slides/slide{next_num}.xml'

        # Determine the layout to use
        dest_layout_part_name = None
        if dest_layout is not None:
            dest_layout_part_name = dest_layout._part_name
        elif dest_master is not None:
            # Find matching layout in destination master
            dest_layout_part_name = self._find_matching_layout(
                source_slide, dest_master, allow_clone_missing_layout
            )
        else:
            # Use source layout if cloning within same presentation
            # or find matching layout in destination
            source_layout = source_slide.layout_slide
            if source_package is self._package:
                # Same presentation - use the same layout
                dest_layout_part_name = source_layout._part_name
            else:
                # Different presentation - clone the master slide chain
                dest_layout_part_name = self._clone_master_chain_for_slide(
                    source_slide, source_layout
                )

        # Clone the slide using SlidePart
        slide_part = SlidePart.clone_from(
            source_package=source_package,
            source_part_name=source_part_name,
            dest_package=self._package,
            dest_part_name=dest_part_name,
            dest_layout_part_name=dest_layout_part_name
        )

        # Add relationship from presentation to the new slide
        pres_rels = RelationshipsManager(self._package, self._presentation_part.PART_NAME)
        relative_target = 'slides/slide' + str(next_num) + '.xml'
        rel_id = pres_rels.add_relationship(REL_TYPES['slide'], relative_target)
        pres_rels.save()

        # Add slide reference to presentation.xml
        slide_ref = self._presentation_part.add_slide_reference(rel_id, index=index)

        # Create Slide object
        slide = SlideClass()
        slide._init_internal(
            presentation=self._presentation,
            package=self._package,
            part_name=dest_part_name,
            slide_ref=slide_ref,
            slide_part=slide_part,
            layout_resolver=self._layout_resolver,
        )

        # Add to internal list
        if index < 0 or index >= len(self._slides):
            self._slides.append(slide)
        else:
            self._slides.insert(index, slide)

        return slide

    def _find_matching_layout(self, source_slide, dest_master, allow_clone: bool) -> Optional[str]:
        """Find a matching layout in the destination master for the source slide."""
        source_layout = source_slide.layout_slide
        source_layout_type = source_layout.layout_type

        # Look for matching layout type in destination master
        for layout in dest_master.layout_slides:
            if layout.layout_type == source_layout_type:
                return layout._part_name

        # Try to match by name if type doesn't match
        source_layout_name = source_layout.name
        for layout in dest_master.layout_slides:
            if layout.name == source_layout_name:
                return layout._part_name

        if allow_clone:
            # Return first layout as fallback
            layouts = list(dest_master.layout_slides)
            if layouts:
                return layouts[0]._part_name

        # Return first layout as default
        layouts = list(dest_master.layout_slides)
        if layouts:
            return layouts[0]._part_name

        return None

    def _find_layout_by_type(self, source_layout) -> Optional[str]:
        """Find a layout in the destination presentation matching the source layout type."""
        try:
            source_type = source_layout.layout_type
        except (AttributeError, NotImplementedError):
            # Layout type not available, use layout_slides instead
            return self._find_layout_from_layout_slides(source_layout)

        # Try using layout_slides property directly
        try:
            if hasattr(self._presentation, 'layout_slides') and self._presentation.layout_slides:
                for layout in self._presentation.layout_slides:
                    try:
                        if layout.layout_type == source_type:
                            return layout._part_name
                    except (AttributeError, NotImplementedError):
                        continue
        except (AttributeError, NotImplementedError):
            pass

        # Fallback: get first available layout
        return self._get_first_layout_part_name()

    def _find_layout_from_layout_slides(self, source_layout) -> Optional[str]:
        """Find matching layout by name using layout_slides."""
        try:
            source_name = source_layout.name
            if hasattr(self._presentation, 'layout_slides') and self._presentation.layout_slides:
                for layout in self._presentation.layout_slides:
                    try:
                        if layout.name == source_name:
                            return layout._part_name
                    except (AttributeError, NotImplementedError):
                        continue
        except (AttributeError, NotImplementedError):
            pass
        return self._get_first_layout_part_name()

    def _get_first_layout_part_name(self) -> Optional[str]:
        """Get the first available layout part name in the destination presentation."""
        # Try using layout_slides property directly
        try:
            if hasattr(self._presentation, 'layout_slides') and self._presentation.layout_slides:
                layouts = list(self._presentation.layout_slides)
                if layouts:
                    return layouts[0]._part_name
        except (AttributeError, NotImplementedError):
            pass

        # Last resort: scan the package for layout files
        for part_name in self._package.get_part_names():
            if part_name.startswith('ppt/slideLayouts/') and part_name.endswith('.xml'):
                return part_name

        return None

    def _clone_master_chain_for_slide(self, source_slide, source_layout) -> Optional[str]:
        """
        Clone the master slide chain for a slide being cloned from another presentation.

        This clones:
        1. The source layout's master slide
        2. All layouts from that master (to maintain the relationship)
        3. Returns the cloned layout's part name matching the source layout

        Args:
            source_slide: The source slide being cloned.
            source_layout: The source slide's layout.

        Returns:
            The cloned layout's part name to use for the new slide.
        """
        # Get the source master
        try:
            source_master = source_layout.master_slide
        except (AttributeError, NotImplementedError):
            # Can't access master, fall back to finding existing layout
            return self._get_first_layout_part_name()

        # Check if we already have a matching master (by comparing themes or backgrounds)
        # For now, always clone the master to ensure styling is preserved
        try:
            cloned_master = self._presentation.masters.add_clone(source_master)
        except Exception as e:
            # If master cloning fails, fall back to existing layout
            return self._get_first_layout_part_name()

        # Find the cloned layout that matches the source layout
        source_layout_type = None
        source_layout_name = None
        try:
            source_layout_type = source_layout.layout_type
        except (AttributeError, NotImplementedError):
            pass
        try:
            source_layout_name = source_layout.name
        except (AttributeError, NotImplementedError):
            pass

        # Search in cloned master's layouts
        for cloned_layout in cloned_master.layout_slides:
            # Try to match by type first
            if source_layout_type is not None:
                try:
                    if cloned_layout.layout_type == source_layout_type:
                        return cloned_layout._part_name
                except (AttributeError, NotImplementedError):
                    pass
            # Try to match by name
            if source_layout_name is not None:
                try:
                    if cloned_layout.name == source_layout_name:
                        return cloned_layout._part_name
                except (AttributeError, NotImplementedError):
                    pass

        # Return first layout from cloned master as fallback
        layouts = list(cloned_master.layout_slides)
        if layouts:
            return layouts[0]._part_name

        return self._get_first_layout_part_name()

    def remove(self, value) -> None:
        if not hasattr(self, '_slides'):
            raise ValueError("Unsupported arguments for this method.")
        idx = self.index_of(value)
        if idx >= 0:
            self.remove_at(idx)

    def remove_at(self, index) -> None:
        if not hasattr(self, '_slides'):
            raise ValueError("Unsupported arguments for this method.")

        from ._internal.pptx.slide_part import SlidePart
        from ._internal.opc import RelationshipsManager

        slide = self._slides[index]
        slide_id = slide.slide_id
        part_name = slide._part_name
        rel_id = slide._slide_ref.rel_id

        # Delete slide parts from the package
        SlidePart.delete(self._package, part_name)

        # Remove the relationship from presentation.xml.rels
        pres_rels = RelationshipsManager(self._package, self._presentation_part.PART_NAME)
        pres_rels.remove_relationship(rel_id)
        pres_rels.save()

        # Remove slide reference from presentation.xml
        self._presentation_part.remove_slide_reference(slide_id)

        # Remove from internal list
        self._slides.pop(index)

    def index_of(self, slide) -> int:
        if not hasattr(self, '_slides'):
            raise ValueError("Unsupported arguments for this method.")
        for i, s in enumerate(self._slides):
            if s.slide_id == slide.slide_id:
                return i
        return -1

    def __getitem__(self, index: int) -> Slide:
        if hasattr(self, '_slides'):
            return self._slides[index]
        raise ValueError("Unsupported arguments for this method.")

    def __len__(self) -> int:
        if hasattr(self, '_slides'):
            return len(self._slides)
        raise ValueError("Unsupported arguments for this method.")

    def __iter__(self):
        if hasattr(self, '_slides'):
            return iter(self._slides)
        raise ValueError("Unsupported arguments for this method.")

