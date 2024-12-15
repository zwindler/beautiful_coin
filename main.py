import xml.etree.ElementTree as ET

def get_viewbox_scale(viewbox, target_size):
    vb_min_x, vb_min_y, vb_width, vb_height = map(float, viewbox.split())
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

merge_svgs("output/coat_of_arms.svg", "svg/shield.svg", icon_paths)
