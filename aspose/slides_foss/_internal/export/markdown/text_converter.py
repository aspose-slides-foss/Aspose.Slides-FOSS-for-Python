"""Converting text to markdown by the chosen specification."""

from __future__ import annotations

from . import constants
from .settings import Feature, MarkdownConverterSettings
from .text_escaper import escape_markdown_text_if_needed

# Placeholder <p:ph> type attribute values that are rendered as headers.
PH_TITLE = 'title'
PH_CENTERED_TITLE = 'ctrTitle'
PH_SUBTITLE = 'subTitle'
PH_FOOTER = 'ftr'
PH_HEADER = 'hdr'
PH_BODY = 'body'


class MarkdownTextConverter:
    """Model for converting presentation to markdown by most popular specification."""

    def __init__(self, flavor, new_line_type, skip_java_script_links, handle_repeated_spaces):
        self.settings = MarkdownConverterSettings(
            flavor, new_line_type, skip_java_script_links, handle_repeated_spaces)

    def add_spaces_to_string(self, text, add_to_start_number, add_to_end_number):
        return '{0}{1}{2}'.format(' ' * add_to_start_number, text, ' ' * add_to_end_number)

    def convert_text_to_bold(self, text):
        return constants.BOLD_TEXT.format(text)

    def convert_text_to_head(self, text, pixels):
        if pixels <= 0:
            return text

        if pixels > 36:
            level = 1
        else:
            level = 6 - int(pixels / 6)

        return self.convert_text_with_font_size_level(text, level)

    def convert_text_to_italic(self, text):
        return self.settings.italic_format.format(text)

    def convert_text_to_ordered_list(self, text, depth):
        return self._convert_text_to_list_text(
            self.settings.ordered_list_format, text, self.settings.ordered_list_char, depth)

    def convert_text_to_strikethrough(self, text):
        return self.settings.strikethrough_format.format(text)

    def convert_text_to_text_with_new_line(self, text):
        return constants.ELEMENT_END.format(text if text is not None else '', self.settings.new_string_text)

    def convert_text_to_underlined(self, text):
        return self.settings.underlined_format.format(text)

    def convert_text_to_unordered_list(self, text, depth):
        return self._convert_text_to_list_text(
            self.settings.unordered_list_format, text, self.settings.unordered_list_char, depth)

    def convert_text_with_font_size_level(self, text, level):
        # https://www.markdownguide.org/basic-syntax/#headings
        header_string = self.settings.header_char * level
        return constants.HEADER_TEXT.format(header_string, text)

    def convert_text_with_new_lines_between_it(self, text):
        return constants.ELEMENT_WITH_NEW_LINES_BETWEEN_IT.format(text, self.settings.new_string_text)

    def get_char_to_ignore_reserved_chars(self):
        return self.settings.ignore_reserved_char

    def convert_comment_text(self, author, comment):
        return constants.COMMENT_TEXT.format(author, comment)

    def feature_is_enabled(self, feature):
        return (self.settings.disabled_features & feature) == 0

    def get_new_line(self):
        return self.settings.new_string_text

    def ignore_reserved_chars(self, text):
        return escape_markdown_text_if_needed(text, self.get_char_to_ignore_reserved_chars())

    def set_text_font_height(self, text, placeholder_type):
        """Sets text height depending on the type of placeholder.

        Returns a (text, is_header) tuple.
        """
        if placeholder_type in (PH_TITLE, PH_CENTERED_TITLE):
            return self.convert_text_to_head(text, constants.TITLE_HEIGHT), True
        if placeholder_type == PH_SUBTITLE:
            return self.convert_text_to_head(text, constants.SUB_TITLE_HEIGHT), True
        if placeholder_type in (PH_FOOTER, PH_HEADER):
            return self.convert_text_to_head(text, constants.HEADER_HEIGHT), True
        return text, False

    def _convert_text_to_list_text(self, fmt, text, char_for_nested_list, depth):
        tabulation_char = char_for_nested_list * (depth * self.settings.list_char_times_for_level)
        return fmt.format(tabulation_char, text)
