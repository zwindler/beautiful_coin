from flask import Flask, render_template, request, send_file
import modules.elements as elements

app = Flask(__name__)

@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    """Generate coat of arms and coin based on selected crown."""
    crown_path = request.form["crown"]
    shield_path = request.form["shield"]
    coat_of_arms_path = "output/coat_of_arms.svg"
    coin_output_path = "output/coin.svg"

    # Call functions to generate SVGs
    elements.create_coat_of_arms(coat_of_arms_path, shield_path)
    elements.create_coin(coin_output_path, coat_of_arms_path, crown_path)

    return send_file(coin_output_path, mimetype="image/svg+xml")

if __name__ == "__main__":
    app.run(debug=True)
