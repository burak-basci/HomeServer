#!/usr/bin/env python3
"""
Generate Adobe Stock metadata CSV for uploaded images.
"""
import os
import csv
import sys

def generate_metadata(images_dir, output_csv):
    """Generate metadata CSV for images in directory."""

    # Get list of image files
    images = []
    for filename in sorted(os.listdir(images_dir)):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff', '.tif')):
            images.append(filename)

    if not images:
        print(f"No images found in {images_dir}")
        return 1

    print(f"Found {len(images)} images")

    # Adobe Stock categories (from adobe_stock.md)
    # Using generic categories for AI-generated content
    CATEGORIES = {
        'abstract': 8,      # Graphic Resources
        'landscape': 11,    # Landscape
        'technology': 19,   # Technology
        'lifestyle': 12,    # Lifestyle
        'business': 3,      # Business
    }

    # Generate CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow(['Filename', 'Title', 'Keywords', 'Category'])

        # Generate metadata for each image
        for idx, filename in enumerate(images, 1):
            # Generic AI-generated image metadata
            title = f"AI Generated Abstract Digital Art {idx}"

            # Keywords (up to 49 allowed)
            keywords = "ai generated, artificial intelligence, digital art, abstract, modern, contemporary, creative, artistic, computer generated, neural network, deep learning, machine learning, futuristic, technology, digital, illustration, graphic design, background, pattern, colorful, vibrant"

            # Use Technology category (19) as default for AI-generated content
            category = CATEGORIES['technology']

            writer.writerow([filename, title, keywords, category])

    print(f"✓ Metadata CSV generated: {output_csv}")
    print(f"  - {len(images)} images")
    print(f"  - Ready for Adobe Stock upload")

    return 0


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python generate_metadata.py <images_dir> <output_csv>")
        sys.exit(1)

    images_dir = sys.argv[1]
    output_csv = sys.argv[2]

    sys.exit(generate_metadata(images_dir, output_csv))
