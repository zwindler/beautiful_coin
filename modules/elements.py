import xml.etree.ElementTree as ET

import modules.utils as utils

svg_ns = "http://www.w3.org/2000/svg"

def create_coat_of_arms(output_file, shield_file, icons):
    shield_tree = ET.parse(shield_file)
    shield_root = shield_tree.getroot()
    
    ET.register_namespace("", svg_ns)

    output_svg = ET.Element(f"{{{svg_ns}}}svg", attrib={
        "width": "500",
        "height": "500",
    })

    for element in shield_root:
        output_svg.append(element)

    positions = [
        (90, 70),
        (300, 70),
        (90, 270),
        (300, 270),
    ]

    target_size = (125, 125)

    for pos, icon_file in zip(positions, icons):
        icon_tree = ET.parse(icon_file)
        icon_root = icon_tree.getroot()

        viewbox = icon_root.attrib.get("viewBox", "0 0 100 100")
        scale = utils.get_viewbox_scale(viewbox, target_size)

        icon_group = ET.Element(f"{{{svg_ns}}}g", attrib={
            "transform": f"translate({pos[0]},{pos[1]}) scale({scale})"
        })

        for element in icon_root:
            icon_group.append(element)

        output_svg.append(icon_group)

    tree = ET.ElementTree(output_svg)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


def add_circle(current_svg, radius, center, color):
    circle = ET.Element(f"{{{svg_ns}}}circle", attrib={
        "cx": f"{center}",
        "cy": f"{center}",
        "r": str(radius),
        "stroke": "black",
        "stroke-width": "5",
        "fill": f"{color}"
    })
    current_svg.append(circle)
    return current_svg


def add_textpath_circle(current_svg, radius, center, id):
    path_data = f"M {center} {center - radius} A {radius} {radius} 0 1 1 425 {center + radius} A {radius} {radius} 0 1 1 {center} {center - radius}"
    text_path = ET.Element(f"{{{svg_ns}}}path", attrib={
        "id": f"{id}",
        "d": path_data,
        "fill": "none"
    })
    current_svg.append(text_path)
    return current_svg


def add_text_on_circle(current_svg, pos, text, id):
    text_group = ET.Element(f"{{{svg_ns}}}text", attrib={
        "font-family": "Arial",
        "font-size": "80",
        "fill": "black",
        "font-weight": "bold" 
    })

    text_content = ET.Element(f"{{{svg_ns}}}textPath", attrib={
        "href": f"#{id}",
        "startOffset": f"{pos}%"
    })
    text_content.text = text

    text_group.append(text_content)
    current_svg.append(text_group)
    return current_svg


def add_crown(current_svg):
    crown_tree = ET.parse("svg/crown.svg")
    crown_root = crown_tree.getroot()

    crown_group = ET.Element(f"{{{svg_ns}}}g", attrib={
        "transform": "translate(260, -30) scale(2.5)"
    })

    for element in crown_root:
        crown_group.append(element)

    current_svg.append(crown_group)
    return current_svg


def add_coat_of_arms(current_svg, shield_file):
    shield_tree = ET.parse(shield_file)
    shield_root = shield_tree.getroot()

    shield_group = ET.Element(f"{{{svg_ns}}}g", attrib={
        "transform": "translate(175, 240)"
    })

    for element in shield_root:
        shield_group.append(element)

    current_svg.append(shield_group)
    return current_svg

def create_coin(output_file, shield_file):
    ET.register_namespace("", svg_ns)

    output_svg = ET.Element(f"{{{svg_ns}}}svg", attrib={
        "width": "850",
        "height": "850",
        "viewBox": "0 0 850 850"
    })

    add_circle(output_svg, 420, 425, "black")
    add_circle(output_svg, 390, 425, "grey")

    add_coat_of_arms(output_svg, shield_file)

    add_crown(output_svg)

    # create a SVG textPath and add text on both side of the coin
    add_textpath_circle(output_svg, 315, 425, "circlePath")
    add_text_on_circle(output_svg, "61", "DARK ▾ VADA", "circlePath")
    add_text_on_circle(output_svg, "11.8", "VADA ▾ COIN", "circlePath")

    tree = ET.ElementTree(output_svg)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
