#!/usr/bin/env python3
import os
import sys
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from PIL import Image

def main():
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set in .env")
        sys.exit(1)
        
    print("Initializing GenAI Client...")
    client = genai.Client(api_key=api_key)
    
    # Define prompt for the sticker
    prompt = (
        "Minimalist horizontal panoramic vinyl sticker decal design for the side of a camper van, "
        "flat solid matte black silhouette on a pure solid white background. "
        "Die-cut vector style, no gradients, no shading, clean outline edges. "
        "The layout is a continuous story from left (rear of van) to right (front of van) along a fluid ground line: "
        "\n1. Far left (high zone): Stylized mountain range silhouette defined by clean white hollow contour lines to lighten the solid black mass. "
        "At the foot of the mountains, a geometric forest of fir trees and the silhouette of a majestic stag (large deer) looking forward. "
        "\n2. Middle (action zone): The ground line slopes down in a smooth, fluid curve. On it is a sharp silhouette of a wildlife photographer crouching "
        "down with a tripod and a very long telephoto lens camera pointing forward. In front of the camera, a minimalist square camera viewfinder reticle [ ] "
        "surrounding an eagle in mid-flight. "
        "\n3. Far right (front, low zone): The ground line becomes very low and flat, transitioning into a minimalist wetland marsh with a few slender reeds, "
        "a tall standing heron silhouette, and ends on the far right with a flock of 3 wild ducks taking flight to taper off the sticker. "
        "\nTechnical requirements: Solid color matte black vinyl decal, flat design, thick clean cuttable vector lines (minimum 4mm line thickness for all thin parts like bird legs, reeds, tripod), "
        "high contrast, isolated on a pure white background."
    )
    
    print("\nPrompt being used for generation:")
    print("-" * 60)
    print(prompt)
    print("-" * 60)
    
    try:
        print("Sending request to Imagen 4 (imagen-4.0-generate-001)...")
        # Aspect ratios: "1:1", "3:4", "4:3", "9:16", "16:9"
        result = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=prompt,
            config=dict(
                number_of_images=1,
                aspect_ratio='16:9',
                output_mime_type='image/png',
            )
        )
        
        if not result.generated_images:
            print("Error: No images were generated.")
            sys.exit(1)
            
        print("Image generated successfully! Saving...")
        
        output_dir = Path("/Users/jchavauxm5/PKA_JCH/PHOTO/analyses")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / "panoramic_van_sticker_imagen3.png"
        
        for generated_image in result.generated_images:
            image_data = generated_image.image.image_bytes
            image = Image.open(BytesIO(image_data))
            image.save(output_path)
            print(f"Sticker saved to: {output_path}")
            
    except Exception as e:
        print(f"An error occurred during generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
