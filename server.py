from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__)

# Directory where uploaded files will be stored
UPLOAD_FOLDER = r'C:\Users\FAJJOS\OneDrive\Desktop\Raspberry'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def calculate_brightness(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Calculate the histogram of pixel intensities
    hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
    # Calculate the cumulative distribution function (CDF) of the histogram
    cdf = hist.cumsum()
    # Normalize the CDF
    cdf_normalized = cdf / cdf[-1]
    # Find the brightness threshold that separates darker and lighter regions
    brightness_threshold = np.argmax(cdf_normalized > 0.5)
    # Calculate the average brightness
    brightness = np.mean(gray_image)
    # Convert numpy int64 to regular Python integers
    brightness = int(brightness)
    brightness_threshold = int(brightness_threshold)
    return brightness, brightness_threshold

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        # Read the uploaded image
        image = cv2.imread(save_path)

        # Calculate image brightness and brightness threshold
        brightness, brightness_threshold = calculate_brightness(image)

        # Determine whether the image is dark or light based on the fixed threshold
        threshold = 100
        if brightness < threshold and brightness_threshold < threshold:
            brightness_status = "dark"
        else:
            brightness_status = "light"

        # Print the brightness status on the server side
        print(f"Image '{filename}' brightness: {brightness}, threshold: {brightness_threshold}, status: {brightness_status}")

        return jsonify({"message": f"File {filename} uploaded successfully",
                        "brightness": brightness,
                        "threshold": threshold,
                        "status": brightness_status}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
