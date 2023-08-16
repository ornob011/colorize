# Flask related imports
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy

# Image processing and utilities
import colorization.colorizers as colorizers
from colorization.colorizers import eccv16, load_img, preprocess_img, postprocess_tens
from PIL import Image
from skimage import color
import torch
import matplotlib.pyplot as plt
from io import BytesIO

# System and other utilities
import os
import uuid

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
db = SQLAlchemy(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Secret key for session management

# Database model for storing image information
class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(255), nullable=False)
    uuid_filename = db.Column(db.String(255), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Main route for uploading and processing images
@app.route('/', methods=['GET', 'POST'])
def hello():
    # Handle GET requests
    if request.method == 'GET':
        return render_template('index.html')
    
    # Handle POST requests
    if "file" not in request.files:
        return jsonify({"message": "File not uploaded."}), 400
    
    file = request.files['file']
    image = BytesIO(file.read())

    # Process the image
    colorizer = eccv16(pretrained=True).eval()
    img = load_img(image)
    tens_l_orig, tens_l_rs = preprocess_img(img, HW=(256,256))
    out_img = postprocess_tens(tens_l_orig, colorizer(tens_l_rs).cpu())

    # Save the processed image
    if not os.path.exists('imgs_out'):
        os.makedirs('imgs_out')
    filename = f"{uuid.uuid4()}.png"
    output_path = os.path.join('imgs_out', filename)
    plt.imsave(output_path, out_img)

    # Store image information in the database
    image_entry = ImageModel(original_filename=file.filename, uuid_filename=filename)
    db.session.add(image_entry)
    db.session.commit()

    return jsonify({
        "message": "Image processed successfully.",
        "image_url": f"/image/{image_entry.id}"
    })

# Route for fetching processed images
@app.route('/image/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = ImageModel.query.get(image_id)
    if image:
        return send_from_directory('imgs_out', image.uuid_filename, as_attachment=True)
    return "Image not found", 404

# Entry point
if __name__ == "__main__":
    app.run()
