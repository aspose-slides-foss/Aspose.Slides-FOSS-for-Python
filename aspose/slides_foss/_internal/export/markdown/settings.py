"""Per-flavor markdown converter settings."""

from __future__ import annotations
from enum import IntFlag

from ....export.Flavor import Flavor
from ....export.HandleRepeatedSpaces import HandleRepeatedSpaces
from ....export.NewLineType import NewLineType
from . import constants


class Feature(IntFlag):
    """All markdown features used in program."""
    TABLE = 1
    STRIKETHROUGH = 2
    MATH_SUPERSCRIPT = 4
    MATH_SUBSCRIPT = 8
    UNDERLINE = 16


_NO_TABLE_FLAVORS = frozenset([
    Flavor.COMMON_MARK, Flavor.GHOST, Flavor.GRUBER, Flavor.REMARKABLE,
    Flavor.S9E_TEXT_FORMATTER, Flavor.SCHOLARLY_MARKDOWN, Flavor.TRELLO,
])

_NO_MATH_SUBSCRIPT_FLAVORS = frozenset([
    Flavor.COMMON_MARK, Flavor.GITHUB, Flavor.GIT_LAB, Flavor.GRUBER,
    Flavor.HAROOPAD, Flavor.IA_WRITER, Flavor.KRAMDOWN, Flavor.MARKDOWN2,
    Flavor.MARKDOWN_EXTRA, Flavor.MARUKU, Flavor.REDCARPET,
    Flavor.SCHOLARLY_MARKDOWN, Flavor.SHOWDOWN, Flavor.STACK_OVERFLOW,
    Flavor.TAIGA, Flavor.TRELLO,
])

_NO_MATH_SUPERSCRIPT_FLAVORS = frozenset([
    Flavor.COMMON_MARK, Flavor.GITHUB, Flavor.GIT_LAB, Flavor.GRUBER,
    Flavor.HAROOPAD, Flavor.IA_WRITER, Flavor.KRAMDOWN, Flavor.MARKDOWN_EXTRA,
    Flavor.MARUKU, Flavor.SCHOLARLY_MARKDOWN, Flavor.SHOWDOWN,
    Flavor.STACK_OVERFLOW, Flavor.TAIGA, Flavor.TRELLO,
])

_NO_STRIKETHROUGH_FLAVORS = frozenset([
    Flavor.COMMON_MARK, Flavor.GRUBER, Flavor.HAROOPAD, Flavor.IA_WRITER,
    Flavor.KRAMDOWN, Flavor.MARKDOWN2, Flavor.MARUKU, Flavor.SCHOLARLY_MARKDOWN,
    Flavor.STACK_OVERFLOW, Flavor.TAIGA,
])

_CURLY_STRIKETHROUGH_FLAVORS = frozenset([
    Flavor.MARKDOWN_EXTRA, Flavor.MARKUA, Flavor.MULTI_MARKDOWN,
])

_NO_UNDERLINE_FLAVORS = frozenset([
    Flavor.COMMON_MARK, Flavor.GITHUB, Flavor.GIT_LAB, Flavor.GRUBER,
    Flavor.IA_WRITER, Flavor.KRAMDOWN, Flavor.MARKDOWN2, Flavor.MARKDOWN_EXTRA,
    Flavor.MARUKU, Flavor.S9E_TEXT_FORMATTER, Flavor.SCHOLARLY_MARKDOWN,
    Flavor.SHOWDOWN, Flavor.STACK_OVERFLOW, Flavor.TAIGA, Flavor.TRELLO,
])

_EQUALS_UNDERLINE_FLAVORS = frozenset([
    Flavor.GHOST, Flavor.HAROOPAD, Flavor.REDCARPET, Flavor.REMARKABLE,
])


