from PIL import Image
import os

root_folder = "plants_data/convert"  # adjust if needed

for subdir, dirs, files in os.walk(root_folder):
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg", ".png", ".svg")):
            input_path = os.path.join(subdir, file)

            # create output path (same folder, new format)
            output_path = os.path.splitext(input_path)[0] + ".webp"

            img = Image.open(input_path)

            # resize (important)
            img.thumbnail((800, 800))

            # convert to webp
            img.save(output_path, "WEBP", quality=80)

            print(f"Converted: {input_path} → {output_path}")

