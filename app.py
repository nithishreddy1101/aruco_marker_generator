import cv2
import os
from flask import Flask, request, send_file
from fpdf import FPDF
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Mapping string names to OpenCV ArUco dictionaries
ARUCO_DICTS = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100
}

# Page size map (mm)
PAGE_SIZES = {
    "A4": (210, 297),
    "A3": (297, 420),
    "Letter": (216, 279)
}

@app.route("/generate", methods=["POST"])
def generate():

    data = request.json

    marker_side_length_mm = float(data.get("marker_size", 70))
    cut_padding_mm = float(data.get("padding", 5))
    margin_x_mm = float(data.get("margin", 10))
    spacing_between_borders_mm = float(data.get("spacing", 10))

    ids_to_generate = data.get("ids", [0, 1, 2])

    # NEW OPTIONS
    dict_name = data.get("dictionary", "DICT_4X4_50")
    page_size_name = data.get("page_size", "A4")

    border_color = data.get("border_color", [180, 180, 180])
    border_thickness = float(data.get("border_thickness", 0.1))

    # Validate dictionary
    aruco_dict = cv2.aruco.getPredefinedDictionary(
        ARUCO_DICTS.get(dict_name, cv2.aruco.DICT_4X4_50)
    )

    # Select page size
    page_w, page_h = PAGE_SIZES.get(page_size_name, (210, 297))

    output_filename = "aruco_output.pdf"

    pdf = FPDF(orientation='P', unit='mm', format=(page_w, page_h))
    pdf.add_page()
    pdf.set_font("Arial", size=9)

    block_size = marker_side_length_mm + (2 * cut_padding_mm)

    x_cursor = margin_x_mm
    y_cursor = margin_x_mm

    for marker_id in ids_to_generate:

        img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, 500)
        temp_filename = f"temp_marker_{marker_id}.png"
        cv2.imwrite(temp_filename, img)

        if x_cursor + block_size > page_w - margin_x_mm:
            x_cursor = margin_x_mm
            y_cursor += block_size + 10 + spacing_between_borders_mm

        if y_cursor + block_size + 10 > page_h - margin_x_mm:
            pdf.add_page()
            x_cursor = margin_x_mm
            y_cursor = margin_x_mm

        # BORDER STYLE FROM USER
        r, g, b = border_color
        pdf.set_draw_color(r, g, b)
        pdf.set_line_width(border_thickness)

        pdf.rect(x_cursor, y_cursor, block_size, block_size, style='D')

        image_x_pos = x_cursor + cut_padding_mm
        image_y_pos = y_cursor + cut_padding_mm

        pdf.image(
            temp_filename,
            x=image_x_pos,
            y=image_y_pos,
            w=marker_side_length_mm,
            h=marker_side_length_mm
        )

        pdf.set_text_color(0, 0, 0)

        text_x_pos = x_cursor + (block_size / 2) - 6
        text_y_pos = y_cursor + block_size + 5

        pdf.text(x=text_x_pos, y=text_y_pos, txt=f"ID: {marker_id}")

        x_cursor += block_size + spacing_between_borders_mm

        os.remove(temp_filename)

    pdf.output(output_filename)

    return send_file(output_filename, mimetype="application/pdf")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
