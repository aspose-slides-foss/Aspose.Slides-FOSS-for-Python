"""Converters of slide shapes to markdown text."""

from __future__ import annotations

from ....AutoShape import AutoShape
from ....BulletType import BulletType
from ....GeometryShape import GeometryShape
from ....GroupShape import GroupShape
from ....NullableBool import NullableBool
from ....ShapeType import ShapeType
from ....Table import Table
from ....TextAlignment import TextAlignment
from ....TextStrikethroughType import TextStrikethroughType
from ....TextUnderlineType import TextUnderlineType
from ....charts.Chart import Chart
from ....export.HandleRepeatedSpaces import HandleRepeatedSpaces
from . import constants
from .chart_converters import get_chart_converter
from .settings import Feature
from .text_converter import PH_BODY


def convert_shape(shape, context):
    """Converts a shape to markdown with new lines before and after it.

    Returns None for shapes that produce no markdown output.
    """
    if _is_shape_empty(shape):
        return None

    if isinstance(shape, GroupShape):
        return convert_group_shape(shape, context)

    result = _convert_shape_to_markdown(shape, context)

    if not result:
        return result

    return context.text_converter.convert_text_with_new_lines_between_it(result)


def convert_group_shape(group_shape, context):
    parts = []
    for shape in group_shape.shapes:
        text = convert_shape(shape, context)
        if text:
            parts.append(text)
    return ''.join(parts)


def convert_auto_shape(auto_shape, context):
    text_frame = auto_shape.text_frame
    if text_frame is not None and text_frame.text:
        ph_info = auto_shape._get_placeholder_info()
        placeholder_type = PH_BODY
        if ph_info is not None and ph_info[0]:
            placeholder_type = ph_info[0]

        add_empty_lines = not context.save_options.remove_empty_lines

        return convert_text_frame(text_frame, context.text_converter, add_empty_lines, placeholder_type)

    # A picture-filled auto shape without text requires image export, which is not supported.
    return None


def _convert_shape_to_markdown(shape, context):
    # Video/audio frames and picture frames require image/media export, which is not supported.
    if isinstance(shape, AutoShape):
        result = convert_auto_shape(shape, context)
        if result is not None:
            return result

    if context.text_converter.feature_is_enabled(Feature.TABLE):
        if isinstance(shape, Table):
            result = convert_table(shape, context.text_converter)
            if result is not None:
                return result

    if isinstance(shape, Chart):
        chart_converter = get_chart_converter(list(shape.chart_data.series)[0].type)

        if chart_converter is None:
            return '### {0} chart'.format(shape.type.value)

        return chart_converter(shape, context.text_converter)

    return None


def _is_shape_empty(shape):
    if not isinstance(shape, GeometryShape) or shape.shape_type != ShapeType.NOT_DEFINED:
        return False

    if not isinstance(shape, AutoShape):
        return True

    text_frame = shape.text_frame

    return text_frame is None or not text_frame.text


def convert_text_frame(text_frame, converter, add_empty_lines=False, placeholder_type=PH_BODY):
    paragraphs = list(text_frame.paragraphs)
    count = len(paragraphs)
    parts = []

    for i in range(count):
        paragraph = paragraphs[i]
        paragraph_is_last = i == count - 1

        converted_paragraph = _convert_paragraph_to_markdown(
            converter, paragraph, add_empty_lines, placeholder_type, paragraph_is_last)

        if not converted_paragraph:
            continue

        parts.append(converter.convert_text_to_text_with_new_line(converted_paragraph)
                     if i < count - 1 else converted_paragraph)

    return ''.join(parts)


def _convert_paragraph_to_markdown(converter, paragraph, add_empty_lines, placeholder_type, paragraph_is_last):
    converted_by_portions = _convert_list_of_portions_to_markdown(converter, paragraph.portions, add_empty_lines)

    if not add_empty_lines:
        return converted_by_portions

    if not converted_by_portions:
        if not paragraph_is_last:
            return '{0}{1}{0}'.format(converter.get_new_line(), constants.EMPTY_TEXT)

        return '{0}{1}'.format(converter.get_new_line(), constants.EMPTY_TEXT)

    converted_by_lines = _convert_lines_of_paragraph_text(
        converter, paragraph, converted_by_portions, placeholder_type)

    return _replace_empty_lines(converted_by_lines, converter)


def _convert_list_of_portions_to_markdown(converter, portions, add_empty_lines):
    # Hyperlinks are not supported, so portions concatenate without
    # any link-wrapping.
    parts = []
    for portion in portions:
        text = _convert_portion_to_markdown(converter, portion, add_empty_lines)
        if text:
            parts.append(text)
    return ''.join(parts)


def _convert_portion_to_markdown(converter, portion, add_empty_lines):
    text = portion.text

    if not text:
        return text

    parts = []

    for line_text in _get_lines_of_text(text):
        if not line_text:
            parts.append(converter.get_new_line())
            continue

        parts.append(_convert_text_by_portion_format(
            converter, portion.portion_format, line_text, add_empty_lines))

    return ''.join(parts)


