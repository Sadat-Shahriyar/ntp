import os
import re
import torch
import shutil
from datetime import datetime
from PIL import Image
from pathlib import Path
from datasets import load_dataset
from pdf2image import convert_from_path
from huggingface_hub import hf_hub_download
from transformers import NougatProcessor, VisionEncoderDecoderModel


def get_time_string():
    now = datetime.now()
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    return str(timestamp_str)

time_str = get_time_string()

# Path to your PDF
pdf_path = "./docurag.pdf"

# Directory to save images
output_dir = "pdf_images"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir, exist_ok=True)

# Convert PDF to a list of PIL Image objects
pages = convert_from_path(pdf_path, dpi=300)  # 300 dpi = good quality

# Save each page as an image
for i, page in enumerate(pages):
    image_path = os.path.join(output_dir, f"page_{i+1}.png")
    page.save(image_path, "PNG")
    print(f"Saved {image_path}")

print(f"\n✅ Done! All pages saved to: {output_dir}")

# print(os.listdir(output_dir))
# exit()

# Images to latex:

output_folder = "latex_out"
os.makedirs(output_folder, exist_ok=True)

image_files = os.listdir(output_dir)

image_files = sorted(
    image_files,
    key=lambda x: os.path.getmtime(os.path.join(output_dir, x))
)

print(image_files)

processor = NougatProcessor.from_pretrained("facebook/nougat-base")
model = VisionEncoderDecoderModel.from_pretrained("facebook/nougat-base")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

pathlib_path = Path(pdf_path)
file_stem_name = pathlib_path.stem

file_to_write_path = f"{output_folder}/{time_str}output_{file_stem_name}.md"
if os.path.exists(file_to_write_path):
    os.remove(file_to_write_path)

file_to_write = open(file_to_write_path, "a", encoding="utf-8")


for page_images_path in image_files:
    file_path = output_dir + "/" + page_images_path
    image = Image.open(file_path).convert("RGB")
    pixel_values = processor(image, return_tensors="pt").pixel_values
    outputs = model.generate(
        pixel_values.to(device),
        min_length=1,
        max_new_tokens=3000,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
    )

    sequence = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    sequence = processor.post_process_generation(sequence, fix_markdown=False)
    file_to_write.write(sequence)

    print(f"converted {file_path}")