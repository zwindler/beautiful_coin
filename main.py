import xml.etree.ElementTree as ET

def get_viewbox_scale(viewbox, target_size):
    _, _, vb_width, vb_height = map(float, viewbox.split())
    scale_x = target_size[0] / vb_width
    scale_y = target_size[1] / vb_height
    return min(scale_x, scale_y)

def merge_svgs(output_file, shield_file, icons):
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
        scale = get_viewbox_scale(viewbox, target_size)

        icon_group = ET.Element(f"{{{svg_ns}}}g", attrib={
            "transform": f"translate({pos[0]},{pos[1]}) scale({scale})"
        })

        for element in icon_root:
            icon_group.append(element)

        output_svg.append(icon_group)

    tree = ET.ElementTree(output_svg)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

icon_paths = [
    "svg/icon1.svg",
    "svg/icon2.svg",
    "svg/icon3.svg",
    "svg/icon4.svg",
]

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
    circle_radius3 = 320

    circle1 = ET.Element(f"{{{svg_ns}}}circle", attrib={
        "cx": "425",
        "cy": "425",
        "r": str(circle_radius1),
        "stroke": "black",
        "stroke-width": "5",
        "fill": "#DAA520"
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
        "transform": "translate(175, 250)"
    })

    for element in shield_root:
        shield_group.append(element)

    output_svg.append(shield_group)

    crown_tree = ET.parse("svg/crown.svg")
    crown_root = crown_tree.getroot()

    crown_group = ET.Element(f"{{{svg_ns}}}g", attrib={
        "transform": "translate(260, -20) scale(2.5)"
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

    text_group = ET.Element(f"{{{svg_ns}}}text", attrib={
        "font-family": "Arial",
        "font-size": "80",
        "fill": "black"
    })

    text_content = ET.Element(f"{{{svg_ns}}}textPath", attrib={
        "href": "#circle2Path",
        "startOffset": "60%" #left of coin
    })
    text_content.text = "DARTH · VADA"

    text_group.append(text_content)
    output_svg.append(text_group)

    tree = ET.ElementTree(output_svg)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

merge_svgs("output/coat_of_arms.svg", "svg/shield.svg", icon_paths)
create_coin("output/coin.svg", "output/coat_of_arms.svg")
