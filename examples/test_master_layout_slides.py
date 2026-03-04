"""
Master and layout slides — access masters, layouts, layout types, relationships.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import Presentation
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def access_masters():
    """List all master slides in a presentation."""
    with Presentation() as pres:
        print(f"Number of master slides: {len(pres.masters)}")
        for i, master in enumerate(pres.masters):
            print(f"  Master {i}: name='{master.name}', shapes={len(master.shapes)}")


def access_layout_slides():
    """List all layout slides and their types."""
    with Presentation() as pres:
        print(f"Number of layout slides: {len(pres.layout_slides)}")
        for i, layout in enumerate(pres.layout_slides):
            print(f"  Layout {i}: name='{layout.name}', type={layout.layout_type}")


def layout_master_relationship():
    """Each layout slide references a master slide."""
    with Presentation() as pres:
        for i, layout in enumerate(pres.layout_slides):
            master = layout.master_slide
            print(f"  Layout '{layout.name}' -> Master '{master.name}'")
            if i >= 4:
                print("  ...")
                break


def master_layout_slides():
    """Access layout slides through a master slide."""
    with Presentation() as pres:
        master = pres.masters[0]
        print(f"Master '{master.name}' has {len(master.layout_slides)} layout(s)")
        for i, layout in enumerate(master.layout_slides):
            print(f"  Layout {i}: '{layout.name}'")
            if i >= 4:
                print("  ...")
                break


def slide_layout_relationship():
    """Each slide has a layout_slide, and the layout has a master."""
    with Presentation() as pres:
        slide = pres.slides[0]
        layout = slide.layout_slide
        master = layout.master_slide
        print(f"Slide -> Layout '{layout.name}' -> Master '{master.name}'")


if __name__ == "__main__":
    access_masters()
    access_layout_slides()
    layout_master_relationship()
    master_layout_slides()
    slide_layout_relationship()
    print("\n=== test_master_layout_slides.py completed ===")
