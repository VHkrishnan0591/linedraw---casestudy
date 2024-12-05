from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image,ImageDraw
from utils.strokesort import *
import utils.perlin
from utils.util import *
from utils import background_remover,watermark_adder
from utils import linedrawer
app = Flask(__name__)

# Initialize background remover
background_remover = background_remover.Backgroundremover()
watermark_adder = watermark_adder.Watermarkadder()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data_url = request.json.get('image')
    header, encoded = data_url.split(",", 1)
    image_data = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_data)).convert("RGBA")
    image = background_remover.remove_background(image)
    image = watermark_adder.watermark_at_top_right(image)
    sketcher = linedrawer.ImageSketcher()
    lines = sketcher.sketch(image)  # Directly pass the image to the sketch method
    # Create a new image to draw the lines on, based on the resolution from ImageSketcher
    disp = Image.new("RGB", (sketcher.resolution, sketcher.resolution * image.height // image.width), (255, 255, 255))
    draw = ImageDraw.Draw(disp)
    for l in lines:
        draw.line(l, (0, 0, 0), 5)

    # Save the image to a buffer
    buffered = BytesIO()
    disp.save(buffered, format="PNG")
    sketch_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    watermark_adder.print_watermark_info("output\out.svg")  # Print watermark information to console
    
    return jsonify({'linedraw': f"data:image/png;base64,{sketch_image_base64}",
                    'image': f"data:image/png;base64,{image}",})

if __name__ == '__main__':
    app.run(debug=True)
