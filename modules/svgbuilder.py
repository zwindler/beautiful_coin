import xml.etree.ElementTree as ET
import modules.utils as utils

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
        attrib = {
            "width": str(width),
            "height": str(height),
            "style": "shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd"
        }
        if viewBox:
            attrib["viewBox"] = viewBox
        return ET.Element("svg", attrib=attrib)

    @staticmethod
    def remove_namespace(xml_string):
        """
        Removes unnecessary namespace prefixes from an XML string.

        Args:
            xml_string (str): The XML string to process.

        Returns:
            str: XML string without namespace prefixes.
        """
        return xml_string.replace('ns0:', '').replace(':ns0', '')

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
        group = ET.Element("g", attrib={"transform": transform})
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
        circle = ET.Element("circle", attrib={
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
        text_path = ET.Element("path", attrib={
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
        text_group = ET.Element("text", attrib={
            "font-family": font_family,
            "font-size": str(font_size),
            "fill": fill,
            "font-weight": font_weight
        })
        text_content = ET.Element("textPath", attrib={
            "href": f"#{path_id}",
            "startOffset": f"{pos}%"
        })
        text_content.text = text
        text_group.append(text_content)
        parent.append(text_group)
        return parent

    @staticmethod
    def add_crown(parent, crown_path):
        """
        Adds a crown to an SVG element.

        Args:
            parent (ET.Element): Parent SVG element.
            crown_path (str): Path to the crown SVG file.

        Returns:
            ET.Element: Updated parent element.
        """
        svg_tree = ET.parse(crown_path)
        svg_root = svg_tree.getroot()

        # Ensure the svg SVG has a proper viewBox
        utils.ensure_viewbox(svg_root)

        # Fix scale issues
        scale = utils.scale_svg(svg_root, (320, 320))
        print(f"Calculated scale for crown: {scale}")

        # Wrap the svg elements in a <g> tag with scale transformation
        svg_group = ET.Element("g", {"transform": f"scale({scale})"})
        for element in list(svg_root):  # Use list to avoid modifying the root during iteration
            svg_group.append(element)
            svg_root.remove(element)
        svg_root.append(svg_group)

        return SVGBuilder.add_group_with_transform(parent, "translate(264, -10)", svg_root)

    @staticmethod
    def add_single_svg(parent, single_svg_path, already_scaled, crown):
        """
        Adds a coat of arms to an SVG element.

        Args:
            parent (ET.Element): Parent SVG element.
            single_svg_path (str): Path to the SVG file.
            already_scaled (bool): is SVG already scaled or not.
            crown (bool): add a crown or not

        Returns:
            ET.Element: Updated parent element.
        """
        svg_tree = ET.parse(single_svg_path)
        svg_root = svg_tree.getroot()

        # Ensure the svg SVG has a proper viewBox
        utils.ensure_viewbox(svg_root)

        if already_scaled:
            scale = 1
        else:
            # Fix scale issues
            scale = utils.scale_svg(svg_root, (512, 512))
            print(f"Calculated scale for svg {single_svg_path}: {scale}")

        # Wrap the svg elements in a <g> tag with scale transformation
        svg_group = ET.Element("g", {"transform": f"scale({scale})"})
        for element in list(svg_root):  # Use list to avoid modifying the root during iteration
            svg_group.append(element)
            svg_root.remove(element)
        svg_root.append(svg_group)

        if crown:
            return SVGBuilder.add_group_with_transform(parent, "translate(169, 232)", svg_root)
        return SVGBuilder.add_group_with_transform(parent, "translate(169, 200)", svg_root)
    
    @staticmethod
    def add_laurels(parent, laurels_path):
        """
        Adds laurels at the coin edge

        Args:
            parent (ET.Element): Parent SVG element.
            laurels_path (str): Path to the laurels SVG file.

        Returns:
            ET.Element: Updated parent element.
        """
        laurels_tree = ET.parse(laurels_path)
        laurels_root = laurels_tree.getroot()
        return SVGBuilder.add_group_with_transform(parent, "translate(31, 60) scale(0.615)", laurels_root)

    @staticmethod
    def add_center_lines(parent, width, height, color="red", stroke_width=1):
        """
        Adds vertical and horizontal lines at the center of the SVG for debug.

        Args:
            parent (ET.Element): Parent SVG element.
            width (int): Width of the SVG.
            height (int): Height of the SVG.
            color (str, optional): Color of the lines (default: "red").
            stroke_width (int, optional): Width of the lines (default: 1).

        Returns:
            ET.Element: Updated parent element.
        """
        # Vertical line
        vertical_line = ET.Element("line", attrib={
            "x1": str(width / 2),
            "y1": "0",
            "x2": str(width / 2),
            "y2": str(height),
            "stroke": color,
            "stroke-width": str(stroke_width)
        })
        parent.append(vertical_line)

        # Horizontal line
        horizontal_line = ET.Element("line", attrib={
            "x1": "0",
            "y1": str(height / 2),
            "x2": str(width),
            "y2": str(height / 2),
            "stroke": color,
            "stroke-width": str(stroke_width)
        })
        parent.append(horizontal_line)

        return parent
