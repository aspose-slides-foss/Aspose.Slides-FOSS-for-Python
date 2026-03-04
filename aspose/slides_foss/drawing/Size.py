class Size:
    """Represents a 2D size with integer dimensions, equivalent to System.Drawing.Size."""

    def __init__(self, width: int = 0, height: int = 0):
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f"Size(width={self.width}, height={self.height})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Size):
            return self.width == other.width and self.height == other.height
        return False
