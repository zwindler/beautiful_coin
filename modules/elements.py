import xml.etree.ElementTree as ET
import modules.utils as utils
import modules.svgbuilder as svgbuilder

def create_coat_of_arms(output_file, shield_path, ul_path, ur_path, dl_path, dr_path):
    """
    Creates a coat of arms SVG by overlaying a shield and placing icons in fixed positions.

    Args:
        output_file (str): Path to the output SVG file.
        shield_path (str): Path to the shield SVG file.
        ul_path (str): Path to the upper left SVG icon file.
        ur_path (str): Path to the upper right SVG icon file.
        dl_path (str): Path to the down left SVG icon file.
        dr_path (str): Path to the down right SVG icon file.
    """
    svg_tree = ET.parse(shield_path)
    svg_root = svg_tree.getroot()

    # Ensure the svg SVG has a proper viewBox
    utils.ensure_viewbox(svg_root)

    # Fix scale issues
    scale = utils.scale_svg(svg_root, (512, 512))
    print(f"Calculated scale for svg: {scale}")

    # Wrap the svg elements in a <g> tag with scale transformation
    svg_group = ET.Element("g", {"transform": f"scale({scale})"})
    for element in list(svg_root):  # Use list to avoid modifying the root during iteration
        svg_group.append(element)
        svg_root.remove(element)
    svg_root.append(svg_group)

    # Positions and target size for icons
    positions = [(80, 60),
                 (285, 60),
                 (80, 260),
                 (285, 260)]
    target_size = (145, 145)

    icon_paths = [
        ul_path,
        ur_path,
        dl_path,
        dr_path,
    ]
    for pos, icon_file in zip(positions, icon_paths):
        icon_tree = ET.parse(icon_file)
        icon_root = icon_tree.getroot()

        viewbox = icon_root.attrib.get("viewBox", "0 0 100 100")
        scale = utils.get_viewbox_scale(viewbox, target_size)
        # print(f"Calculated scale for icon {icon_file}: {scale}")

        # Create a group for each icon and append it
        svgbuilder.SVGBuilder.add_group_with_transform(svg_root, f"translate({pos[0]},{pos[1]}) scale({scale})", icon_root)

    # Write the final SVG
    tree = ET.ElementTree(svg_root)
    utils.write_clean_svg(tree, output_file)


def create_coin(output_file, single_svg_path, crown_path, laurels_path, left_line="", right_line="", already_scaled=False, debug=False, background=True):
    """
    Creates a complete SVG coin borders, a central icon or coat of arms, crown, and text or laurels at the sides.

    Args:
        output_file (str): Path to the output SVG file.
        single_svg_path (str): Path to the central SVG file.
        crown_path (str): path for the crown SVG file, "none" is no crown.
        laurels_path (str): path for the laurels SVG file, "none" is no laurels (and replaced by text).
        left_line (str): if there is text instead of laurels, the text of the left side
        right_line (str): if there is text instead of laurels, the text of the right side
        already_scaled (bool): is the central SVG file already scaled properly.
        debug (bool): enable / disable debug.
    """
    svg_element = svgbuilder.SVGBuilder.create_svg(850, 850, "0 0 850 850")

    # Add a white background if necessary (TODO add condition)
    if background:
        utils.add_white_background(svg_element)

    # Add concentric circles to materialize the coin
    svgbuilder.SVGBuilder.add_circle(svg_element, 420, 425, "black")
    svgbuilder.SVGBuilder.add_circle(svg_element, 400, 425, "#555555")

    # Add coat of arms with a crown on top (or not)
    if crown_path != "none":
        svgbuilder.SVGBuilder.add_single_svg(svg_element, single_svg_path, already_scaled, True)
        svgbuilder.SVGBuilder.add_crown(svg_element, crown_path)
    else:
        svgbuilder.SVGBuilder.add_single_svg(svg_element, single_svg_path, already_scaled, False)

    # Add laurels OR text
    if laurels_path != "none":
        svgbuilder.SVGBuilder.add_laurels(svg_element, laurels_path)
    else:
        # Add circular text around a textPath, inside the coin
        svgbuilder.SVGBuilder.add_textpath_circle(svg_element, 315, 425, "circlePath")
        svgbuilder.SVGBuilder.add_text_on_circle(svg_element, 57.75, left_line, "circlePath")
        svgbuilder.SVGBuilder.add_text_on_circle(svg_element, 8.40, right_line, "circlePath")

    if debug:
        svgbuilder.SVGBuilder.add_center_lines(svg_element, 850, 850)

    tree = ET.ElementTree(svg_element)
    utils.write_clean_svg(tree, output_file)
