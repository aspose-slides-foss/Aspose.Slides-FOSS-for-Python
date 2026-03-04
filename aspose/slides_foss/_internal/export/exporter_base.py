"""
Abstract base class for presentation exporters.

Defines the interface that all format exporters must implement.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, BinaryIO, Optional, Any, Union

if TYPE_CHECKING:
    from ..opc import OpcPackage


class ExporterBase(ABC):
    """
    Abstract base class for presentation format exporters.

    Each exporter handles conversion from the internal presentation
    representation to a specific output format (PPTX, PDF, HTML, etc.).

    Subclasses must implement:
    - export_to_path(): Export to a file path
    - export_to_stream(): Export to a binary stream
    - get_supported_formats(): Return list of SaveFormat values supported
    """
    def export_to_path(
        self,
        package: OpcPackage,
        path: str,
        options: Optional[Any] = None
    ) -> None:
        """
        Export the presentation to a file path.

        Args:
            package: The OPC package containing the presentation data.
            path: The output file path.
            options: Optional export options specific to the format.

        Raises:
            IOError: If the file cannot be written.
            ValueError: If the options are invalid.
        """
        pass
    def export_to_stream(
        self,
        package: OpcPackage,
        stream: BinaryIO,
        options: Optional[Any] = None
    ) -> None:
        """
        Export the presentation to a binary stream.

        Args:
            package: The OPC package containing the presentation data.
            stream: The output stream with write capability.
            options: Optional export options specific to the format.

        Raises:
            IOError: If the stream cannot be written to.
            ValueError: If the options are invalid.
        """
        pass

    @classmethod
    def get_supported_formats(cls) -> list[str]:
        """
        Get the list of SaveFormat values this exporter supports.

        Returns:
            List of SaveFormat enum value strings (e.g., ['Pptx', 'Pptm']).
        """
        pass

    def export(
        self,
        package: OpcPackage,
        destination: Union[str, BinaryIO],
        options: Optional[Any] = None
    ) -> None:
        """
        Export to either a file path or stream.

        Args:
            package: The OPC package containing the presentation data.
            destination: File path (str) or binary stream.
            options: Optional export options specific to the format.
        """
        if isinstance(destination, str):
            self.export_to_path(package, destination, options)
        else:
            self.export_to_stream(package, destination, options)
