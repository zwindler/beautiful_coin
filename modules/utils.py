import xml.etree.ElementTree as ET
import modules.svgbuilder as svgbuilder
import re

def ensure_viewbox(svg_element):
    def parse_dimension(value):
        # Remove 'px' or any non-numeric characters
        return float(re.sub(r'[^\d.]+', '', value))

    viewbox = svg_element.get("viewBox")
    if not viewbox:
        width = parse_dimension(svg_element.get("width", "0"))
        height = parse_dimension(svg_element.get("height", "0"))
        if width > 0 and height > 0:
            viewbox = f"0 0 {width} {height}"
            svg_element.set("viewBox", viewbox)
    return viewbox

def scale_svg(svg_element, target_size):
    viewbox = ensure_viewbox(svg_element)
    _, _, vb_width, vb_height = map(float, viewbox.split())
    scale = get_viewbox_scale(viewbox, target_size)

    # Update dimensions
    scaled_width = vb_width * scale
    scaled_height = vb_height * scale
    svg_element.set("width", f"{scaled_width}px")
    svg_element.set("height", f"{scaled_height}px")
    return scale

def apply_scale_transform(svg_element, scale):
    existing_transform = svg_element.get("transform", "")
    new_transform = f"{existing_transform} scale({scale})"
    svg_element.set("transform", new_transform)

def get_viewbox_scale(viewbox, target_size):
    _, _, vb_width, vb_height = map(float, viewbox.split())
    scale_x = target_size[0] / vb_width
    scale_y = target_size[1] / vb_height
    return min(scale_x, scale_y)

def add_white_background(parent):
    background = ET.Element("rect", attrib={
        "x": "0",
        "y": "0",
        "width": "850",
        "height": "850",
        "fill": "white"
    })
    parent.append(background)
    return 

def write_clean_svg(tree, output_file):
    """
    Writes an SVG tree to a file without namespace prefixes.

    Args:
        tree (ET.ElementTree): The SVG element tree.
        output_file (str): Path to the output SVG file.
    """
    # Convert the ElementTree to a string
    rough_string = ET.tostring(tree.getroot(), encoding="unicode")
    # Remove the namespaces
    clean_string = svgbuilder.SVGBuilder.remove_namespace(rough_string)
    # Write the clean string to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(clean_string)