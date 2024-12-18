import xml.etree.ElementTree as ET
import modules.utils as utils


icon_paths = [
    "svg/icon1.svg",
    "svg/icon5.svg",
    "svg/icon4.svg",
    "svg/icon2.svg",
]
shield_path = "svg/shield1.svg"

class SVGBuilder:
    """Utility class for simplifying SVG element manipulation."""
    svg_ns = "http://www.w3.org/2000/svg"

    @staticmethod
    def create_svg(width, height, viewBox=None):
        """
        Creates a basic SVG element.

        Args:
            width (int): Width of the SVG.
            height (int): Height of the SVG.
            viewBox (str, optional): ViewBox attribute, if needed.

        Returns:
            ET.Element: The created SVG element.
        """
        attrib = {"width": str(width), "height": str(height)}
        if viewBox:
            attrib["viewBox"] = viewBox
        return ET.Element(f"{{{SVGBuilder.svg_ns}}}svg", attrib=attrib)

    @staticmethod
    def add_group_with_transform(parent, transform, elements):
        """
        Adds a group (`<g>`) with a transformation and child elements.

        Args:
            parent (ET.Element): Parent SVG element.
            transform (str): SVG transformation (e.g., "translate(260, -30) scale(2.5)").
            elements (list[ET.Element]): List of child elements to include in the group.

        Returns:
            ET.Element: Updated parent element.
        """
        group = ET.Element(f"{{{SVGBuilder.svg_ns}}}g", attrib={"transform": transform})
        for element in elements:
            group.append(element)
        parent.append(group)
        return parent

    @staticmethod
    def add_circle(parent, radius, center, color, stroke="black", stroke_width=5):
        """
        Adds a circle to an SVG element.

        Args:
            parent (ET.Element): Parent SVG element.
            radius (int): Circle radius.
            center (int): Center position (`cx`, `cy`) of the circle.
            color (str): Fill color.
            stroke (str, optional): Stroke color (default: "black").
            stroke_width (int, optional): Stroke width (default: 5).

        Returns:
            ET.Element: Updated parent element.
        """
        circle = ET.Element(f"{{{SVGBuilder.svg_ns}}}circle", attrib={
            "cx": str(center),
            "cy": str(center),
            "r": str(radius),
            "stroke": stroke,
            "stroke-width": str(stroke_width),
            "fill": color
        })
        parent.append(circle)
        return parent

    @staticmethod
    def add_textpath_circle(parent, radius, center, path_id):
        """
        Adds a circular path for text to follow.

        Args:
            parent (ET.Element): Parent SVG element.
            radius (int): Circle radius.
            center (int): Center position (`cx`, `cy`) of the circle.
            path_id (str): Unique identifier for the path.

        Returns:
            ET.Element: Updated parent element.
        """
        path_data = (
            f"M {center} {center - radius} "
            f"A {radius} {radius} 0 1 1 {center} {center + radius} "
            f"A {radius} {radius} 0 1 1 {center} {center - radius}"
        )
        text_path = ET.Element(f"{{{SVGBuilder.svg_ns}}}path", attrib={
            "id": path_id,
            "d": path_data,
            "fill": "none"
        })
        parent.append(text_path)
        return parent

    @staticmethod
    def add_text_on_circle(parent, pos, text, path_id, font_family="Arial", font_size=100, fill="black", font_weight="bold"):
        """
        Adds text along a circular path.

        Args:
            parent (ET.Element): Parent SVG element.
            pos (float): Text position percentage (startOffset).
            text (str): Text content.
            path_id (str): Identifier for the path.
            font_family (str, optional): Font family (default: "Arial").
            font_size (int, optional): Font size (default: 100).
            fill (str, optional): Text color (default: "black").
            font_weight (str, optional): Font weight (default: "bold").

        Returns:
            ET.Element: Updated parent element.
        """
        text_group = ET.Element(f"{{{SVGBuilder.svg_ns}}}text", attrib={
            "font-family": font_family,
            "font-size": str(font_size),
            "fill": fill,
            "font-weight": font_weight
        })
        text_content = ET.Element(f"{{{SVGBuilder.svg_ns}}}textPath", attrib={
            "href": f"#{path_id}",
            "startOffset": f"{pos}%"
        })
        text_content.text = text
        text_group.append(text_content)
        parent.append(text_group)
        return parent
    
    def add_crown(parent, crown_path):
        """
        Adds a crown to an SVG element.

        Args:
            parent (ET.Element): Parent SVG element.
            crown_path (str): Path to the crown SVG file.

        Returns:
            ET.Element: Updated parent element.
        """
        crown_tree = ET.parse(crown_path)
        crown_root = crown_tree.getroot()
        return SVGBuilder.add_group_with_transform(parent, "translate(260, -45) scale(2.5)", crown_root)

    def add_coat_of_arms(parent, coat_of_arms_path):
        """
        Adds a coat of arms to an SVG element.

        Args:
            parent (ET.Element): Parent SVG element.
            coat_of_arms_path (str): Path to the coat of arms SVG file.

        Returns:
            ET.Element: Updated parent element.
        """
        shield_tree = ET.parse(coat_of_arms_path)
        shield_root = shield_tree.getroot()
        return SVGBuilder.add_group_with_transform(parent, "translate(175, 230)", shield_root)


