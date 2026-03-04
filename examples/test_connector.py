"""
Connectors — add connector shapes, adjust values, and connect to shapes.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import Presentation, ShapeType
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def add_straight_connector():
    """Add a straight connector between two positions."""
    with Presentation() as pres:
        slide = pres.slides[0]
        connector = slide.shapes.add_connector(
            ShapeType.STRAIGHT_CONNECTOR1, 100, 100, 300, 200
        )
        print(f"Connector shape_type: {connector.shape_type}")
        print(f"Position: x={connector.x}, y={connector.y}, w={connector.width}, h={connector.height}")

        pres.save(os.path.join(OUT, "straight_connector.pptx"), SaveFormat.PPTX)
        print("Saved straight_connector.pptx")


def add_bent_connector():
    """Add a bent connector with adjustment values."""
    with Presentation() as pres:
        slide = pres.slides[0]
        connector = slide.shapes.add_connector(
            ShapeType.BENT_CONNECTOR3, 50, 50, 300, 200
        )
        print(f"Bent connector type: {connector.shape_type}")

        # Access adjustment values
        adjustments = connector.adjustments
        print(f"Number of adjustments: {len(adjustments)}")

        if len(adjustments) > 0:
            adj = adjustments[0]
            print(f"  adj[0] name='{adj.name}', raw_value={adj.raw_value}")

            # Modify the adjustment
            adj.raw_value = 30000
            print(f"  adj[0] after change: raw_value={adj.raw_value}")

        pres.save(os.path.join(OUT, "bent_connector.pptx"), SaveFormat.PPTX)


def connect_shapes():
    """Connect a connector to two shapes."""
    with Presentation() as pres:
        slide = pres.slides[0]

        # Create two shapes
        shape1 = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 100, 60)
        shape2 = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 350, 200, 100, 60)

        # Create connector
        connector = slide.shapes.add_connector(
            ShapeType.BENT_CONNECTOR3, 0, 0, 1, 1
        )

        # Connect start to shape1 (site 3 = right side)
        connector.start_shape_connected_to = shape1
        connector.start_shape_connection_site_index = 3

        # Connect end to shape2 (site 1 = left side)
        connector.end_shape_connected_to = shape2
        connector.end_shape_connection_site_index = 1

        print(f"Start connected to: {connector.start_shape_connected_to is not None}")
        print(f"Start site index: {connector.start_shape_connection_site_index}")
        print(f"End connected to: {connector.end_shape_connected_to is not None}")
        print(f"End site index: {connector.end_shape_connection_site_index}")

        pres.save(os.path.join(OUT, "connected_shapes.pptx"), SaveFormat.PPTX)
        print("Saved connected_shapes.pptx")


def reroute_connector():
    """Explicitly reroute a connector after changing connections."""
    with Presentation() as pres:
        slide = pres.slides[0]

        shape1 = slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 50, 100, 80, 80)
        shape2 = slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 400, 100, 80, 80)

        connector = slide.shapes.add_connector(
            ShapeType.BENT_CONNECTOR3, 0, 0, 1, 1
        )

        connector.start_shape_connected_to = shape1
        connector.start_shape_connection_site_index = 3  # right
        connector.end_shape_connected_to = shape2
        connector.end_shape_connection_site_index = 1    # left

        # Reroute recalculates connector path
        connector.reroute()
        print("Connector rerouted")
        print(f"After reroute: x={connector.x}, y={connector.y}, w={connector.width}, h={connector.height}")

        pres.save(os.path.join(OUT, "rerouted_connector.pptx"), SaveFormat.PPTX)


def adjustment_angle_value():
    """Access angle_value of adjustment values."""
    with Presentation() as pres:
        slide = pres.slides[0]
        connector = slide.shapes.add_connector(
            ShapeType.BENT_CONNECTOR3, 50, 50, 300, 200
        )

        if len(connector.adjustments) > 0:
            adj = connector.adjustments[0]
            print(f"raw_value: {adj.raw_value}")
            print(f"angle_value: {adj.angle_value}")
            print(f"name: '{adj.name}'")


if __name__ == "__main__":
    add_straight_connector()
    add_bent_connector()
    connect_shapes()
    reroute_connector()
    adjustment_angle_value()
    print("\n=== test_connector.py completed ===")
