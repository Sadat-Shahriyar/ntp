from pdf2image import convert_from_path
import os

# Path to your PDF
pdf_path = "./paper_1.pdf"

# Directory to save images
output_dir = "pdf_images"
os.makedirs(output_dir, exist_ok=True)

# Convert PDF to a list of PIL Image objects
pages = convert_from_path(pdf_path, dpi=300)  # 300 dpi = good quality

# Save each page as an image
for i, page in enumerate(pages):
    image_path = os.path.join(output_dir, f"page_{i+1}.png")
    page.save(image_path, "PNG")
    print(f"Saved {image_path}")

print(f"\n✅ Done! All pages saved to: {output_dir}")
