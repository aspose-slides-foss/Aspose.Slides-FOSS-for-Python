class PointF:
    """Represents a 2D point with float coordinates, equivalent to System.Drawing.PointF."""

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"PointF(x={self.x}, y={self.y})"

    def __eq__(self, other) -> bool:
        if isinstance(other, PointF):
            return self.x == other.x and self.y == other.y
        return False
