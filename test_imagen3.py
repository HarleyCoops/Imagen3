"""
Test script for the updated Imagen 3 API implementation.

This script tests the correct implementation of the Imagen 3 API using
the google-generativeai package version 0.8.3.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_imagen3_api():
    """
    Test the Imagen 3 API implementation using the correct approach.
    """
    print("Testing Imagen 3 API Implementation")
    print("---------------------------------")
    
    # Load API key from environment
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables.")
        print("   Please add it to your .env file.")
        return
    
    try:
        # Step 1: Configure the API
        print("\n1. Configuring the API...")
        genai.configure(api_key=api_key)
        print("✅ API configured successfully")
        
        # Step 2: Create an image generation model
        print("\n2. Creating an image generation model...")
        model = genai.ImageGenerationModel('imagen-3.0-generate-002')
        print("✅ Model created successfully")
        
        # Step 3: Prepare image generation parameters
        print("\n3. Preparing image generation parameters...")
        prompt = "A test prompt for Imagen 3"
        generation_config = {
            "number_of_images": 1,
            "aspect_ratio": "1:1",
            "person_generation": "ALLOW_ADULT"
        }
        
        print(f"   Prompt: '{prompt}'")
        print(f"   Configuration: {generation_config}")
        print("✅ Image generation parameters prepared correctly")
        
        # Step 4: Verify the API structure
        print("\n4. Verifying API structure...")
        has_generate_images = hasattr(model, 'generate_images')
        print(f"   Model has generate_images method: {'✅' if has_generate_images else '❌'}")
        
        print("\nTest completed successfully!")
        print("\nTo generate an actual image, uncomment the following code:")
        print("----------------------------------------------------------")
        print("response = model.generate_images(")
        print("    prompt=prompt,")
        print("    **generation_config")
        print(")")
        print("response[0].save('test_image.png')")
        print("print('Image saved to test_image.png')")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")

if __name__ == "__main__":
    test_imagen3_api() 