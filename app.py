"""
Imagen 3 API Integration

This script provides a simple interface to generate images using Google's Imagen 3 model
through the Gemini API. It demonstrates how to connect to the API, generate images with
various parameters, and save the results.

Requirements:
- google-generativeai
- python-dotenv
- Pillow (PIL)

Usage:
1. Set up your GEMINI_API_KEY in the .env file
2. Run the script with a prompt: python app.py "your prompt here"
3. Optional parameters can be specified (see --help for details)
"""

import os
import argparse
import sys
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from io import BytesIO

# Create output directory if it doesn't exist
OUTPUT_DIR = "generated_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_api():
    """
    Configure the Gemini API using the API key from environment variables.
    
    Raises:
        ValueError: If the API key is not found or invalid
    """
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in environment variables. "
            "Please add it to your .env file."
        )
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
    except Exception as e:
        raise ValueError(f"Failed to configure Gemini API: {e}")

def generate_images(
    prompt, 
    number_of_images=1, 
    aspect_ratio="1:1", 
    safety_filter_level=None, 
    person_generation="ALLOW_ADULT"
):
    """
    Generate images using Imagen 3 model via the Gemini API.
    
    Args:
        prompt (str): Text prompt for the image generation
        number_of_images (int, optional): Number of images to generate (1-4). Defaults to 1.
        aspect_ratio (str, optional): Aspect ratio of the generated images. 
            Options: "1:1", "3:4", "4:3", "9:16", "16:9". Defaults to "1:1".
        safety_filter_level (str, optional): Safety filter level. 
            Options: "BLOCK_LOW_AND_ABOVE", "BLOCK_MEDIUM_AND_ABOVE", "BLOCK_ONLY_HIGH". 
            Defaults to None.
        person_generation (str, optional): Allow generation of people. 
            Options: "DONT_ALLOW", "ALLOW_ADULT". Defaults to "ALLOW_ADULT".
    
    Returns:
        list: List of generated image objects
        
    Raises:
        Exception: If image generation fails
    """
    try:
        # Configure the API
        setup_api()
        
        # Validate parameters
        if not 1 <= number_of_images <= 4:
            raise ValueError("number_of_images must be between 1 and 4")
            
        valid_aspect_ratios = ["1:1", "3:4", "4:3", "9:16", "16:9"]
        if aspect_ratio not in valid_aspect_ratios:
            raise ValueError(f"aspect_ratio must be one of {valid_aspect_ratios}")
            
        valid_person_generation = ["DONT_ALLOW", "ALLOW_ADULT"]
        if person_generation not in valid_person_generation:
            raise ValueError(f"person_generation must be one of {valid_person_generation}")
        
        # Configure generation parameters
        generation_config = {
            "number_of_images": number_of_images,
            "aspect_ratio": aspect_ratio,
            "person_generation": person_generation
        }
        
        # Add safety filter if specified
        if safety_filter_level:
            valid_safety_levels = ["BLOCK_LOW_AND_ABOVE", "BLOCK_MEDIUM_AND_ABOVE", "BLOCK_ONLY_HIGH"]
            if safety_filter_level not in valid_safety_levels:
                raise ValueError(f"safety_filter_level must be one of {valid_safety_levels}")
            generation_config["safety_filter_level"] = safety_filter_level
        
        # Create an image generation model
        model = genai.ImageGenerationModel('imagen-3.0-generate-002')
        
        # Generate images
        print(f"Generating {number_of_images} image(s) with prompt: '{prompt}'")
        response = model.generate_images(
            prompt=prompt,
            **generation_config
        )
        
        return response
    
    except Exception as e:
        print(f"Error generating images: {e}")
        return None

def save_images(images, prompt, output_dir=OUTPUT_DIR):
    """
    Save generated images to disk with timestamp and prompt-based filename.
    
    Args:
        images (list): List of generated image objects
        prompt (str): The prompt used to generate the images
        output_dir (str, optional): Directory to save images. Defaults to OUTPUT_DIR.
    
    Returns:
        list: Paths to saved image files
    """
    if not images:
        return []
    
    # Create a timestamp and sanitize the prompt for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_prompt = "".join(c if c.isalnum() else "_" for c in prompt)[:30]
    
    saved_paths = []
    for i, image_data in enumerate(images):
        # Create filename with timestamp, sanitized prompt, and index
        filename = f"{timestamp}_{sanitized_prompt}_{i+1}.png"
        filepath = os.path.join(output_dir, filename)
        
        # Save the image
        image_data.save(filepath)
        saved_paths.append(filepath)
        print(f"Image saved to {filepath}")
    
    return saved_paths

def display_images(images):
    """
    Display generated images (if running in an environment that supports it).
    
    Args:
        images (list): List of generated image objects
    """
    if not images:
        return
    
    for image_data in images:
        try:
            image_data.show()
        except Exception as e:
            print(f"Error displaying image: {e}")

def main():
    """
    Main function to parse command line arguments and run the image generation.
    """
    parser = argparse.ArgumentParser(description="Generate images using Google's Imagen 3 model")
    
    parser.add_argument("prompt", type=str, help="Text prompt for image generation")
    parser.add_argument(
        "--number", "-n", type=int, default=1, 
        help="Number of images to generate (1-4, default: 1)"
    )
    parser.add_argument(
        "--aspect", "-a", type=str, default="1:1",
        choices=["1:1", "3:4", "4:3", "9:16", "16:9"],
        help="Aspect ratio of generated images (default: 1:1)"
    )
    parser.add_argument(
        "--safety", "-s", type=str, 
        choices=["BLOCK_LOW_AND_ABOVE", "BLOCK_MEDIUM_AND_ABOVE", "BLOCK_ONLY_HIGH"],
        help="Safety filter level (default: None)"
    )
    parser.add_argument(
        "--people", "-p", type=str, default="ALLOW_ADULT",
        choices=["DONT_ALLOW", "ALLOW_ADULT"],
        help="Allow generation of people (default: ALLOW_ADULT)"
    )
    parser.add_argument(
        "--display", "-d", action="store_true",
        help="Display images after generation (if supported by environment)"
    )
    
    args = parser.parse_args()
    
    # Generate images
    generated_images = generate_images(
        args.prompt,
        number_of_images=args.number,
        aspect_ratio=args.aspect,
        safety_filter_level=args.safety,
        person_generation=args.people
    )
    
    if not generated_images:
        print("No images were generated. Please check your API key and parameters.")
        return 1
    
    # Save images
    saved_paths = save_images(generated_images, args.prompt)
    
    # Display images if requested
    if args.display:
        display_images(generated_images)
    
    print(f"Successfully generated and saved {len(saved_paths)} image(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
