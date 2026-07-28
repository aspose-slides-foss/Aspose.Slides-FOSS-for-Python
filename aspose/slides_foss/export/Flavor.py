from __future__ import annotations
from enum import Enum

class Flavor(Enum):
    """All markdown specifications used in program."""
    GITHUB = 'Github'  # Github flavor.
    GRUBER = 'Gruber'  # Gruber flavor.
    MULTI_MARKDOWN = 'MultiMarkdown'  # Multi markdown flavor.
    COMMON_MARK = 'CommonMark'  # Common mark flavor.
    MARKDOWN_EXTRA = 'MarkdownExtra'  # Markdown extra flavor.
    PANDOC = 'Pandoc'  # Pandoc flavor.
    KRAMDOWN = 'Kramdown'  # Kramdown flavor.
    MARKUA = 'Markua'  # Markua flavor.
    MARUKU = 'Maruku'  # Maruku flavor.
    MARKDOWN2 = 'Markdown2'  # Markdown2 flavor.
    REMARKABLE = 'Remarkable'  # Remarkable flavor
    SHOWDOWN = 'Showdown'  # Showdown flavor.
    GHOST = 'Ghost'  # Ghost flavor.
    GIT_LAB = 'GitLab'  # Gitlab flavor.
    HAROOPAD = 'Haroopad'  # Haroopad flavor.
    IA_WRITER = 'IaWriter'  # IAWriter flavor.
    REDCARPET = 'Redcarpet'  # Redcarpet flavor.
    SCHOLARLY_MARKDOWN = 'ScholarlyMarkdown'  # Scholarly markdown flavor.
    TAIGA = 'Taiga'  # Taiga flavor.
    TRELLO = 'Trello'  # Trello flavor.
    S9E_TEXT_FORMATTER = 'S9ETextFormatter'  # S9E text formatter flavor.
    X_WIKI = 'XWiki'  # XWiki flavor.
    STACK_OVERFLOW = 'StackOverflow'  # Stack overflow flavor.
    DEFAULT = 'Default'  # Default markdown flavor.
