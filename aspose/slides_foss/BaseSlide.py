from __future__ import annotations
from typing import overload, TYPE_CHECKING, Optional
from .IBaseSlide import IBaseSlide
from .theme.IThemeable import IThemeable
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IAnimationTimeLine import IAnimationTimeLine
    from .IBackground import IBackground
    from .IPresentation import IPresentation
    from .IShape import IShape
    from .IShapeCollection import IShapeCollection
    from .ISlideShowTransition import ISlideShowTransition

class BaseSlide(IBaseSlide, IThemeable, ISlideComponent, IPresentationComponent):
    """Represents common data for all slide types."""

    def __init__(self):
        """Initialize base slide."""
        self._shapes_collection: Optional[IShapeCollection] = None
        self._slide_show_transition_cache = None
        self._background_cache = None

    def _get_slide_part(self):
        """
        Get the slide part object for this slide.

        This method should be overridden by subclasses to return the appropriate
        part object (SlidePart, LayoutSlidePart, or MasterSlidePart).
        """
        # Try different attributes that might exist in subclasses
        if hasattr(self, '_slide_part'):
            return self._slide_part
        elif hasattr(self, '_layout_part'):
            return self._layout_part
        elif hasattr(self, '_master_part'):
            return self._master_part
        return None

    @property
    def shapes(self) -> IShapeCollection:
        """Returns the shapes of a slide. Read-only ."""
        if self._shapes_collection is None:
            from .ShapeCollection import ShapeCollection
            slide_part = self._get_slide_part()
            if slide_part is not None:
                collection = ShapeCollection()
                collection._init_internal(slide_part, self)
                self._shapes_collection = collection
        return self._shapes_collection


    @property
    def name(self) -> str:
        """Returns or sets the name of a slide. Read/write ."""
        slide_part = self._get_slide_part()
        if slide_part is not None:
            return slide_part.name
        return ''

    @name.setter
    def name(self, value: str):
        slide_part = self._get_slide_part()
        if slide_part is not None:
            slide_part.name = value

    @property
    def slide_id(self) -> int:
        """Returns the ID of a slide. Read-only ."""
        # Special case for Slide which uses _slide_ref.slide_id
        if hasattr(self, '_slide_ref') and self._slide_ref is not None:
            return self._slide_ref.slide_id
        # For LayoutSlide and MasterSlide, extract from _part_name
        elif hasattr(self, '_part_name') and self._part_name is not None:
            import re
            m = re.search(r'(\d+)', self._part_name.rsplit('/', 1)[-1])
            if m:
                return int(m.group(1))
        return 0








    @property
    def background(self) -> IBackground:
        """Returns slide's background. Read-only."""
        if self._background_cache is None:
            from .Background import Background
            slide_part = self._get_slide_part()
            if slide_part is not None:
                bg = Background()
                bg._init_internal(slide_part, self)
                self._background_cache = bg
        return self._background_cache

    @property
    def slide_show_transition(self) -> ISlideShowTransition:
        """Returns the TransitionEx object which contains information about how the specified slide advances during a slide show. Read-only ."""
        if self._slide_show_transition_cache is None:
            from .slideshow.SlideShowTransition import SlideShowTransition
            slide_part = self._get_slide_part()
            if slide_part is not None:
                obj = SlideShowTransition()
                obj._init_internal(slide_part)
                self._slide_show_transition_cache = obj
        return self._slide_show_transition_cache

    @property
    def timeline(self) -> IAnimationTimeLine:
        """Returns animation timeline object. Read-only."""
        if not hasattr(self, '_timeline_cache') or self._timeline_cache is None:
            from .animation.AnimationTimeLine import AnimationTimeLine
            slide_part = self._get_slide_part()
            if slide_part is not None:
                tl = AnimationTimeLine()
                tl._init_internal(slide_part, self)
                self._timeline_cache = tl
        return getattr(self, '_timeline_cache', None)

    @property
    def presentation(self) -> IPresentation:
        """Returns IPresentation interface. Read-only ."""
        if hasattr(self, '_presentation_ref') and self._presentation_ref is not None:
            return self._presentation_ref
        return None

    @property
    def slide(self) -> IBaseSlide:
        """Returns the parent slide. Read-only."""
        return self

    @property
    def as_i_slide_component(self) -> ISlideComponent:
        return self

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self

    @property
    def as_i_themeable(self) -> IThemeable:
        return self











