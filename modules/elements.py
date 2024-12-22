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

def create_coat_of_arms(output_file, shield_path):
    """
    Creates a coat of arms SVG by overlaying a shield and placing icons in fixed positions.

    Args:
        output_file (str): Path to the output SVG file.
        shield_path (str): Path to the shield SVG file.
    """
    shield_tree = ET.parse(shield_path)
    shield_root = shield_tree.getroot()

    # Ensure the shield SVG has a proper viewBox
    utils.ensure_viewbox(shield_root)

    # Fix scale issues
    scale = utils.scale_svg(shield_root, (650, 650))
    # print(f"Calculated scale for shield: {scale}")

    # Wrap the shield elements in a <g> tag with scale transformation
    shield_group = ET.Element("g", {"transform": f"scale({scale})"})
    for element in list(shield_root):  # Use list to avoid modifying the root during iteration
        shield_group.append(element)
        shield_root.remove(element)
    shield_root.append(shield_group)

    # Create the SVG element
    svg_element = svgbuilder.SVGBuilder.create_svg(800, 800)
    for element in shield_root:
        svg_element.append(element)

    # Positions and target size for icons
    positions = [(145, 150),
                 (350, 150),
                 (145, 350),
                 (350, 350)]
    target_size = (150, 150)

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
    write_clean_svg(tree, output_file)


def create_coin(output_file, coat_of_arms_path, crown_path, laurels_path):
    """
    Creates a complete SVG coin with concentric circles, coat of arms, crown, and text.

    Args:
        output_file (str): Path to the output SVG file.
        shield_file (str): Path to the coat of arms SVG file.
    """
    svg_element = svgbuilder.SVGBuilder.create_svg(850, 850, "0 0 850 850")

    # Add a white background if necessary (TODO add condition)
    utils.add_white_background(svg_element)

    # Add concentric circles to materialize the coin
    svgbuilder.SVGBuilder.add_circle(svg_element, 420, 425, "black")
    svgbuilder.SVGBuilder.add_circle(svg_element, 400, 425, "#444444")

    # Add coat of arms with a crown on top (or not)
    if crown_path != "none":
        svgbuilder.SVGBuilder.add_coat_of_arms(svg_element, coat_of_arms_path, True)
        svgbuilder.SVGBuilder.add_crown(svg_element, crown_path)
    else:
        svgbuilder.SVGBuilder.add_coat_of_arms(svg_element, coat_of_arms_path, False)

    # Add laurels OR text
    if laurels_path != "none":
        svgbuilder.SVGBuilder.add_laurels(svg_element, laurels_path)
    else:
        # Add circular text around a textPath, inside the coin
        svgbuilder.SVGBuilder.add_textpath_circle(svg_element, 320, 425, "circlePath")
        svgbuilder.SVGBuilder.add_text_on_circle(svg_element, 56, "DARK ▾ VADA", "circlePath")
        svgbuilder.SVGBuilder.add_text_on_circle(svg_element, 10, "VADA ▾ COIN", "circlePath")

    tree = ET.ElementTree(svg_element)
    write_clean_svg(tree, output_file)
