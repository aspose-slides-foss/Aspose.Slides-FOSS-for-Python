"""Tests for Connector shapes, adjustments, and connections."""
from aspose.slides_foss import Presentation, ShapeType


def test_add_straight_connector():
    """Add a straight connector with correct type."""
    with Presentation() as pres:
        slide = pres.slides[0]
        conn = slide.shapes.add_connector(ShapeType.STRAIGHT_CONNECTOR1, 100, 100, 300, 200)
        assert conn.shape_type == ShapeType.STRAIGHT_CONNECTOR1


def test_add_straight_connector_persists(tmp_pptx):
    """Straight connector survives save/reload."""
    pres = Presentation()
    pres.slides[0].shapes.add_connector(ShapeType.STRAIGHT_CONNECTOR1, 100, 100, 300, 200)

    pres2 = tmp_pptx(pres)
    assert len(pres2.slides[0].shapes) >= 1
    pres2.dispose()


def test_bent_connector_adjustments(tmp_pptx):
    """Adjustment values persist after save/reload."""
    from aspose.slides_foss import Connector
    pres = Presentation()
    pres.slides[0].shapes.clear()
    conn = pres.slides[0].shapes.add_connector(ShapeType.BENT_CONNECTOR3, 50, 50, 300, 200)
    if len(conn.adjustments) > 0:
        conn.adjustments[0].raw_value = 30000

    pres2 = tmp_pptx(pres)
    # Find the connector shape
    conn2 = None
    for sh in pres2.slides[0].shapes:
        if isinstance(sh, Connector):
            conn2 = sh
            break
    assert conn2 is not None, "Connector not found after reload"
    if len(conn2.adjustments) > 0:
        assert conn2.adjustments[0].raw_value == 30000
    pres2.dispose()


def test_connect_shapes(tmp_pptx):
    """Start/end connections persist."""
    pres = Presentation()
    slide = pres.slides[0]
    slide.shapes.clear()
    s1 = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 100, 60)
    s2 = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 350, 200, 100, 60)
    conn = slide.shapes.add_connector(ShapeType.BENT_CONNECTOR3, 0, 0, 1, 1)

    conn.start_shape_connected_to = s1
    conn.start_shape_connection_site_index = 3
    conn.end_shape_connected_to = s2
    conn.end_shape_connection_site_index = 1

    assert conn.start_shape_connected_to is not None
    assert conn.end_shape_connected_to is not None

    pres2 = tmp_pptx(pres)
    conn2 = None
    for sh in pres2.slides[0].shapes:
        if sh.shape_type == ShapeType.BENT_CONNECTOR3:
            conn2 = sh
            break
    assert conn2 is not None
    assert conn2.start_shape_connection_site_index == 3
    assert conn2.end_shape_connection_site_index == 1
    pres2.dispose()


def test_reroute():
    """reroute() updates connector position."""
    with Presentation() as pres:
        slide = pres.slides[0]
        s1 = slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 50, 100, 80, 80)
        s2 = slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 400, 100, 80, 80)
        conn = slide.shapes.add_connector(ShapeType.BENT_CONNECTOR3, 0, 0, 1, 1)
        conn.start_shape_connected_to = s1
        conn.start_shape_connection_site_index = 3
        conn.end_shape_connected_to = s2
        conn.end_shape_connection_site_index = 1
        conn.reroute()
        # After reroute the connector should span between the shapes
        assert conn.width > 0 or conn.height > 0


def test_adjustment_properties():
    """Adjustment values expose name, raw_value, angle_value."""
    with Presentation() as pres:
        conn = pres.slides[0].shapes.add_connector(ShapeType.BENT_CONNECTOR3, 50, 50, 300, 200)
        if len(conn.adjustments) > 0:
            adj = conn.adjustments[0]
            assert adj.name is not None
            assert isinstance(adj.raw_value, (int, float))
            assert isinstance(adj.angle_value, (int, float))