class MarkdownConverterSettings:
    """Settings of markdown converting for the chosen flavor."""

    def __init__(self, flavor=Flavor.GITHUB, new_line_type=NewLineType.UNIX,
                 skip_java_script_links=False,
                 handle_repeated_spaces=HandleRepeatedSpaces.ALTERNATE_SPACES_TO_NBSP):
        self.handle_repeated_spaces = handle_repeated_spaces
        self.skip_java_script_links = skip_java_script_links
        self.disabled_features = Feature(0)

        self._set_table(flavor)
        self._set_math_subscript(flavor)
        self._set_math_superscript(flavor)
        self._set_strikethrough(flavor)
        self._set_underline(flavor)
        self._set_font_size_data(flavor)
        self._set_italic(flavor)
        self._set_ordered_list(flavor)
        self._set_unordered_list(flavor)
        self._set_ignore_char_for_verbatim_text(flavor)
        self._set_new_line_char(new_line_type)

    def _set_font_size_data(self, flavor):
        if flavor == Flavor.X_WIKI:
            self.header_char = constants.HEADER_CHAR_USING_EQUAL
        else:
            self.header_char = constants.HEADER_CHAR

    def _set_ignore_char_for_verbatim_text(self, flavor):
        if flavor == Flavor.X_WIKI:
            self.ignore_reserved_char = constants.IGNORE_RESERVED_CHAR_USING_TILDE
        else:
            self.ignore_reserved_char = constants.IGNORE_RESERVED_CHAR

    def _set_italic(self, flavor):
        if flavor == Flavor.X_WIKI:
            self.italic_format = constants.ITALIC_SLASHES_TEXT
        else:
            self.italic_format = constants.ITALIC_TEXT

    def _set_math_subscript(self, flavor):
        self.math_subscript_format = None
        if flavor in _NO_MATH_SUBSCRIPT_FLAVORS:
            self.disabled_features |= Feature.MATH_SUBSCRIPT
        elif flavor == Flavor.X_WIKI:
            self.math_subscript_format = '{0} ,,{1},,'
        else:
            self.math_subscript_format = '{0}~{1}~'

    def _set_math_superscript(self, flavor):
        self.math_superscript_format = None
        if flavor in _NO_MATH_SUPERSCRIPT_FLAVORS:
            self.disabled_features |= Feature.MATH_SUPERSCRIPT
        elif flavor == Flavor.REDCARPET:
            self.math_superscript_format = '{0}^({1})'
        elif flavor == Flavor.X_WIKI:
            self.math_superscript_format = '{0} ^^{1}^^'
        else:
            self.math_superscript_format = '{0}^{1}^'

    def _set_new_line_char(self, new_line_type):
        if new_line_type == NewLineType.WINDOWS:
            self.new_string_text = constants.NEW_LINE_MAC + constants.NEW_LINE_UNIX
        elif new_line_type == NewLineType.MAC:
            self.new_string_text = constants.NEW_LINE_MAC
        else:
            self.new_string_text = constants.NEW_LINE_UNIX

    def _set_ordered_list(self, flavor):
        if flavor == Flavor.X_WIKI:
            self.ordered_list_format = constants.ORDERED_LIST_TEXT_USING_BRACKETS
            self.ordered_list_char = constants.ORDERED_LIST_CHAR_ONE
            self.list_char_times_for_level = constants.LIST_FIRST_SYMBOL_ONE_TIME
        else:
            self.ordered_list_format = constants.ORDERED_LIST_TEXT
            self.ordered_list_char = constants.SPACE_CHAR
            self.list_char_times_for_level = constants.LIST_FIRST_SYMBOL_FOUR_TIMES

    def _set_strikethrough(self, flavor):
        self.strikethrough_format = None
        if flavor in _NO_STRIKETHROUGH_FLAVORS:
            self.disabled_features |= Feature.STRIKETHROUGH
        elif flavor in _CURLY_STRIKETHROUGH_FLAVORS:
            self.strikethrough_format = constants.STRIKETHROUGH_USING_DASHES_AND_CURLY_BRACKETS
        elif flavor == Flavor.X_WIKI:
            self.strikethrough_format = constants.STRIKETHROUGH_TEXT_USING_DOUBLE_DASHES
        else:
            self.strikethrough_format = constants.STRIKETHROUGH_TEXT

    def _set_table(self, flavor):
        if flavor in _NO_TABLE_FLAVORS:
            self.disabled_features |= Feature.TABLE

    def _set_underline(self, flavor):
        self.underlined_format = None
        if flavor in _NO_UNDERLINE_FLAVORS:
            self.disabled_features |= Feature.UNDERLINE
        elif flavor in _EQUALS_UNDERLINE_FLAVORS:
            self.underlined_format = constants.UNDERLINED_USING_EQUALS
        elif flavor == Flavor.X_WIKI:
            self.underlined_format = constants.UNDERLINED_USING_DOUBLE_UNDER_DASHES
        else:
            self.underlined_format = constants.UNDERLINED

    def _set_unordered_list(self, flavor):
        if flavor == Flavor.X_WIKI:
            self.unordered_list_format = constants.UNORDERED_LIST_TEXT_USING_BRACKETS
            self.unordered_list_char = constants.UNORDERED_LIST_CHAR_USING_STAR
        else:
            self.unordered_list_format = constants.UNORDERED_LIST_TEXT
            self.unordered_list_char = constants.SPACE_CHAR
