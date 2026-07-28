from __future__ import annotations
from typing import TYPE_CHECKING
from .SaveOptions import SaveOptions
from .ISaveOptions import ISaveOptions
from .Flavor import Flavor
from .HandleRepeatedSpaces import HandleRepeatedSpaces
from .MarkdownExportType import MarkdownExportType
from .NewLineType import NewLineType

class MarkdownSaveOptions(SaveOptions, ISaveOptions):
    """Represents options that control how presentation should be saved to markdown."""

    def __init__(self):
        self._export_type = MarkdownExportType.TEXT_ONLY
        self._new_line_type = NewLineType.WINDOWS
        self._show_comments = False
        self._show_hidden_slides = False
        self._show_slide_number = False
        self._flavor = Flavor.DEFAULT
        self._slide_number_format = '# {0}'
        self._handle_repeated_spaces = HandleRepeatedSpaces.ALTERNATE_SPACES_TO_NBSP
        self._remove_empty_lines = False

    @property
    def export_type(self) -> MarkdownExportType:
        """Specifies markdown specification to convert presentation. Default is TextOnly."""
        return self._export_type

    @export_type.setter
    def export_type(self, value: MarkdownExportType):
        self._export_type = value

    @property
    def new_line_type(self) -> NewLineType:
        """Specifies whether the generated document should have new lines \\r(Macintosh) of \\n(Unix) or \\r\\n(Windows). Default is Unix."""
        return self._new_line_type

    @new_line_type.setter
    def new_line_type(self, value: NewLineType):
        self._new_line_type = value

    @property
    def show_comments(self) -> bool:
        """Specifies whether the generated document should show comments or not. Default is false."""
        return self._show_comments

    @show_comments.setter
    def show_comments(self, value: bool):
        self._show_comments = value

    @property
    def show_hidden_slides(self) -> bool:
        """Specifies whether the generated document should include hidden slides or not. Default is false."""
        return self._show_hidden_slides

    @show_hidden_slides.setter
    def show_hidden_slides(self, value: bool):
        self._show_hidden_slides = value

    @property
    def show_slide_number(self) -> bool:
        """Specifies whether the generated document should show number of each slide or not. Default is false."""
        return self._show_slide_number

    @show_slide_number.setter
    def show_slide_number(self, value: bool):
        self._show_slide_number = value

    @property
    def flavor(self) -> Flavor:
        """Specifies markdown specification to convert presentation. Default is Multi-markdown."""
        return self._flavor

    @flavor.setter
    def flavor(self, value: Flavor):
        self._flavor = value

    @property
    def slide_number_format(self) -> str:
        """Gets or sets the format string used for slide number headers in Markdown output. The format must include the "{0}" placeholder, which will be replaced with the slide index during export. Example: "# Slide {0}" will produce "# Slide 1", "# Slide 2", etc."""
        return self._slide_number_format

    @slide_number_format.setter
    def slide_number_format(self, value: str):
        if not value:
            raise ValueError("Slide number format cannot be null or empty.")
        if '{0}' not in value:
            raise ValueError('Slide number format must contain the "{0}" placeholder, e.g., "# Slide {0}".')
        self._slide_number_format = value

    @property
    def handle_repeated_spaces(self) -> HandleRepeatedSpaces:
        """Specifies how repeated regular space characters should be handled during Markdown export. Default is AlternateSpacesToNbsp."""
        return self._handle_repeated_spaces

    @handle_repeated_spaces.setter
    def handle_repeated_spaces(self, value: HandleRepeatedSpaces):
        self._handle_repeated_spaces = value

    @property
    def remove_empty_lines(self) -> bool:
        """If set to true, removes empty or whitespace-only lines from the final Markdown output. Default is false."""
        return self._remove_empty_lines

    @remove_empty_lines.setter
    def remove_empty_lines(self, value: bool):
        self._remove_empty_lines = value
