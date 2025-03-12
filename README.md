# Imagen 3 API Integration

This project provides a simple interface to generate images using Google's Imagen 3 model through the Gemini API. It demonstrates how to connect to the API, generate images with various parameters, and save the results.

## Overview

Imagen 3 is Google's highest quality text-to-image model, featuring a number of new and improved capabilities:

- Generate images with better detail, richer lighting, and fewer distracting artifacts
- Understand prompts written in natural language
- Generate images in a wide range of formats and styles
- Render text more effectively than previous models

**Note:** Imagen 3 is only available on the Gemini API Paid Tier.

## Project Structure

- `app.py` - Main application for generating images
- `imagen3_documentation.md` - Comprehensive documentation about Imagen 3
- `.env` - Environment file for storing your API key
- `requirements.txt` - List of required Python packages
- `example_usage.py` - Example script demonstrating how to use the app.py module
- `test_setup.py` - Script to test your environment setup without generating images
- `web_interface.py` - Simple web interface for generating images through a browser

## Installation

### Automatic Setup

For a quick setup, you can use the provided setup scripts:

- **Linux/macOS**:
  ```bash
  chmod +x setup.sh
  ./setup.sh
  ```

- **Windows**:
  ```
  setup.bat
  ```

These scripts will:
- Check if Python and pip are installed
- Optionally create a virtual environment
- Install required dependencies
- Prompt for your Gemini API key
- Run the test setup to verify everything is working

### Manual Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Gemini API key:
   - Get your API key from [Google AI Studio](https://makersuite.google.com/)
   - Edit the `.env` file and replace `your_api_key_here` with your actual API key
   
4. Verify your setup:
   ```bash
   python test_setup.py
   ```

## Usage

### Basic Usage

Generate an image with a simple prompt:

```bash
python app.py "A serene mountain landscape at sunset"
```

### Advanced Options

The script supports various parameters for customizing image generation:

```bash
python app.py "A futuristic cityscape with flying cars" --number 2 --aspect "16:9" --display
```

### Available Parameters

- `--number`, `-n`: Number of images to generate (1-4, default: 1)
- `--aspect`, `-a`: Aspect ratio of generated images (choices: "1:1", "3:4", "4:3", "9:16", "16:9", default: "1:1")
- `--safety`, `-s`: Safety filter level (choices: "BLOCK_LOW_AND_ABOVE", "BLOCK_MEDIUM_AND_ABOVE", "BLOCK_ONLY_HIGH")
- `--people`, `-p`: Allow generation of people (choices: "DONT_ALLOW", "ALLOW_ADULT", default: "ALLOW_ADULT")
- `--display`, `-d`: Display images after generation (if supported by environment)

### Help

For more information about available options:

```bash
python app.py --help
```

### Web Interface

The project includes a simple web interface for generating images through your browser:

1. Start the web server:
   ```bash
   python web_interface.py
   ```

2. Open your browser and navigate to http://localhost:5000

3. Enter your prompt and configure generation parameters through the web form

4. Generated images will be displayed in the browser and saved to the `static/images` directory

### Testing Your Setup

Before generating images, you can verify your environment setup:

```bash
python test_setup.py
```

This script checks:
- Required packages are installed
- The .env file is properly configured
- Your API key is valid
- A connection to the Gemini API can be established

No images are generated during this test, so no API usage is incurred.

### Using as a Module

You can also use the functionality in your own Python scripts:

```python
from app import generate_images, save_images

# Generate images
images = generate_images(
    prompt="Your prompt here",
    number_of_images=2,
    aspect_ratio="16:9"
)

# Save the generated images
save_paths = save_images(images, "Your prompt here")
```

See `example_usage.py` for a complete example.

### Direct API Usage

If you prefer to use the Google Generative AI API directly, here's the correct implementation:

```python
import google.generativeai as genai
from PIL import Image

# Configure the API
genai.configure(api_key='YOUR_GEMINI_API_KEY')

# Create an image generation model
model = genai.ImageGenerationModel('imagen-3.0-generate-002')

# Generate images
response = model.generate_images(
    prompt='Your prompt here',
    number_of_images=1,
    aspect_ratio="1:1",
    person_generation="ALLOW_ADULT"
)

# Process the generated images
for image in response:
    # Display the image
    image.show()
    
    # Or save it:
    image.save('generated_image.png')
```

**Note:** The API implementation has been updated to use the correct methods available in the `google-generativeai` package version 0.8.3. The previous implementation using `from google import genai` and `genai.Client()` is not compatible with the current package.

## Generated Images

All generated images are saved in the `generated_images` directory with filenames that include a timestamp and a sanitized version of the prompt.

## Documentation

For more detailed information about Imagen 3 and its capabilities, refer to the `imagen3_documentation.md` file in this repository.

## Resources

- [Imagen Prompt Guide](https://ai.google.dev/gemini-api/docs/imagen-prompt-guide)
- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Getting Started with Imagen notebook](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_imagen.ipynb)
- [Gemini Cookbook](https://github.com/google-gemini/cookbook)
