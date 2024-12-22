from flask import Flask, render_template, request, jsonify
import modules.elements as elements

app = Flask(__name__)

@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    """Generate coat of arms and coin based on selection in UI."""
    heads_crown_path = request.form["crown"]
    heads_icon_path = request.form["icon-heads"]
    heads_laurels_path = request.form["sides-heads"]
    tails_crown_path = request.form["crown-tails"]
    tails_shield_path = request.form["shield-tails"]
    tails_laurels_path = request.form["sides-tails"]
    debug = request.form.get("debug", False)
    is_debug = debug == "on"


    # Paths for output files
    heads_svg = "output/coin-heads.svg"
    tails_svg = "output/coin-tails.svg"
    coat_of_arms_path = "output/coat_of_arms.svg"

    # Heads always have a single SVG as "head"
    elements.create_coin(heads_svg, heads_icon_path, heads_crown_path, heads_laurels_path, is_debug)
    # Tails always have a coat_of_arms
    elements.create_coat_of_arms(coat_of_arms_path, tails_shield_path)
    elements.create_coin(tails_svg, coat_of_arms_path, tails_crown_path, tails_laurels_path, is_debug)

    with open(heads_svg, "r") as f:
        heads_svg_content = f.read()

    with open(tails_svg, "r") as f:
        tails_svg_content = f.read()

    return jsonify({
        "heads": heads_svg_content,
        "tails": tails_svg_content
    })

if __name__ == "__main__":
    app.run(debug=True)
