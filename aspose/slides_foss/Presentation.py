from __future__ import annotations
from datetime import datetime
from typing import overload, TYPE_CHECKING, Any, BinaryIO, Optional, Union
from .IPresentation import IPresentation
from .IPresentationComponent import IPresentationComponent
from .ILoadOptions import ILoadOptions
from .SourceFormat import SourceFormat
from .export.SaveFormat import SaveFormat

# Internal imports
from ._internal.opc import OpcPackage
from ._internal.pptx import PresentationPart
from ._internal.pptx.template import create_minimal_pptx
from ._internal.export import ExporterRegistry

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
    from .SlideShowSettings import SlideShowSettings


class Presentation(IPresentation, IPresentationComponent):
    """Represents a Microsoft PowerPoint presentation."""






    def __init__(self, *args, **kwargs):
        """
        Initialize a Presentation.

        Overloads:
        - Presentation(): Create a new empty presentation
        - Presentation(load_options): Create new presentation with load options
        - Presentation(stream): Load from a binary stream
        - Presentation(stream, load_options): Load from stream with options
        - Presentation(file): Load from a file path
        - Presentation(file, load_options): Load from file with options
        """
        self._opc_package: Optional[OpcPackage] = None
        self._presentation_part: Optional[PresentationPart] = None
        self._source_format: SourceFormat = SourceFormat.PPTX
        self._current_date_time: datetime = datetime.now()
        self._first_slide_number: int = 1
        self._load_options: Optional[ILoadOptions] = None
        self._slides = None
        self._layout_slides_collection = None
        self._master_slides_map: Optional[dict] = None
        self._layout_slides_map: Optional[dict] = None
        self._document_properties = None
        self._comment_authors = None

        # Parse arguments to determine which overload was called
        source: Optional[Union[str, BinaryIO]] = None
        load_options: Optional[ILoadOptions] = None

        if len(args) == 0:
            # Presentation() - create new empty presentation
            pass
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, ILoadOptions):
                # Presentation(load_options)
                load_options = arg
            elif isinstance(arg, str):
                # Presentation(file)
                source = arg
            elif hasattr(arg, 'read'):
                # Presentation(stream)
                source = arg
            else:
                raise TypeError(f"Unsupported argument type: {type(arg)}")
        elif len(args) == 2:
            arg1, arg2 = args
            if isinstance(arg2, ILoadOptions):
                load_options = arg2
            if isinstance(arg1, str):
                # Presentation(file, load_options)
                source = arg1
            elif hasattr(arg1, 'read'):
                # Presentation(stream, load_options)
                source = arg1
            else:
                raise TypeError(f"Unsupported argument type: {type(arg1)}")
        else:
            raise TypeError(f"Presentation() takes at most 2 arguments ({len(args)} given)")

        self._load_options = load_options

        # Initialize the presentation
        if source is None:
            # Create new empty presentation
            self._opc_package = OpcPackage.create_new()
            create_minimal_pptx(self._opc_package)
        elif isinstance(source, str):
            # Load from file path
            self._opc_package = OpcPackage.open(source)
            self._detect_source_format(source)
        else:
            # Load from stream
            self._opc_package = OpcPackage.open(source)

        # Parse the presentation.xml part
        self._presentation_part = PresentationPart(self._opc_package)

        # Get first slide number from presentation.xml
        self._first_slide_number = self._presentation_part.get_first_slide_number()

    def _detect_source_format(self, path: str) -> None:
        """Detect source format from file extension."""
        lower_path = path.lower()
        if lower_path.endswith('.pptx') or lower_path.endswith('.pptm') or \
           lower_path.endswith('.ppsx') or lower_path.endswith('.potx'):
            self._source_format = SourceFormat.PPTX
        elif lower_path.endswith('.ppt'):
            self._source_format = SourceFormat.PPT
        elif lower_path.endswith('.odp'):
            self._source_format = SourceFormat.ODP

    @property
    def current_date_time(self) -> Any:
        """Returns or sets date and time which will substitute content of datetime fields. Time of this Presentation object creation by default. Read/write ."""
        return self._current_date_time

    @current_date_time.setter
    def current_date_time(self, value: Any):
        self._current_date_time = value



    @property
    def slides(self) -> ISlideCollection:
        """Returns a list of all slides that are defined in the presentation. Read-only ."""
        if self._slides is None:
            self._ensure_layout_slides_parsed()
            from .SlideCollection import SlideCollection
            self._slides = SlideCollection()
            self._slides._init_internal(
                presentation=self,
                package=self._opc_package,
                presentation_part=self._presentation_part,
                layout_resolver=self._resolve_layout_slide,
            )
        return self._slides



    @property
    def notes_size(self) -> INotesSize:
        """Returns notes slide size object. Read-only."""
        if not hasattr(self, '_notes_size') or self._notes_size is None:
            from .NotesSize import NotesSize
            self._notes_size = NotesSize()
            self._notes_size._init_internal(self._presentation_part)
        return self._notes_size

    @property
    def layout_slides(self) -> IGlobalLayoutSlideCollection:
        """Returns a list of all layout slides that are defined in the presentation. Read-only ."""
        if self._layout_slides_collection is None:
            self._ensure_layout_slides_parsed()
            from .GlobalLayoutSlideCollection import GlobalLayoutSlideCollection
            all_layouts = list(self._layout_slides_map.values())
            self._layout_slides_collection = GlobalLayoutSlideCollection()
            self._layout_slides_collection._init_internal(all_layouts)
        return self._layout_slides_collection

    @property
    def masters(self) -> IMasterSlideCollection:
        """Returns a list of all master slides that are defined in the presentation. Read-only ."""
        self._ensure_layout_slides_parsed()
        if not hasattr(self, '_masters_collection') or self._masters_collection is None:
            from .MasterSlideCollection import MasterSlideCollection
            self._masters_collection = MasterSlideCollection()
            self._masters_collection._init_internal(
                presentation=self,
                package=self._opc_package,
                presentation_part=self._presentation_part,
                master_slides=list(self._master_slides_map.values()),
            )
        return self._masters_collection





    @property
    def comment_authors(self) -> ICommentAuthorCollection:
        """Returns the collection of comment authors. Read-only."""
        if self._comment_authors is None:
            from ._internal.pptx.comment_authors_part import CommentAuthorsPart
            from .CommentAuthorCollection import CommentAuthorCollection
            authors_part = CommentAuthorsPart(self._opc_package)
            col = CommentAuthorCollection()
            col._init_internal(authors_part, self._opc_package, self)
            self._comment_authors = col
        return self._comment_authors

    @property
    def document_properties(self) -> IDocumentProperties:
        """Returns DocumentProperties object which contains standard and custom document properties. Read-only ."""
        if self._document_properties is None:
            from .DocumentProperties import DocumentProperties
            self._document_properties = DocumentProperties()
            self._document_properties._init_internal(self._opc_package, self)
        return self._document_properties

    @property
    def images(self) -> IImageCollection:
        """Returns the collection of all images in the presentation. Read-only ."""
        if not hasattr(self, '_images') or self._images is None:
            from .ImageCollection import ImageCollection
            self._images = ImageCollection()
            self._images._init_internal(self._opc_package)
        return self._images











    @property
    def first_slide_number(self) -> int:
        """Represents the first slide number in the presentation"""
        return self._first_slide_number

    @first_slide_number.setter
    def first_slide_number(self, value: int):
        self._first_slide_number = value
        if self._presentation_part:
            self._presentation_part.set_first_slide_number(value)


    @property
    def source_format(self) -> SourceFormat:
        """Returns information about from which format presentation was loaded. Read-only ."""
        return self._source_format



    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self

    @property
    def presentation(self) -> IPresentation:
        return self

    def _ensure_layout_slides_parsed(self) -> None:
        """Parse all master slides and layout slides from the package on first access."""
        if self._layout_slides_map is not None:
            return

        from ._internal.pptx.master_slide_part import MasterSlidePart
        from ._internal.pptx.layout_slide_part import LayoutSlidePart
        from ._internal.opc import RelationshipsManager
        from .MasterSlide import MasterSlide
        from .LayoutSlide import LayoutSlide

        self._master_slides_map = {}
        self._layout_slides_map = {}

        # Resolve presentation relationships
        pres_rels = RelationshipsManager(self._opc_package, PresentationPart.PART_NAME)

        # Parse master slides
        for master_ref in self._presentation_part.master_references:
            rel = pres_rels.get_relationship(master_ref.rel_id)
            if rel is None:
                continue

            target = rel.target
            if target.startswith('/'):
                master_part_name = target.lstrip('/')
            else:
                master_part_name = 'ppt/' + target

            master_part = MasterSlidePart(self._opc_package, master_part_name)

            # Parse layout slides for this master
            master_layouts = []
            for layout_part_name in master_part.layout_part_names:
                if layout_part_name in self._layout_slides_map:
                    master_layouts.append(self._layout_slides_map[layout_part_name])
                    continue

                layout_part = LayoutSlidePart(self._opc_package, layout_part_name)
                layout_slide = LayoutSlide()
                layout_slide._init_internal(
                    presentation=self,
                    package=self._opc_package,
                    part_name=layout_part_name,
                    layout_part=layout_part,
                    master_resolver=self._resolve_master_slide,
                )
                self._layout_slides_map[layout_part_name] = layout_slide
                master_layouts.append(layout_slide)

            # Create master slide object
            master_slide = MasterSlide()
            master_slide._init_internal(
                presentation=self,
                package=self._opc_package,
                part_name=master_part_name,
                master_part=master_part,
                layout_slides=master_layouts,
            )
            self._master_slides_map[master_part_name] = master_slide

    def _resolve_layout_slide(self, part_name: str):
        """Resolve a layout slide part name to a LayoutSlide object."""
        self._ensure_layout_slides_parsed()
        return self._layout_slides_map.get(part_name)

    def _resolve_master_slide(self, part_name: str):
        """Resolve a master slide part name to a MasterSlide object."""
        self._ensure_layout_slides_parsed()
        return self._master_slides_map.get(part_name)










    def save(self, *args, **kwargs) -> None:
        """
        Save the presentation to a file or stream.

        Overloads:
        - save(fname, format): Save to file with specified format
        - save(stream, format): Save to stream with specified format
        - save(fname, format, options): Save to file with format and options
        - save(stream, format, options): Save to stream with format and options
        - save(options): Save using options (which contain output settings)
        - save(fname, slides, format): Save specific slides to file
        - save(fname, slides, format, options): Save specific slides with options
        - save(stream, slides, format): Save specific slides to stream
        - save(stream, slides, format, options): Save specific slides with options
        """
        # Save document properties (auto-update last_saved_time)
        if self._document_properties is not None:
            self._document_properties.last_saved_time = datetime.utcnow()
            self._document_properties._save()

        # Save all modified slide parts and their associated notes slides
        if self._slides is not None:
            for slide in self._slides:
                if hasattr(slide, '_slide_part') and slide._slide_part is not None:
                    slide._slide_part.save()
                # Save notes slide if it was loaded or created
                if hasattr(slide, '_notes_slide_manager_cache') and \
                        slide._notes_slide_manager_cache is not None:
                    mgr = slide._notes_slide_manager_cache
                    cached = getattr(mgr, '_notes_slide_cache', None)
                    if cached is not None:
                        notes_part = getattr(cached, '_notes_part', None)
                        if notes_part is not None:
                            notes_part.save()

        # Save comment authors if they were loaded/modified
        if self._comment_authors is not None:
            from ._internal.pptx.comment_authors_part import CommentAuthorsPart
            authors_part = self._comment_authors._authors_part
            authors_part.save()
            CommentAuthorsPart.ensure_registered(self._opc_package)
            # Save comments parts for all slides that have comments
            from ._internal.pptx.comments_part import CommentsPart
            for part_name in list(self._opc_package.get_part_names()):
                if part_name.startswith('ppt/comments/') and part_name.endswith('.xml'):
                    cp = CommentsPart(self._opc_package, part_name)
                    cp.save()

        # Update the presentation.xml part before saving
        if self._presentation_part:
            self._presentation_part.save()

        # Parse arguments to determine which overload was called
        destination: Optional[Union[str, BinaryIO]] = None
        save_format: Optional[SaveFormat] = None
        options: Optional[Any] = None
        slides: Optional[list] = None

        if len(args) == 1:
            # save(options)
            options = args[0]
            # TODO: Extract destination and format from options
            raise NotImplementedError("save(options) overload not yet implemented")
        elif len(args) == 2:
            # save(fname/stream, format)
            destination = args[0]
            save_format = args[1]
        elif len(args) == 3:
            arg0, arg1, arg2 = args
            if isinstance(arg2, SaveFormat):
                # save(fname/stream, slides, format)
                destination = arg0
                slides = arg1
                save_format = arg2
            else:
                # save(fname/stream, format, options)
                destination = arg0
                save_format = arg1
                options = arg2
        elif len(args) == 4:
            # save(fname/stream, slides, format, options)
            destination = args[0]
            slides = args[1]
            save_format = args[2]
            options = args[3]
        else:
            raise TypeError(f"save() takes 1-4 arguments ({len(args)} given)")

        # Get the format value string from the enum
        if save_format is None:
            raise ValueError("Save format is required")

        format_value = save_format.value

        # Get the appropriate exporter from the registry
        exporter = ExporterRegistry.get_exporter(format_value)
        if exporter is None:
            raise NotImplementedError(f"Export format '{format_value}' is not supported")

        # TODO: Handle slides parameter for partial export
        if slides is not None:
            raise NotImplementedError("Saving specific slides is not yet implemented")

        # Perform the export
        exporter.export(self._opc_package, destination, options)
















    def dispose(self) -> None:
        """Release all resources used by this Presentation object."""
        if self._opc_package is not None:
            self._opc_package.close()
            self._opc_package = None
        self._presentation_part = None
        self._slides = None
        self._layout_slides_collection = None
        self._master_slides_map = None
        self._layout_slides_map = None
        self._document_properties = None
        self._comment_authors = None

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager and dispose resources."""
        self.dispose()
        return False

