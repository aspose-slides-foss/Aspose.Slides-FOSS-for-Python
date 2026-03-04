"""
DocumentProperties — core properties, app properties, and custom properties.
"""
import os
import sys
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import Presentation
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def core_properties():
    """Set and read core document properties."""
    with Presentation() as pres:
        props = pres.document_properties

        # Set core properties
        props.title = "My Presentation"
        props.subject = "Demo Subject"
        props.author = "John Doe"
        props.keywords = "demo, test, slides"
        props.comments = "Created as a demo"
        props.category = "Examples"
        props.content_status = "Draft"
        props.content_type = "Presentation"
        props.last_saved_by = "Jane Doe"
        props.revision_number = 2

        # Read them back
        print(f"title: '{props.title}'")
        print(f"subject: '{props.subject}'")
        print(f"author: '{props.author}'")
        print(f"keywords: '{props.keywords}'")
        print(f"comments: '{props.comments}'")
        print(f"category: '{props.category}'")
        print(f"content_status: '{props.content_status}'")
        print(f"last_saved_by: '{props.last_saved_by}'")
        print(f"revision_number: {props.revision_number}")

        pres.save(os.path.join(OUT, "core_properties.pptx"), SaveFormat.PPTX)


def time_properties():
    """Set creation and modification timestamps."""
    with Presentation() as pres:
        props = pres.document_properties

        now = datetime.datetime.now()
        props.created_time = now
        props.last_saved_time = now

        print(f"created_time: {props.created_time}")
        print(f"last_saved_time: {props.last_saved_time}")

        pres.save(os.path.join(OUT, "time_properties.pptx"), SaveFormat.PPTX)


def app_properties():
    """Read application properties."""
    with Presentation() as pres:
        props = pres.document_properties

        print(f"app_version: '{props.app_version}'")
        print(f"total_editing_time: {props.total_editing_time}")

        pres.save(os.path.join(OUT, "app_properties.pptx"), SaveFormat.PPTX)


def custom_properties():
    """Add, read, and remove custom document properties."""
    with Presentation() as pres:
        props = pres.document_properties

        # Add custom properties of different types
        props.set_custom_property_value("CustomString", "Hello")
        props.set_custom_property_value("CustomNumber", 42)
        props.set_custom_property_value("CustomBool", True)

        # Read them back using get_custom_property_value (value returned via list)
        out = [None]
        props.get_custom_property_value("CustomString", out)
        print(f"CustomString: {out[0]}")

        props.get_custom_property_value("CustomNumber", out)
        print(f"CustomNumber: {out[0]}")

        props.get_custom_property_value("CustomBool", out)
        print(f"CustomBool: {out[0]}")

        # Count custom properties
        print(f"Custom property count: {props.count_of_custom_properties}")

        # Check contains
        print(f"Contains 'CustomBool': {props.contains_custom_property('CustomBool')}")

        # Remove a custom property
        props.remove_custom_property("CustomBool")
        print(f"After removal: {props.count_of_custom_properties} custom properties")

        pres.save(os.path.join(OUT, "custom_properties.pptx"), SaveFormat.PPTX)


def read_properties_from_file():
    """Load a file and read its properties."""
    # First create a file with properties
    path = os.path.join(OUT, "props_roundtrip.pptx")
    with Presentation() as pres:
        pres.document_properties.title = "Round-Trip Title"
        pres.document_properties.author = "Test Author"
        pres.save(path, SaveFormat.PPTX)

    # Now load and verify
    with Presentation(path) as pres:
        props = pres.document_properties
        print(f"Loaded title: '{props.title}'")
        print(f"Loaded author: '{props.author}'")


if __name__ == "__main__":
    core_properties()
    time_properties()
    app_properties()
    custom_properties()
    read_properties_from_file()
    print("\n=== test_document_properties.py completed ===")
