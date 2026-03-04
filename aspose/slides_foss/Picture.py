from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .ISlidesPicture import ISlidesPicture
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from ._internal.pptx.constants import NS, Attributes

if TYPE_CHECKING:
    from .IBaseSlide import IBaseSlide
    from .effects.IImageTransformOperationCollection import IImageTransformOperationCollection
    from .IPPImage import IPPImage
    from .IPresentation import IPresentation
    from ._internal.pptx.slide_part import SlidePart

class Picture(ISlidesPicture, ISlideComponent, IPresentationComponent):
    """Represents a picture in a presentation."""

    def _init_internal(self, blip_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        """
        Internal initialization with the a:blip XML element.

        Args:
            blip_element: The a:blip element containing r:embed reference.
            slide_part: The SlidePart for relationship resolution.
            parent_slide: The parent Slide object.
        """
        self._blip = blip_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        """Allows to get base IPresentationComponent interface. Read-only ."""
        return self

    @property
    def image(self) -> IPPImage:
        """Returns or sets the embedded image. Read/write ."""
        if not hasattr(self, '_blip'):
            raise NotImplementedError("This feature is not yet available in this version.")
        embed_id = self._blip.get(Attributes.R_EMBED)
        if embed_id is None:
            return None
        # Resolve relationship to part name
        rel = self._slide_part._rels_manager.get_relationship(embed_id)
        if rel is None:
            raise NotImplementedError("This feature is not yet available in this version.")
        part_name = self._slide_part._resolve_target(rel.target)
        # Find the PPImage in the presentation's images collection
        presentation = self._parent_slide.presentation
        for pp_image in presentation.images:
            if hasattr(pp_image, '_part_name') and pp_image._part_name == part_name:
                return pp_image
        raise NotImplementedError("This feature is not yet available in this version.")

    @image.setter
    def image(self, value: IPPImage):
        if not hasattr(self, '_blip'):
            raise NotImplementedError("This feature is not yet available in this version.")
        # value should be a PPImage with a _part_name
        if not hasattr(value, '_part_name'):
            raise ValueError("Image must be a PPImage from the presentation's image collection")
        if self._slide_part is None:
            # No slide part yet (standalone paragraph) — mark blip with pending part name.
            # This temporary attribute will be resolved when the paragraph is added to a slide.
            self._blip.set('_pendingPartName', value._part_name)
            return
        _set_blip_image(self._blip, self._slide_part, value)

    @property
    def link_path_long(self) -> str:
        """Returns of sets linked image's URL. Read/write ."""
        if not hasattr(self, '_blip'):
            raise NotImplementedError("This feature is not yet available in this version.")
        link_id = self._blip.get(f'{NS.R}link')
        if link_id is None:
            return ''
        rel = self._slide_part._rels_manager.get_relationship(link_id)
        if rel is None:
            return ''
        return rel.target

    @link_path_long.setter
    def link_path_long(self, value: str):
        if not hasattr(self, '_blip'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ._internal.opc.relationships import REL_TYPES
        existing_link_id = self._blip.get(f'{NS.R}link')
        if existing_link_id:
            self._slide_part._rels_manager.remove_relationship(existing_link_id)
        if value:
            link_id = self._slide_part._rels_manager.add_relationship(
                REL_TYPES['hyperlink'], value, target_mode='External'
            )
            self._blip.set(f'{NS.R}link', link_id)
            self._slide_part._rels_manager.save()
        else:
            if f'{NS.R}link' in self._blip.attrib:
                del self._blip.attrib[f'{NS.R}link']


    @property
    def presentation(self) -> IPresentation:
        """Returns the presentation. Read-only ."""
        if not hasattr(self, '_parent_slide'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return self._parent_slide.presentation

    @property
    def slide(self) -> IBaseSlide:
        """Returns the parent slide of a picture. Read-only ."""
        if not hasattr(self, '_parent_slide'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return self._parent_slide

    @property
    def as_i_slide_component(self) -> ISlideComponent:
        return self


def _compute_relative_path(from_dir: str, to_path: str) -> str:
    """Compute a relative path from from_dir to to_path."""
    from_parts = from_dir.split('/')
    to_parts = to_path.split('/')
    # Find common prefix
    common = 0
    for i in range(min(len(from_parts), len(to_parts))):
        if from_parts[i] == to_parts[i]:
            common += 1
        else:
            break
    # Build relative path
    up = len(from_parts) - common
    remaining = to_parts[common:]
    return '/'.join(['..'] * up + remaining)


def _set_blip_image(blip, slide_part, pp_image) -> None:
    """Set image relationship on a blip element."""
    slide_dir = slide_part._part_name.rsplit('/', 1)[0]
    image_path = pp_image._part_name
    relative_target = _compute_relative_path(slide_dir, image_path)
    from ._internal.opc.relationships import REL_TYPES
    existing_rels = slide_part._rels_manager.get_relationships_by_type(REL_TYPES['image'])
    embed_id = None
    for rel in existing_rels:
        resolved = slide_part._resolve_target(rel.target)
        if resolved == image_path:
            embed_id = rel.id
            break
    if embed_id is None:
        embed_id = slide_part._rels_manager.add_relationship(
            REL_TYPES['image'], relative_target
        )
        slide_part._rels_manager.save()
    blip.set(Attributes.R_EMBED, embed_id)
    slide_part.save()


def flush_pending_blip_images(element, slide_part, parent_slide) -> None:
    """Resolve any pending image references on blip elements within the XML tree."""
    from ._internal.pptx.constants import NS as _NS
    for blip in element.iter(f'{_NS.A}blip'):
        pending_part = blip.get('_pendingPartName')
        if pending_part is not None:
            del blip.attrib['_pendingPartName']
            presentation = parent_slide.presentation
            for pp_image in presentation.images:
                if hasattr(pp_image, '_part_name') and pp_image._part_name == pending_part:
                    _set_blip_image(blip, slide_part, pp_image)
                    break
