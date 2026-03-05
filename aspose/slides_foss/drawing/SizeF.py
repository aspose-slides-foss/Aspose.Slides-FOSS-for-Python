class SizeF:
    """Represents a 2D size with float dimensions, equivalent to System.Drawing.SizeF."""

    def __init__(self, width: float = 0.0, height: float = 0.0):
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f"SizeF(width={self.width}, height={self.height})"

    def __eq__(self, other) -> bool:
        if isinstance(other, SizeF):
            return self.width == other.width and self.height == other.height
        return False
