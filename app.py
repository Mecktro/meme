import os
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def add_meme_text(image_path, top_text, bottom_text):
    """Adds text to an image and saves the result."""
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # Load font
    font_path = "static/impact.ttf"  # Make sure you have a font file
    font = ImageFont.truetype(font_path, 40)

    # Define text positions
    width, height = img.size
    top_position = (width // 2, 10)
    bottom_position = (width // 2, height - 60)

    # Draw text (centered)
    draw.text(top_position, top_text.upper(), font=font, fill="white", anchor="mt", stroke_width=2, stroke_fill="black")
    draw.text(bottom_position, bottom_text.upper(), font=font, fill="white", anchor="mb", stroke_width=2, stroke_fill="black")

    meme_path = os.path.join(UPLOAD_FOLDER, "meme.png")
    img.save(meme_path)
    return meme_path

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        file = request.files["file"]
        top_text = request.form["top_text"]
        bottom_text = request.form["bottom_text"]

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            # Process image
            meme_path = add_meme_text(file_path, top_text, bottom_text)
            return send_file(meme_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