def _convert_lines_of_paragraph_text(converter, paragraph, text, placeholder_type):
    result = []

    lines = list(_get_lines_of_text(text))
    for line_text in lines:
        if not line_text:
            result.append(converter.get_new_line())
            continue

        result_line_text, is_header = converter.set_text_font_height(line_text, placeholder_type)

        bullet = paragraph.paragraph_format.bullet
        if bullet is not None and bullet.type not in (BulletType.NONE, BulletType.NOT_DEFINED):
            if bullet.type == BulletType.NUMBERED:
                result_line_text = converter.convert_text_to_ordered_list(
                    line_text, paragraph.paragraph_format.depth)
            else:
                result_line_text = converter.convert_text_to_unordered_list(
                    line_text, paragraph.paragraph_format.depth)

        # https://www.markdownguide.org/basic-syntax/#heading-best-practices
        if is_header and len(lines) > 1:
            result.append(converter.get_new_line())

        result.append(result_line_text)

        if is_header and len(lines) > 1:
            result.append(converter.get_new_line())

    return ''.join(result)


def _convert_text_by_portion_format(converter, portion_format, text, add_empty_lines):
    if not text:
        return ''

    result_text = text
    is_space_end = text.endswith(' ')
    is_space_start = text.startswith(' ')
    start_spaces_count = 0
    end_spaces_count = 0

    if is_space_end:
        result_text = result_text.rstrip()
        end_spaces_count = len(text) - len(result_text)

    if is_space_start:
        result_text = result_text.lstrip()
        start_spaces_count = len(text) - len(result_text) - end_spaces_count

    result_text = converter.ignore_reserved_chars(result_text)

    # In case when only spaces in text
    if not result_text:
        # Even if result text is empty, it can store spaces that were in beginning.
        return _handle_spaces_for_markdown(text, converter) if add_empty_lines else ''

    # There are some symbols that work in wrong way in different markdowns, so they are replaced to their's analogs.
    result_text = _replace_wrong_symbols(result_text, converter)

    if portion_format.strikethrough_type not in (TextStrikethroughType.NONE, TextStrikethroughType.NOT_DEFINED) and \
            converter.feature_is_enabled(Feature.STRIKETHROUGH):
        result_text = converter.convert_text_to_strikethrough(result_text)

    if portion_format.font_italic == NullableBool.TRUE:
        result_text = converter.convert_text_to_italic(result_text)

    if portion_format.font_underline not in (TextUnderlineType.NONE, TextUnderlineType.NOT_DEFINED) and \
            converter.feature_is_enabled(Feature.UNDERLINE):
        result_text = converter.convert_text_to_underlined(result_text)

    if portion_format.font_bold == NullableBool.TRUE:
        result_text = converter.convert_text_to_bold(result_text)

    # Adds deleted spaces in the start and end of the result text.
    result_text = converter.add_spaces_to_string(result_text, start_spaces_count, end_spaces_count)

    if not add_empty_lines and _is_empty_markdown_line(result_text):
        return ''

    # Replace spaces one through one to empty char, to see same tabulation, because markdown ignores two or more spaces in a row.
    return _handle_spaces_for_markdown(result_text, converter)


def _is_empty_markdown_line(text):
    return text is None or not text.strip()


def _handle_spaces_for_markdown(text, converter):
    """Normalizes special Unicode space characters and processes repeated regular spaces."""
    if not text:
        return text

    handle_repeated_spaces = converter.settings.handle_repeated_spaces

    result = []
    emit_next_space_as_nbsp = False
    previous_was_regular_space = False

    for c in text:
        # Special single-width Unicode spaces -> &nbsp;
        if c in constants.SINGLE_NBSP_SPACE_CHARS:
            result.append(constants.EMPTY_TEXT)
            emit_next_space_as_nbsp = False
            previous_was_regular_space = False
        # Wide Unicode spaces -> &nbsp;&nbsp;
        elif c in constants.DOUBLE_NBSP_SPACE_CHARS:
            result.append(constants.EMPTY_TEXT)
            result.append(constants.EMPTY_TEXT)
            emit_next_space_as_nbsp = False
            previous_was_regular_space = False
        # Regular space (U+0020)
        elif c == constants.SPACE_CHAR:
            if handle_repeated_spaces == HandleRepeatedSpaces.ALTERNATE_SPACES_TO_NBSP:
                result.append(constants.EMPTY_TEXT if emit_next_space_as_nbsp else constants.SPACE_CHAR)
                emit_next_space_as_nbsp = not emit_next_space_as_nbsp
                previous_was_regular_space = True
            elif handle_repeated_spaces == HandleRepeatedSpaces.MULTIPLE_SPACES_TO_NBSP:
                if previous_was_regular_space:
                    result.append(constants.EMPTY_TEXT)
                else:
                    result.append(constants.SPACE_CHAR)
                    previous_was_regular_space = True
            else:
                result.append(constants.SPACE_CHAR)
                previous_was_regular_space = True
        else:
            result.append(c)
            emit_next_space_as_nbsp = False
            previous_was_regular_space = False

    return ''.join(result)


