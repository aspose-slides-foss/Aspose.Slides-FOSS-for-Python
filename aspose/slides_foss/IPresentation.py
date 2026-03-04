from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IAudioCollection import IAudioCollection
    from .IBaseSlide import IBaseSlide
    from .ICommentAuthorCollection import ICommentAuthorCollection
    from .ICustomData import ICustomData
    from .ICustomXmlPart import ICustomXmlPart
    from .IDigitalSignatureCollection import IDigitalSignatureCollection
    from .IDocumentProperties import IDocumentProperties
    from .IFontsManager import IFontsManager
    from .IGlobalLayoutSlideCollection import IGlobalLayoutSlideCollection
    from .IHyperlinkQueries import IHyperlinkQueries
    from .IImage import IImage
    from .IImageCollection import IImageCollection
    from .IMasterHandoutSlideManager import IMasterHandoutSlideManager
    from .IMasterNotesSlideManager import IMasterNotesSlideManager
    from .IMasterSlideCollection import IMasterSlideCollection
    from .theme.IMasterTheme import IMasterTheme
    from .INotesSize import INotesSize
    from .IPresentationHeaderFooterManager import IPresentationHeaderFooterManager
    from .IProtectionManager import IProtectionManager
    from .ISectionCollection import ISectionCollection
    from .ISensitivityLabelCollection import ISensitivityLabelCollection
    from .ISlideCollection import ISlideCollection
    from .ISlideSize import ISlideSize
    from .ITextStyle import ITextStyle
    from .vba.IVbaProject import IVbaProject
    from .IVideoCollection import IVideoCollection
    from .IViewProperties import IViewProperties
    from .SourceFormat import SourceFormat

class IPresentation(IPresentationComponent, ABC):
    """Presentation document"""
    @property
    def current_date_time(self) -> Any:
        """Returns or sets date and time which will substitute content of datetime fields. Time of this Presentation object creation by default. Read/write ."""
        ...

    @current_date_time.setter
    def current_date_time(self, value: Any):
        ...



    @property
    def slides(self) -> ISlideCollection:
        """Returns a list of all slides that are defined in the presentation. Read-only ."""
        ...



    @property
    def notes_size(self) -> INotesSize:
        """Returns notes slide size object. Read-only ."""
        ...

    @property
    def layout_slides(self) -> IGlobalLayoutSlideCollection:
        """Returns a list of all layout slides that are defined in the presentation. Read-only ."""
        ...

    @property
    def masters(self) -> IMasterSlideCollection:
        """Returns a list of all master slides that are defined in the presentation. Read-only ."""
        ...





    @property
    def comment_authors(self) -> ICommentAuthorCollection:
        """Returns the collection of comments autors. Read-only ."""
        ...

    @property
    def document_properties(self) -> IDocumentProperties:
        """Returns DocumentProperties object which contains standard and custom document properties. Read-only ."""
        ...

    @property
    def images(self) -> IImageCollection:
        """Returns the collection of all images in the presentation. Read-only ."""
        ...






    @property
    def source_format(self) -> SourceFormat:
        """Returns information about from which format presentation was loaded. Read-only ."""
        ...




    @property
    def first_slide_number(self) -> int:
        """Represents the first slide number in the presentation. Read/write ."""
        ...

    @first_slide_number.setter
    def first_slide_number(self, value: int):
        ...





    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        """Allows to get base IPresentationComponent interface. Read-only ."""
        ...

    @overload
    def save(self, fname, format) -> None:
        ...

    @overload
    def save(self, stream, format) -> None:
        ...

    @overload
    def save(self, fname, format, options) -> None:
        ...

    @overload
    def save(self, stream, format, options) -> None:
        ...

    @overload
    def save(self, fname, slides, format) -> None:
        ...

    @overload
    def save(self, fname, slides, format, options) -> None:
        ...

    @overload
    def save(self, stream, slides, format) -> None:
        ...

    @overload
    def save(self, stream, slides, format, options) -> None:
        ...

    @overload
    def save(self, options) -> None:
        ...

















