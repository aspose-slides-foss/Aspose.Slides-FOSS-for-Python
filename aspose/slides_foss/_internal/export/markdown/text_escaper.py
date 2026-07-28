"""Escaping of markdown reserved characters in plain text."""

from __future__ import annotations


def escape_markdown_text_if_needed(text: str, escape_character: str) -> str:
    if not text:
        return ''

    result = []
    i = 0
    while i < len(text):
        ch = text[i]
        is_line_start = i == 0

        # Group 1: Escape link/image syntax [text](url), ![alt](img)
        escaped, consumed = _try_escape_link_or_image(i, text, escape_character)
        if escaped is not None:
            result.append(escaped)
            i = consumed + 1
            continue

        # Group 2: Escape <...> with non-empty content
        escaped, consumed = _try_escape_angle_brackets(i, text, escape_character)
        if escaped is not None:
            result.append(escaped)
            i = consumed + 1
            continue

        # Group 3: Escape numbered lists
        escaped, consumed = _try_escape_number_with_dot(i, text, escape_character, is_line_start)
        if escaped is not None:
            result.append(escaped)
            i = consumed + 1
            continue

        # Group 4: Escape underscores when part of _italic_ or __bold__ or more
        escaped, consumed = _try_escape_underscores_block(i, text, escape_character)
        if escaped is not None:
            result.append(escaped)
            i = consumed + 1
            continue

        # Group 5: Always escaped characters (\ ` * |)
        if _is_always_escaped(ch):
            result.append(escape_character)
            result.append(ch)
            i += 1
            continue

        # Group 6: Characters that are only escaped at the start of the line with a following space (# + - >)
        if _is_line_start_escaped(ch, is_line_start, text, i):
            result.append(escape_character)
            result.append(ch)
            i += 1
            continue

        # Group 7: Escapes a line consisting only of consecutive hyphens (one or more)
        escaped, consumed = _try_escape_line_of_hyphens(i, text, escape_character)
        if escaped is not None:
            result.append(escaped)
            i = consumed + 1
            continue

        result.append(ch)
        i += 1

    return ''.join(result)


def _is_always_escaped(ch: str) -> bool:
    return ch in ('\\', '`', '*', '|')


def _is_line_start_escaped(ch: str, is_line_start: bool, text: str, index: int) -> bool:
    if not is_line_start:
        return False

    if ch in ('#', '+', '-'):
        nxt = index + 1
        if nxt < len(text) and text[nxt].isspace():
            return True

    if ch == '>':
        return True

    return False


def _try_escape_angle_brackets(index, text, escape_character):
    if text[index] == '<':
        closing = text.find('>', index + 1)
        if closing > index + 1:  # check if at least one symbol in <.>
            inner = text[index + 1:closing]
            # Escape only if no whitespace, no digits, and length > 0
            if inner and ' ' not in inner:
                if any(c.isdigit() for c in inner):
                    return None, index
                return escape_character + '<' + inner + escape_character + '>', closing
    return None, index


def _try_escape_link_or_image(index, text, escape_character):
    # Check if start "[" or "!["
    if text[index] == '[' or (text[index] == '!' and index + 1 < len(text) and text[index + 1] == '['):
        link_start = index + 1 if text[index] == '!' else index
        close_bracket = text.find(']', link_start)

        # Check if "[]("
        if close_bracket > link_start and close_bracket + 1 < len(text) and text[close_bracket + 1] == '(':
            # Check if ".)"
            close_paren = text.find(')', close_bracket + 2)
            if close_paren > close_bracket + 2:  # check if at least one symbol in "(.)"
                parts = []
                if text[index] == '!':
                    parts.append(escape_character + '!')

                parts.append(escape_character + '[')
                parts.append(text[link_start + 1:close_bracket])
                parts.append(escape_character + ']')

                parts.append(escape_character + '(')
                parts.append(text[close_bracket + 2:close_paren])
                parts.append(escape_character + ')')

                return ''.join(parts), close_paren
    return None, index


def _try_escape_number_with_dot(index, text, escape_character, is_line_start):
    if is_line_start and text[index].isdigit():
        j = index
        while j < len(text) and text[j].isdigit():
            j += 1

        if j < len(text) and text[j] in ('.', ')'):
            k = j + 1
            if k < len(text) and text[k].isspace():
                return text[index:j] + escape_character + text[j], j
    return None, index


def _try_escape_underscores_block(index, text, escape_character):
    if text[index] != '_':
        return None, index

    if index > 0 and text[index - 1] != ' ':
        return None, index

    # Gets all markers before symbol
    count = 1
    while index + count < len(text) and text[index + count] == '_':
        count += 1

    marker = '_' * count
    end = text.find(marker, index + count)  # index of the next run of underscores after the inner text

    if end > index + count:
        inner = text[index + count:end]

        if inner.strip():
            escaped_marker = (escape_character + '_') * count
            return escaped_marker + inner + escaped_marker, end + count - 1

    return None, index


def _try_escape_line_of_hyphens(index, text, escape_character):
    if index != 0 or text[index] != '-':
        return None, index

    count = 0
    while count < len(text) and text[count] == '-':
        count += 1

    if count > 0 and count == len(text):
        return (escape_character + '-') * count, count - 1

    return None, index
