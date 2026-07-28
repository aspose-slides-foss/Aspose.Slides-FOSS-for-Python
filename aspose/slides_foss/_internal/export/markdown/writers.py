"""Writers of presentation and slides to a markdown stream."""

from __future__ import annotations

from . import constants
from .shape_converters import convert_shape
from .text_converter import MarkdownTextConverter


class MarkdownStreamWriter:
    """Writes markdown text to a binary stream as UTF-8."""

    def __init__(self, stream):
        self._stream = stream

    @property
    def is_document_empty(self):
        try:
            return self._stream.tell() == 0
        except (OSError, AttributeError):
            return False

    def write(self, text):
        if not text:
            return

        self._stream.write(text.encode('utf-8'))


class Context:
    """Stores the save options and the flavor-specific text converter."""

    def __init__(self, save_options):
        self.save_options = save_options
        self.text_converter = MarkdownTextConverter(
            save_options.flavor,
            save_options.new_line_type,
            False,  # skip_java_script_links: hyperlinks are not supported
            save_options.handle_repeated_spaces)


def save_presentation_to_markdown(presentation, destination, slides_numbers=None, options=None):
    """Saves a presentation to markdown at a file path or into a binary stream."""
    if options is None:
        from ....export.MarkdownSaveOptions import MarkdownSaveOptions
        options = MarkdownSaveOptions()

    if destination is None:
        raise ValueError("Value can't be null.")

    if isinstance(destination, str):
        with open(destination, 'wb') as stream:
            _write_presentation(presentation, stream, slides_numbers, options)
    else:
        _write_presentation(presentation, stream=destination, slides_numbers=slides_numbers, options=options)


def _write_presentation(presentation, stream, slides_numbers, options):
    stream_writer = MarkdownStreamWriter(stream)
    context = Context(options)

    if slides_numbers is None:
        for slide in presentation.slides:
            if slide.hidden and not options.show_hidden_slides:
                continue

            _write_slide(slide, context, stream_writer)
        return

    slides_texts = {}
    slides_to_cache = _get_slides_to_cache(slides_numbers)
    slides_count = len(presentation.slides)

    for slide_number in slides_numbers:
        if slide_number > slides_count or slide_number < 1:
            raise ValueError(
                "'slides' array contains {0} slide position, which is not present in the presentation.".format(
                    slide_number))

        if slide_number in slides_texts:
            stream_writer.write(slides_texts[slide_number])
            continue

        slide = presentation.slides[slide_number - 1]
        result_slide_text = _write_slide(slide, context, stream_writer)

        if slide_number in slides_to_cache:
            slides_texts[slide_number] = result_slide_text


def _get_slides_to_cache(slides_numbers):
    seen = set()
    to_cache = set()

    for slide_number in slides_numbers:
        if slide_number in seen:
            to_cache.add(slide_number)
        else:
            seen.add(slide_number)

    return to_cache


def _write_slide(slide, context, stream_writer):
    result_slide_text = []

    result_slide_text.append(_write_slide_divider(slide.slide_number, context, stream_writer))

    # Background pictures require image export, which is not supported.

    result_slide_text.append(_write_shapes(slide, context, stream_writer))

    if context.save_options.show_comments:
        result_slide_text.append(_write_comments(slide, context, stream_writer))

    return ''.join(result_slide_text)


def _write_shapes(slide, context, stream_writer):
    converter = context.text_converter
    shapes = sorted(slide.shapes, key=lambda s: (s.y, s.x))

    shapes_text = []

    for shape in shapes:
        shape_text = convert_shape(shape, context)

        if shape_text == '':
            continue

        stream_writer.write(shape_text)
        shapes_text.append(converter.convert_text_to_text_with_new_line(shape_text))

    return ''.join(shapes_text)


def _write_comments(slide, context, stream_writer):
    converter = context.text_converter
    comments = []

    for author in slide.presentation.comment_authors:
        for comment in author.comments:
            if comment.slide is slide:
                comments.append(
                    converter.convert_text_to_text_with_new_line(
                        converter.convert_comment_text(author.name, comment.text)))

    comments_string = ''.join(comments)
    stream_writer.write(comments_string)

    return comments_string


def _write_horizontal_line(context):
    return context.text_converter.convert_text_to_text_with_new_line(constants.HORIZONTAL_LINE)


def _write_slide_divider(slide_number, context, stream_writer):
    converter = context.text_converter
    slide_divider = []

    if not stream_writer.is_document_empty:
        slide_divider.append(converter.get_new_line())

    # The slide header on the first slide doesn't display correctly in some viewers
    if context.save_options.show_slide_number and slide_number == 1:
        slide_divider.append(converter.get_new_line())

    slide_divider.append(_write_horizontal_line(context))

    if context.save_options.show_slide_number:
        slide_divider.append(_get_slide_number_markdown_header(slide_number, context))
        slide_divider.append(converter.get_new_line())
        slide_divider.append(_write_horizontal_line(context))

    slide_divider_text = ''.join(slide_divider)
    stream_writer.write(slide_divider_text)

    return slide_divider_text


def _get_slide_number_markdown_header(slide_number, context):
    slide_number_format = context.save_options.slide_number_format or constants.SLIDE_NUMBER_FORMAT

    return slide_number_format.format(slide_number)