def _replace_wrong_symbols(text, converter):
    text = text.replace('\v', converter.get_new_line())
    text = text.replace('\t', ' ' * 4)
    return text


def _replace_empty_lines(text, converter):
    new_line_text = converter.get_new_line()
    empty_text = constants.EMPTY_TEXT
    previous_text = ''
    result = []
    new_line_length = len(new_line_text)

    i = 0
    while i < len(text):
        current_text_to_check_ends_number = i + new_line_length

        if current_text_to_check_ends_number > len(text) - 1:
            result.append(text[i])
            i += 1
            continue

        # Take part of string with length as new line text.
        text_to_check = text[i:i + new_line_length]

        # If this part of text is new line text.
        if text_to_check == new_line_text:
            # If previous text is new line text too - add new line, empty char and new line.
            if previous_text == new_line_text:
                result.append('{0}{1}{0}'.format(new_line_text, empty_text)
                              if current_text_to_check_ends_number == len(text) - 1
                              else '{0}{1}{0}{0}'.format(new_line_text, empty_text))

                previous_text = empty_text
                i += new_line_length
                continue

            # If previous text is empty text - add empty text, and new lines.
            if previous_text == empty_text:
                result.append('{0}{1}'.format(empty_text, new_line_text)
                              if current_text_to_check_ends_number == len(text) - 1
                              else '{0}{1}{1}'.format(empty_text, new_line_text))

                previous_text = empty_text
                i += new_line_length
                continue

            previous_text = new_line_text
            result.append(text_to_check)
            i += new_line_length
            continue

        previous_text = text[i]
        result.append(text[i])
        i += 1

    return ''.join(result)


def _get_lines_of_text(text):
    if '\r\n' in text:
        text = text.replace('\r\n', '\n')

    # Checking for "\n\r" while replacing "\r\n" is intentional — this exact
    # behavior is required for output compatibility.
    if '\n\r' in text:
        text = text.replace('\r\n', '\n')

    if '\n' in text:
        return text.split('\n')

    if '\r' in text:
        return text.split('\r')

    if '\v' in text:
        return text.split('\v')

    return [text]


def convert_table(table, converter):
    divider = constants.TABLE_COLUMN_DIVIDER
    rows = list(table.rows)
    parts = [_convert_head_row(table, rows, converter, divider)]

    for row_number in range(1, len(rows)):
        parts.append(_convert_row(rows[row_number], converter, divider))

        # New line shouldn't be added after table's end.
        if row_number != len(rows) - 1:
            parts.append(converter.get_new_line())

    return ''.join(parts)


def _convert_head_row(table, rows, converter, divider):
    parts = [_convert_row(rows[0], converter, divider)]
    parts.append(converter.get_new_line())
    parts.append(_convert_head_divider(table.columns))
    parts.append(converter.get_new_line())
    return ''.join(parts)


def _convert_head_divider(columns):
    parts = [constants.TABLE_COLUMN_DIVIDER]

    for column in columns:
        parts.append(_get_column_head_divider(column))

    return ''.join(parts)


def _convert_row(row, converter, divider):
    parts = []
    cells = list(row)

    for column_number in range(len(cells)):
        if column_number == 0:
            parts.append(divider)

        if cells[column_number].text_frame is not None:
            parts.append(convert_text_frame(cells[column_number].text_frame, converter))

        parts.append(divider)

    return ''.join(parts)


def _get_column_head_divider(column):
    text_alignment = _get_column_text_alignment(column)

    if text_alignment == TextAlignment.RIGHT:
        return constants.TABLE_COLUMN_RIGHT_ALIGNMENT_DIVIDER
    if text_alignment == TextAlignment.CENTER:
        return constants.TABLE_COLUMN_CENTER_ALIGNMENT_DIVIDER
    return constants.TABLE_COLUMN_LEFT_ALIGNMENT_DIVIDER


def _get_column_text_alignment(column):
    column = list(column)
    if len(column) == 0:
        return TextAlignment.LEFT

    center_seen = False
    right_seen = False
    other_seen = False

    for cell in column:
        if cell.text_frame is None:
            continue
        for paragraph in cell.text_frame.paragraphs:
            alignment = paragraph.paragraph_format.alignment
            if alignment == TextAlignment.CENTER:
                center_seen = True
            elif alignment == TextAlignment.RIGHT:
                right_seen = True
            else:
                other_seen = True

    if not right_seen and not other_seen:
        return TextAlignment.CENTER

    if not center_seen and not other_seen:
        return TextAlignment.RIGHT

    return TextAlignment.LEFT
