"""
Web Interface for Imagen 3 API Integration

This script provides a simple web interface for generating images using
Google's Imagen 3 model through the Gemini API.

Requirements:
- Flask
- All requirements from app.py

Usage:
1. Install Flask: pip install flask
2. Run the script: python web_interface.py
3. Open a browser and navigate to http://localhost:5000

For setup only (creates template files without running the server):
python web_interface.py --setup-only
"""

import os
import sys
import base64
from io import BytesIO
from datetime import datetime

# Check if we're just setting up templates
if len(sys.argv) > 1 and sys.argv[1] == "--setup-only":
    # Create template files only
    from web_interface_setup import create_template_files
    create_template_files()
    print("Template files created successfully.")
    sys.exit(0)

# Import Flask and other dependencies for normal operation
try:
    from flask import Flask, render_template, request, jsonify, send_from_directory
    from app import generate_images, save_images
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("If you're setting up the project, run: python web_interface.py --setup-only")
    print("Otherwise, install the required dependencies: pip install -r requirements.txt")
    sys.exit(1)

app = Flask(__name__)

# Create directories for templates, static files, and generated images
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("static/images", exist_ok=True)

# Create HTML template
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    """Handle image generation requests from the web interface."""
    try:
        # Get parameters from form
        prompt = request.form.get("prompt", "")
        number_of_images = int(request.form.get("number_of_images", 1))
        aspect_ratio = request.form.get("aspect_ratio", "1:1")
        safety_filter_level = request.form.get("safety_filter_level", None)
        person_generation = request.form.get("person_generation", "ALLOW_ADULT")
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        # Generate images
        images = generate_images(
            prompt=prompt,
            number_of_images=number_of_images,
            aspect_ratio=aspect_ratio,
            safety_filter_level=safety_filter_level,
            person_generation=person_generation
        )
        
        if not images:
            return jsonify({"error": "Failed to generate images"}), 500
        
        # Save images and prepare response
        saved_paths = save_images(images, prompt, output_dir="static/images")
        
        # Convert image paths to web URLs and create base64 previews
        result = []
        for i, path in enumerate(saved_paths):
            # Create a relative path for the web URL
            web_path = "/" + path.replace("\\", "/")
            
            # Create a base64 preview for immediate display
            image = BytesIO(images[i].image.image_bytes)
            base64_image = base64.b64encode(image.getvalue()).decode("utf-8")
            
            result.append({
                "path": web_path,
                "preview": f"data:image/png;base64,{base64_image}"
            })
        
        return jsonify({"images": result, "success": True})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/static/images/<path:filename>")
def serve_image(filename):
    """Serve generated images."""
    return send_from_directory("static/images", filename)

# Create the HTML template file
def create_template_files():
    """Create the necessary template files for the web interface."""
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Imagen 3 - Image Generator</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #1a73e8;
            text-align: center;
            margin-bottom: 30px;
        }
        .container {
            background-color: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
        }
        input[type="text"], select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        button {
            background-color: #1a73e8;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            display: block;
            margin: 20px auto;
            min-width: 200px;
        }
        button:hover {
            background-color: #1557b0;
        }
        button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
        .loading {
            text-align: center;
            margin: 20px 0;
            display: none;
        }
        .spinner {
            border: 4px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            border-top: 4px solid #1a73e8;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .results {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .image-card {
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        .image-card:hover {
            transform: translateY(-5px);
        }
        .image-card img {
            width: 100%;
            height: auto;
            display: block;
        }
        .image-card .actions {
            padding: 15px;
            display: flex;
            justify-content: space-between;
        }
        .image-card a {
            text-decoration: none;
            color: #1a73e8;
            font-weight: 500;
        }
        .error {
            color: #d93025;
            text-align: center;
            margin: 20px 0;
            padding: 10px;
            background-color: #fce8e6;
            border-radius: 4px;
            display: none;
        }
    </style>
</head>
<body>
    <h1>Imagen 3 - Image Generator</h1>
    
    <div class="container">
        <form id="generationForm">
            <div class="form-group">
                <label for="prompt">Prompt:</label>
                <input type="text" id="prompt" name="prompt" placeholder="Describe the image you want to generate..." required>
            </div>
            
            <div class="form-group">
                <label for="number_of_images">Number of Images:</label>
                <select id="number_of_images" name="number_of_images">
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="aspect_ratio">Aspect Ratio:</label>
                <select id="aspect_ratio" name="aspect_ratio">
                    <option value="1:1">1:1 (Square)</option>
                    <option value="3:4">3:4 (Portrait)</option>
                    <option value="4:3">4:3 (Landscape)</option>
                    <option value="9:16">9:16 (Vertical)</option>
                    <option value="16:9">16:9 (Widescreen)</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="safety_filter_level">Safety Filter Level:</label>
                <select id="safety_filter_level" name="safety_filter_level">
                    <option value="">Default</option>
                    <option value="BLOCK_LOW_AND_ABOVE">Block Low and Above</option>
                    <option value="BLOCK_MEDIUM_AND_ABOVE">Block Medium and Above</option>
                    <option value="BLOCK_ONLY_HIGH">Block Only High</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="person_generation">Person Generation:</label>
                <select id="person_generation" name="person_generation">
                    <option value="ALLOW_ADULT">Allow Adults</option>
                    <option value="DONT_ALLOW">Don't Allow People</option>
                </select>
            </div>
            
            <button type="submit" id="generateBtn">Generate Images</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Generating images... This may take a few moments.</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="results" id="results"></div>
    </div>

    <script>
        document.getElementById('generationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const form = this;
            const generateBtn = document.getElementById('generateBtn');
            const loading = document.getElementById('loading');
            const error = document.getElementById('error');
            const results = document.getElementById('results');
            
            // Clear previous results and errors
            results.innerHTML = '';
            error.style.display = 'none';
            
            // Show loading indicator
            loading.style.display = 'block';
            generateBtn.disabled = true;
            
            try {
                const formData = new FormData(form);
                
                const response = await fetch('/generate', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Failed to generate images');
                }
                
                // Display the generated images
                data.images.forEach(image => {
                    const card = document.createElement('div');
                    card.className = 'image-card';
                    
                    const img = document.createElement('img');
                    img.src = image.preview;
                    img.alt = 'Generated image';
                    
                    const actions = document.createElement('div');
                    actions.className = 'actions';
                    
                    const downloadLink = document.createElement('a');
                    downloadLink.href = image.path;
                    downloadLink.download = image.path.split('/').pop();
                    downloadLink.textContent = 'Download';
                    
                    const viewLink = document.createElement('a');
                    viewLink.href = image.path;
                    viewLink.target = '_blank';
                    viewLink.textContent = 'View Full Size';
                    
                    actions.appendChild(downloadLink);
                    actions.appendChild(viewLink);
                    
                    card.appendChild(img);
                    card.appendChild(actions);
                    
                    results.appendChild(card);
                });
            } catch (err) {
                error.textContent = err.message;
                error.style.display = 'block';
            } finally {
                loading.style.display = 'none';
                generateBtn.disabled = false;
            }
        });
    </script>
</body>
</html>
"""
    
    # Write the template file
    os.makedirs("templates", exist_ok=True)
    with open("templates/index.html", "w") as f:
        f.write(index_html)

if __name__ == "__main__":
    # Create template files if they don't exist
    if not os.path.exists("templates/index.html"):
        create_template_files()
    
    # Run the Flask app
    print("Starting web interface for Imagen 3 API...")
    print("Open your browser and navigate to http://localhost:5000")
    app.run(debug=True)
