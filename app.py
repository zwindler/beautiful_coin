from flask import Flask, render_template, request, jsonify, send_file
import modules.elements as elements
import os

common_options = {
    "crowns": [
        {"value": "none", "img": "static/none.svg", "alt": "None"},
        {"value": "static/crown1.svg", "img": "static/crown1.svg", "alt": "Crown 1", "checked": True},
        {"value": "static/crown2.svg", "img": "static/crown2.svg", "alt": "Crown 2"},
        {"value": "static/crown3.svg", "img": "static/crown3.svg", "alt": "Crown 3"},
    ],
    "shields": [
        {"value": "static/shield1.svg", "img": "static/shield1.svg", "alt": "Shield 1"},
        {"value": "static/shield2.svg", "img": "static/shield2.svg", "alt": "Shield 2", "checked": True},
        {"value": "static/shield3.svg", "img": "static/shield3.svg", "alt": "Shield 3"},
    ],
    "icons": [
        {"value": "static/icon1.svg", "img": "static/icon1.svg", "alt": "Lego brick", "checked": True},
        {"value": "static/icon2.svg", "img": "static/icon2.svg", "alt": "Diamond"},
        {"value": "static/icon3.svg", "img": "static/icon3.svg", "alt": "Speeding truck"},
        {"value": "static/icon4-2.svg", "img": "static/icon4-2.svg", "alt": "Horse"},
        {"value": "static/icon5.svg", "img": "static/icon5.svg", "alt": "Truck"},
        {"value": "static/icon6.svg", "img": "static/icon6.svg", "alt": "Turned Lego brick"},
    ],
    "icons_alternate": [
        {"value": "static/icon7.svg", "img": "static/icon7.svg", "alt": "3D printer 1"},
        {"value": "static/icon8.svg", "img": "static/icon8.svg", "alt": "3D printer 2"},
        {"value": "static/icon9.svg", "img": "static/icon9.svg", "alt": "Skull 1", "checked": True},
        {"value": "static/icon10.svg", "img": "static/icon10.svg", "alt": "Skull 2"},
    ],
}

options = {
    "crown-heads": common_options["crowns"],
    "crown-tails": common_options["crowns"],
    "icon-heads": common_options["icons_alternate"],
    "shield-tails": common_options["shields"],
    "upperleft-tails": common_options["icons"],
    "upperright-tails": common_options["icons"],
    "downleft-tails": common_options["icons"],
    "downright-tails": common_options["icons"],
}

app = Flask(__name__)

@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html", options=options)

@app.route("/generate", methods=["POST"])
def generate():
    """Generate coat of arms and coin based on selection in UI."""
    heads_crown_path = request.form["crown-heads"]
    heads_icon_path = request.form["icon-heads"]
    heads_laurels_path = request.form["sides-heads"]
    heads_text_left = request.form["text-heads-line1"]
    heads_text_right = request.form["text-heads-line2"]
    tails_crown_path = request.form["crown-tails"]
    tails_shield_path = request.form["shield-tails"]
    tails_laurels_path = request.form["sides-tails"]
    tails_text_left = request.form["text-tails-line1"]
    tails_text_right = request.form["text-tails-line2"]
    tails_upperleft_path = request.form["upperleft-tails"]
    tails_upperright_path = request.form["upperright-tails"]
    tails_downleft_path = request.form["downleft-tails"]
    tails_downright_path = request.form["downright-tails"]

    debug = request.form.get("debug", False)
    is_debug = debug == "on"


    # Paths for output files
    heads_svg = "output/coin-heads.svg"
    tails_svg = "output/coin-tails.svg"
    coat_of_arms_path = "output/coat_of_arms.svg"

    # Heads always have a single SVG as "head"
    elements.create_coin(heads_svg, heads_icon_path, heads_crown_path, heads_laurels_path, heads_text_left, heads_text_right, False, is_debug, False)
    # Tails always have a coat_of_arms (which is already scaled)
    elements.create_coat_of_arms(coat_of_arms_path, tails_shield_path, tails_upperleft_path, tails_upperright_path, tails_downleft_path, tails_downright_path)
    elements.create_coin(tails_svg, coat_of_arms_path, tails_crown_path, tails_laurels_path, tails_text_left, tails_text_right, True, is_debug, False)

    with open(heads_svg, "r") as f:
        heads_svg_content = f.read()

    with open(tails_svg, "r") as f:
        tails_svg_content = f.read()

    return jsonify({
        "heads": heads_svg_content,
        "tails": tails_svg_content
    })

@app.route("/download/<filename>")
def download(filename):
    """Route to download SVG files."""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(base_dir, "output", filename)
    files_in_output = os.listdir(os.path.join(base_dir, "output"))
    app.logger.debug(f"Files in output directory: {files_in_output}")
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({"error": f"File {filename} not found in output directory: {files_in_output}"}), 404

if __name__ == "__main__":
    app.run(debug=False)
