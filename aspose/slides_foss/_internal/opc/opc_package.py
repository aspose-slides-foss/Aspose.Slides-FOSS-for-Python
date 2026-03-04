"""
OPC Package handling for ZIP-based Office Open XML formats.

Provides reading and writing capabilities for PPTX and similar formats,
preserving unknown parts to ensure round-trip fidelity.
"""

from __future__ import annotations
import zipfile
import os
import io
from typing import BinaryIO, Optional, Union


class OpcPackage:
    """
    Manages an Open Packaging Conventions (OPC) package.

    An OPC package is a ZIP archive containing parts (files) organized
    according to Office Open XML conventions. This class provides:
    - Loading from file path or stream
    - Saving to file path or stream
    - Part access (get/set/delete)
    - Preservation of unknown parts for round-trip fidelity
    """

    def __init__(self):
        """Initialize an empty OPC package."""
        self._parts: dict[str, bytes] = {}
        self._source_path: Optional[str] = None

    @classmethod
    def open(cls, source: Union[str, BinaryIO]) -> OpcPackage:
        """
        Open an OPC package from a file path or stream.

        Args:
            source: File path (str) or binary stream with read capability.

        Returns:
            Loaded OpcPackage instance.

        Raises:
            FileNotFoundError: If file path doesn't exist.
            zipfile.BadZipFile: If the file is not a valid ZIP archive.
        """
        package = cls()

        if isinstance(source, str):
            package._source_path = source
            if not os.path.exists(source):
                raise FileNotFoundError(f"Package file not found: {source}")
            package._load_from_path(source)
        else:
            package._load_from_stream(source)

        return package

    @classmethod
    def create_new(cls) -> OpcPackage:
        """
        Create a new empty OPC package.

        Returns:
            New empty OpcPackage instance.
        """
        return cls()

    def _load_from_path(self, path: str) -> None:
        """Load all parts from a ZIP file at the given path."""
        with zipfile.ZipFile(path, 'r') as zf:
            self._load_from_zipfile(zf)

    def _load_from_stream(self, stream: BinaryIO) -> None:
        """Load all parts from a ZIP stream."""
        with zipfile.ZipFile(stream, 'r') as zf:
            self._load_from_zipfile(zf)

    def _load_from_zipfile(self, zf: zipfile.ZipFile) -> None:
        """Load all parts from an open ZipFile object."""
        for name in zf.namelist():
            self._parts[name] = zf.read(name)

    def save(self, destination: Union[str, BinaryIO]) -> None:
        """
        Save the OPC package to a file path or stream.

        Args:
            destination: File path (str) or binary stream with write capability.
        """
        if isinstance(destination, str):
            self._save_to_path(destination)
        else:
            self._save_to_stream(destination)

    def _save_to_path(self, path: str) -> None:
        """Save all parts to a ZIP file at the given path."""
        with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zf:
            self._save_to_zipfile(zf)

    def _save_to_stream(self, stream: BinaryIO) -> None:
        """Save all parts to a ZIP stream."""
        with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as zf:
            self._save_to_zipfile(zf)

    def _save_to_zipfile(self, zf: zipfile.ZipFile) -> None:
        """Save all parts to an open ZipFile object."""
        for name, content in self._parts.items():
            zf.writestr(name, content)

    def get_part(self, part_name: str) -> Optional[bytes]:
        """
        Get the content of a part by name.

        Args:
            part_name: The part path within the package (e.g., 'ppt/presentation.xml').

        Returns:
            Part content as bytes, or None if part doesn't exist.
        """
        return self._parts.get(part_name)

    def set_part(self, part_name: str, content: Union[bytes, str]) -> None:
        """
        Set or update the content of a part.

        Args:
            part_name: The part path within the package.
            content: Part content as bytes or string (will be encoded as UTF-8).
        """
        if isinstance(content, str):
            content = content.encode('utf-8')
        self._parts[part_name] = content

    def has_part(self, part_name: str) -> bool:
        """
        Check if a part exists in the package.

        Args:
            part_name: The part path to check.

        Returns:
            True if the part exists, False otherwise.
        """
        return part_name in self._parts

    def delete_part(self, part_name: str) -> bool:
        """
        Delete a part from the package.

        Args:
            part_name: The part path to delete.

        Returns:
            True if the part was deleted, False if it didn't exist.
        """
        if part_name in self._parts:
            del self._parts[part_name]
            return True
        return False

    def get_part_names(self) -> list[str]:
        """
        Get a list of all part names in the package.

        Returns:
            List of part paths.
        """
        return list(self._parts.keys())

    @property
    def source_path(self) -> Optional[str]:
        """
        Get the original file path if the package was loaded from a file.

        Returns:
            File path or None if loaded from stream or created new.
        """
        return self._source_path

    def close(self) -> None:
        """
        Close the package and release resources.

        Clears all in-memory part data. The package should not be used after closing.
        """
        self._parts.clear()
        self._source_path = None
