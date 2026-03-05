"""Tests for DocumentProperties: core + custom properties."""
from aspose.slides_foss import Presentation


def test_core_properties(tmp_pptx):
    """Core properties persist after save/reload."""
    pres = Presentation()
    props = pres.document_properties
    props.title = "My Presentation"
    props.subject = "Demo Subject"
    props.author = "John Doe"
    props.keywords = "demo, test"
    props.category = "Examples"

    pres2 = tmp_pptx(pres)
    p2 = pres2.document_properties
    assert p2.title == "My Presentation"
    assert p2.subject == "Demo Subject"
    assert p2.author == "John Doe"
    assert p2.keywords == "demo, test"
    assert p2.category == "Examples"
    pres2.dispose()


def test_custom_string_property(tmp_pptx):
    """Custom string properties persist."""
    pres = Presentation()
    pres.document_properties.set_custom_property_value("MyProp", "hello")

    pres2 = tmp_pptx(pres)
    out = [None]
    pres2.document_properties.get_custom_property_value("MyProp", out)
    assert out[0] == "hello"
    pres2.dispose()


def test_custom_int_property(tmp_pptx):
    """Custom integer properties persist."""
    pres = Presentation()
    pres.document_properties.set_custom_property_value("Count", 42)

    pres2 = tmp_pptx(pres)
    out = [None]
    pres2.document_properties.get_custom_property_value("Count", out)
    assert out[0] == 42
    pres2.dispose()


def test_remove_custom_property():
    """Removing a custom property decreases count."""
    with Presentation() as pres:
        props = pres.document_properties
        props.set_custom_property_value("A", "val")
        props.set_custom_property_value("B", "val")
        assert props.count_of_custom_properties == 2

        props.remove_custom_property("A")
        assert props.count_of_custom_properties == 1
        assert props.contains_custom_property("A") is False
        assert props.contains_custom_property("B") is True
