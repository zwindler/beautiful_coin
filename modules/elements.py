import xml.etree.ElementTree as ET

import modules.utils as utils

def create_coat_of_arms(output_file, shield_file, icons):
    shield_tree = ET.parse(shield_file)
    shield_root = shield_tree.getroot()

    svg_ns = "http://www.w3.org/2000/svg"
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

def create_coin(output_file, shield_file):
    svg_ns = "http://www.w3.org/2000/svg"
    ET.register_namespace("", svg_ns)

    output_svg = ET.Element(f"{{{svg_ns}}}svg", attrib={
        "width": "850",
        "height": "850",
        "viewBox": "0 0 850 850"
    })

    circle_radius1 = 420
    circle_radius2 = 390
    circle_radius3 = 315

    circle1 = ET.Element(f"{{{svg_ns}}}circle", attrib={
        "cx": "425",
        "cy": "425",
        "r": str(circle_radius1),
        "stroke": "black",
        "stroke-width": "5",
        "fill": "black"
    })
    output_svg.append(circle1)

    circle2 = ET.Element(f"{{{svg_ns}}}circle", attrib={
        "cx": "425",
        "cy": "425",
        "r": str(circle_radius2),
        "stroke": "black",
        "stroke-width": "5",
        "fill": "#FFD700"
    })
    output_svg.append(circle2)

    shield_tree = ET.parse(shield_file)
    shield_root = shield_tree.getroot()

    shield_group = ET.Element(f"{{{svg_ns}}}g", attrib={
        "transform": "translate(175, 240)"
    })

    for element in shield_root:
        shield_group.append(element)

    output_svg.append(shield_group)

    crown_tree = ET.parse("svg/crown.svg")
    crown_root = crown_tree.getroot()

    crown_group = ET.Element(f"{{{svg_ns}}}g", attrib={
        "transform": "translate(260, -30) scale(2.5)"
    })

    for element in crown_root:
        crown_group.append(element)

    output_svg.append(crown_group)

    path_data = f"M 425 {425 - circle_radius3} A {circle_radius3} {circle_radius3} 0 1 1 425 {425 + circle_radius3} A {circle_radius3} {circle_radius3} 0 1 1 425 {425 - circle_radius3}"
    text_path = ET.Element(f"{{{svg_ns}}}path", attrib={
        "id": "circle2Path",
        "d": path_data,
        "fill": "none"
    })
    output_svg.append(text_path)

    text_group_left = ET.Element(f"{{{svg_ns}}}text", attrib={
        "font-family": "Arial",
        "font-size": "80",
        "fill": "black",
        "font-weight": "bold" 
    })

    text_content_left = ET.Element(f"{{{svg_ns}}}textPath", attrib={
        "href": "#circle2Path",
        "startOffset": "61%" #left of coin
    })
    text_content_left.text = "DARK ▾ VADA"

    text_group_left.append(text_content_left)
    output_svg.append(text_group_left)

    text_group_right = ET.Element(f"{{{svg_ns}}}text", attrib={
        "font-family": "Arial",
        "font-size": "80",
        "fill": "black",
        "font-weight": "bold" 
    })

    text_content_right = ET.Element(f"{{{svg_ns}}}textPath", attrib={
        "href": "#circle2Path",
        "startOffset": "11.8%" #right of coin
    })
    text_content_right.text = "VADA ▾ COIN"

    text_group_right.append(text_content_right)
    output_svg.append(text_group_right)


    tree = ET.ElementTree(output_svg)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
