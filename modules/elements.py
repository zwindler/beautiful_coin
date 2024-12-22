import xml.etree.ElementTree as ET
import modules.utils as utils
import modules.svgbuilder as svgbuilder

icon_paths = [
    "svg/icon1.svg",
    "svg/icon5.svg",
    "svg/icon4.svg",
    "svg/icon2.svg",
]
shield_path = "svg/shield1.svg"

def create_coat_of_arms(output_file, shield_path):
    """
    Creates a coat of arms SVG by overlaying a shield and placing icons in fixed positions.

    Args:
        output_file (str): Path to the output SVG file.
        shield_path (str): Path to the shield SVG file.
    """
    shield_tree = ET.parse(shield_path)
    shield_root = shield_tree.getroot()

    # Create the SVG element
    svg_element = svgbuilder.SVGBuilder.create_svg(800, 800)
    for element in shield_root:
        svg_element.append(element)

    # Positions and target size for icons
    positions = [(80, 60),
                 (285, 60),
                 (80, 260),
                 (285, 260)]
    target_size = (145, 145)

    for pos, icon_file in zip(positions, icon_paths):
        icon_tree = ET.parse(icon_file)
        icon_root = icon_tree.getroot()

        viewbox = icon_root.attrib.get("viewBox", "0 0 100 100")
        scale = utils.get_viewbox_scale(viewbox, target_size)
        # print(f"Calculated scale for icon {icon_file}: {scale}")

        # Create a group for each icon and append it
        svgbuilder.SVGBuilder.add_group_with_transform(svg_element, f"translate({pos[0]},{pos[1]}) scale({scale})", icon_root)

    # Write the final SVG
    tree = ET.ElementTree(svg_element)
    utils.write_clean_svg(tree, output_file)


def create_coin(output_file, single_svg_path, crown_path, laurels_path, debug=False):
    """
    Creates a complete SVG coin borders, a central icon or coat of arms, crown, and text or laurels at the sides.

    Args:
        output_file (str): Path to the output SVG file.
        shield_file (str): Path to the central SVG file.
    """
    svg_element = svgbuilder.SVGBuilder.create_svg(850, 850, "0 0 850 850")

    # Add a white background if necessary (TODO add condition)
    utils.add_white_background(svg_element)

    # Add concentric circles to materialize the coin
    svgbuilder.SVGBuilder.add_circle(svg_element, 420, 425, "black")
    svgbuilder.SVGBuilder.add_circle(svg_element, 400, 425, "#444444")

    # Add coat of arms with a crown on top (or not)
    if crown_path != "none":
        svgbuilder.SVGBuilder.add_single_svg(svg_element, single_svg_path, True)
        svgbuilder.SVGBuilder.add_crown(svg_element, crown_path)
    else:
        svgbuilder.SVGBuilder.add_single_svg(svg_element, single_svg_path, False)

    # Add laurels OR text
    if laurels_path != "none":
        svgbuilder.SVGBuilder.add_laurels(svg_element, laurels_path)
    else:
        # Add circular text around a textPath, inside the coin
        svgbuilder.SVGBuilder.add_textpath_circle(svg_element, 320, 425, "circlePath")
        svgbuilder.SVGBuilder.add_text_on_circle(svg_element, 56, "DARK ▾ VADA", "circlePath")
        svgbuilder.SVGBuilder.add_text_on_circle(svg_element, 10, "VADA ▾ COIN", "circlePath")

    if debug:
        svgbuilder.SVGBuilder.add_center_lines(svg_element, 850, 850)

    tree = ET.ElementTree(svg_element)
    utils.write_clean_svg(tree, output_file)
