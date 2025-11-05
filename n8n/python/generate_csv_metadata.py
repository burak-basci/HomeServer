#!/usr/bin/env python3
"""
Generate CSV metadata for batch of images.
Creates generic AI art metadata for each image.
"""

import csv
import sys
from pathlib import Path

def generate_csv_metadata(images_dir: str, output_csv: str):
    """Generate CSV metadata for images in directory."""

    images_path = Path(images_dir)
    image_files = sorted([
        f.name for f in images_path.iterdir()
        if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.tiff', '.tif'}
    ])

    if not image_files:
        print(f"❌ No images found in {images_dir}")
        return False

    # Generic AI art metadata templates
    titles = [
        "Abstract Digital Art Background",
        "AI Generated Creative Pattern",
        "Modern Technology Concept Design",
        "Futuristic Digital Illustration",
        "Colorful Abstract Composition",
        "Geometric AI Art Pattern",
        "Creative Digital Background",
        "Abstract Technology Visualization",
        "Modern AI Generated Design",
        "Digital Art Creative Concept"
    ]

    keywords_sets = [
        "abstract,digital art,technology,background,modern,futuristic,colorful,artistic,creative,design",
        "ai generated,pattern,geometric,creative,modern,abstract,design,vibrant,colorful,innovative",
        "technology,innovation,digital,modern,concept,futuristic,abstract,business,creative,design",
        "abstract,digital,background,modern,colorful,artistic,design,creative,technology,pattern",
        "geometric,pattern,abstract,modern,design,creative,colorful,digital,art,background",
        "digital art,abstract,creative,modern,technology,design,colorful,futuristic,artistic,pattern",
        "modern,abstract,digital,technology,creative,design,colorful,background,artistic,concept",
        "ai art,digital,abstract,creative,modern,colorful,pattern,design,technology,background",
        "abstract,modern,digital,creative,technology,colorful,design,pattern,artistic,futuristic",
        "digital,abstract,modern,creative,technology,design,colorful,pattern,artistic,background"
    ]

    # Category 11 = Abstract
    category = 11

    print(f"Generating CSV metadata for {len(image_files)} images...")

    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Filename', 'Title', 'Keywords', 'Category'])
        writer.writeheader()

        for i, filename in enumerate(image_files):
            # Rotate through templates
            title = titles[i % len(titles)]
            keywords = keywords_sets[i % len(keywords_sets)]

            writer.writerow({
                'Filename': filename,
                'Title': title,
                'Keywords': keywords,
                'Category': category
            })

    print(f"✓ CSV metadata saved to: {output_csv}")
    print(f"✓ Generated metadata for {len(image_files)} images")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_csv_metadata.py <images_dir> <output_csv>")
        sys.exit(1)

    success = generate_csv_metadata(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)
