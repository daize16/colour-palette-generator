from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import re, os
from dotenv import load_dotenv
import numpy as np
import cv2
from sklearn.cluster import KMeans
import tempfile

# Load environment variables
load_dotenv()

api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
CORS(app)

# ===== Mood palette using Gemini AI =====
def get_palette(prompt):
    try:
        response = model.generate_content(
            f"Generate a 5-color palette (hex codes only) for the theme: {prompt}. Return only the hex codes, comma-separated."
        )
        text = response.text
        codes = re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}", text)
        return codes[:5]
    except Exception as e:
        print("Gemini error", e)
        return []

# ===== Image palette extraction =====
def extract_palette(image_path, num_colors=5):
    img = cv2.imread(image_path)
    if img is None:
        return []
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (200, 200))
    pixels = img.reshape((-1, 3))
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    colors = np.round(kmeans.cluster_centers_).astype(int)
    hex_codes = ['#%02x%02x%02x' % tuple(color) for color in colors]
    return hex_codes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    theme = data.get("theme", "").strip()
    if not theme:
        return jsonify({"error": "Theme is required"}), 400
    
    colours = get_palette(theme)
    return jsonify({"palette": colours})

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    file = request.files['image']
    suffix = os.path.splitext(file.filename)[1] or ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        file.save(tmp)
        tmp_path = tmp.name
    colours = extract_palette(tmp_path)
    os.remove(tmp_path)
    return jsonify({"palette": colours})

if __name__ == "__main__":
    app.run(debug=True)
