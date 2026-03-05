from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING
from .IGeometryShape import IGeometryShape

if TYPE_CHECKING:
    from .IConnectorLock import IConnectorLock

class IConnector(IGeometryShape, ABC):
    """Represents a connector."""
    @property
    def connector_lock(self) -> IConnectorLock:
        """Returns Connector's locks. Read-only ."""
        ...

    @property
    def start_shape_connected_to(self) -> IShape:
        """Returns or sets the shape to attach the beginning of the connector to. Read/write ."""
        ...

    @start_shape_connected_to.setter
    def start_shape_connected_to(self, value: IShape):
        ...

    @property
    def end_shape_connected_to(self) -> IShape:
        """Returns or sets the shape to attach the end of the connector to. Read/write ."""
        ...

    @end_shape_connected_to.setter
    def end_shape_connected_to(self, value: IShape):
        ...

    @property
    def start_shape_connection_site_index(self) -> int:
        """Returns or sets the index of connection site for start shape. Read/write ."""
        ...

    @start_shape_connection_site_index.setter
    def start_shape_connection_site_index(self, value: int):
        ...

    @property
    def end_shape_connection_site_index(self) -> int:
        """Returns or sets the index of connection site for end shape. Read/write ."""
        ...

    @end_shape_connection_site_index.setter
    def end_shape_connection_site_index(self, value: int):
        ...

    @property
    def as_i_geometry_shape(self) -> IGeometryShape:
        """Allows to get base IGeometryShape interface. Read-only ."""
        ...
    def reroute(self) -> None:
        ...
