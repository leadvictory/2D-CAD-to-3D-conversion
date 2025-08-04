import tempfile
import os 

import cadquery as cq
from cadquery import exporters
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg


def render_and_export_image(cat_filepath: str, output_filepath: str):
    """Render a CAD file and export it as an SVG file

    Args:
        cat_file (str): Path to the CAD file
        output_filename (str): Path to the output PNG file
    """
    cad = cq.importers.importStep(cat_filepath)
    output_filename = os.path.basename(output_filepath)
    svg_filepath = output_filename + ".svg"
    exporters.export(cad, svg_filepath, exportType='SVG')
    drawing = svg2rlg(svg_filepath)

    renderPM.drawToFile(drawing, output_filepath, fmt="PNG")
