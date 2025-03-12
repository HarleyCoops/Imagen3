"""
Example Usage of Imagen 3 API Integration

This script demonstrates how to use the app.py module to generate images
with Imagen 3 in your own Python applications.
"""

from app import generate_images, save_images, display_images

def main():
    """
    Example function demonstrating how to use the Imagen 3 API integration.
    """
    print("Imagen 3 API Integration Example")
    print("--------------------------------")
    
    # Example 1: Basic image generation
    prompt = "A colorful hot air balloon floating over a mountain range at sunrise"
    print(f"\nExample 1: Generating an image with prompt: '{prompt}'")
    
    images = generate_images(prompt)
    if images:
        save_paths = save_images(images, prompt)
        print(f"Successfully saved {len(save_paths)} image(s)")
    
    # Example 2: Customized image generation
    prompt = "A futuristic robot playing chess in a cyberpunk city"
    print(f"\nExample 2: Generating images with custom parameters and prompt: '{prompt}'")
    
    images = generate_images(
        prompt=prompt,
        number_of_images=2,
        aspect_ratio="16:9",
        person_generation="DONT_ALLOW"
    )
    
    if images:
        save_paths = save_images(images, prompt)
        print(f"Successfully saved {len(save_paths)} image(s)")
        
        # Uncomment to display images (if environment supports it)
        # display_images(images)

if __name__ == "__main__":
    main()
