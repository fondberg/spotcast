"""Small script to create the icons and logos for spotcast based on
the svg files"""

from pathlib import Path
from xml.etree import ElementTree as element_tree
from types import MappingProxyType

from cairosvg import svg2png

FORMATS = (64, 128, 256, 512)
COLORS = MappingProxyType({
    "green": "1ed760",
    "black": "111111",
    "dark_gray": "232323",
    "white": "fafafa"

})

BASE_COLOR = "1ed760"


def main():
    """Main process of the create_asset script"""

    folder = Path("./assets/images/svg/")

    for svg_path in folder.iterdir():

        item = svg_path.stem

        with open(svg_path, mode='r', encoding="utf8") as file:
            svg = file.read()

        for color, hex_code in COLORS.items():

            color_folder = Path(f"./assets/images/{item}/{color}/")
            color_folder.mkdir(parents=True, exist_ok=True)

            colored_svg = svg.replace(BASE_COLOR, hex_code)

            for size in FORMATS:
                file_path = color_folder / f"{size}.png"
                print(f"Creating {file_path}")
                svg_to_png(colored_svg, file_path, size)


def svg_to_png(svg: str, output: Path, height: int, width: int = None):
    """Creates a png file from an svg

    Args:
        - svg(str): the content of an svg file
        - output(Path): the location of where to save the file
        - height(int): Height (in pixel) of the output png
        - width(int, optional): Width (in pizel) of the output png.
            Maintain aspect ratio if None. Default None
    """

    if width is None:

        svg_tree = element_tree.fromstring(svg)
        svg_dim = {
            "height": float(svg_tree.attrib["height"].replace('mm', '')),
            "width": float(svg_tree.attrib["width"].replace('mm', '')),
        }
        width = int(svg_dim["width"] * (height/svg_dim["height"]))

    svg2png(
        bytestring=svg,
        write_to=str(output),
        output_height=height,
        output_width=width,
    )


if __name__ == '__main__':
    main()
