"""
XML namespace constants for SpreadsheetML (XLSX) format.

Namespaces are isolated from PPTX — no global ET.register_namespace() calls.
All serialization uses explicit nsmap dicts.
"""

from __future__ import annotations

# --- Namespace URIs ---

SML_URI = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
R_URI = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
MC_URI = 'http://schemas.openxmlformats.org/markup-compatibility/2006'

# Formatted namespace strings for lxml element access
SML_NS = f'{{{SML_URI}}}'
R_NS = f'{{{R_URI}}}'

# Explicit nsmap dicts for XML serialization (no global registration)
WORKBOOK_NSMAP = {
    None: SML_URI,
    'r': R_URI,
}

WORKSHEET_NSMAP = {
    None: SML_URI,
    'r': R_URI,
}

SST_NSMAP = {
    None: SML_URI,
}

TABLE_NSMAP = {
    None: SML_URI,
}

# --- Relationship types (XLSX-specific) ---

XLSX_REL_TYPES = {
    'worksheet': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet',
    'shared_strings': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings',
    'styles': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles',
    'table': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/table',
    'theme': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme',
}

# --- Content types (XLSX-specific) ---

XLSX_CONTENT_TYPES = {
    'workbook': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml',
    'worksheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml',
    'shared_strings': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml',
    'styles': 'application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml',
    'table': 'application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml',
}