def create_coat_of_arms(output_file):
    """
    Creates a coat of arms SVG by overlaying a shield and placing icons in fixed positions.

    Args:
        output_file (str): Path to the output SVG file.
        shield_file (str): Path to the shield SVG file.
        icons (list[str]): List of icon SVG file paths.
    """
    shield_tree = ET.parse(shield_path)
    shield_root = shield_tree.getroot()
    svg_element = SVGBuilder.create_svg(500, 500)
    for element in shield_root:
        svg_element.append(element)

    positions = [(90, 70), (300, 70), (90, 270), (300, 270)]
    target_size = (130, 130)

    for pos, icon_file in zip(positions, icon_paths):
        icon_tree = ET.parse(icon_file)
        icon_root = icon_tree.getroot()
        viewbox = icon_root.attrib.get("viewBox", "0 0 100 100")
        scale = utils.get_viewbox_scale(viewbox, target_size)

        # Create a group for each icon and append it
        SVGBuilder.add_group_with_transform(svg_element, f"translate({pos[0]},{pos[1]}) scale({scale})", icon_root)

    tree = ET.ElementTree(svg_element)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

def add_white_background(parent):
    background = ET.Element(f"{{{SVGBuilder.svg_ns}}}rect", attrib={
        "x": "0",
        "y": "0",
        "width": "850",
        "height": "850",
        "fill": "white"
    })
    parent.append(background)
    return 

def create_coin(output_file, coat_of_arms_path, crown_path):
    """
    Creates a complete SVG coin with concentric circles, coat of arms, crown, and text.

    Args:
        output_file (str): Path to the output SVG file.
        shield_file (str): Path to the coat of arms SVG file.
    """
    svg_element = SVGBuilder.create_svg(850, 850, "0 0 850 850")

    # Add a white background
    add_white_background(svg_element)

    # Add concentric circles to materialize the coin
    SVGBuilder.add_circle(svg_element, 420, 425, "black")
    SVGBuilder.add_circle(svg_element, 400, 425, "grey")

    # Add coat of arms with a crown on top
    SVGBuilder.add_coat_of_arms(svg_element, coat_of_arms_path)
    SVGBuilder.add_crown(svg_element, crown_path)

    # Add circular text around a textPath, inside the coin
    SVGBuilder.add_textpath_circle(svg_element, 315, 425, "circlePath")
    SVGBuilder.add_text_on_circle(svg_element, 56, "DARK ▾ VADA", "circlePath")
    SVGBuilder.add_text_on_circle(svg_element, 10, "VADA ▾ COIN", "circlePath")

    tree = ET.ElementTree(svg_element)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
