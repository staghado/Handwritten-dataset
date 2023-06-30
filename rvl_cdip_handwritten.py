import os
import zipfile
from PIL import Image

# Extract the contents of the zip file
zip_path = './RVL_CDIP_small.zip'
extract_path = '.'

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# Find the 'handwritten' folder
handwritten_folder = os.path.join(extract_path, 'data', 'handwritten')

# Create the output folder
output_folder = os.path.join(extract_path, 'RVL_CDIP_handwritten')
os.makedirs(output_folder, exist_ok=True)

# Convert TIF files to JPG
tif_files = [f for f in os.listdir(handwritten_folder) if f.endswith('.tif')]
for tif_file in tif_files:
    tif_path = os.path.join(handwritten_folder, tif_file)
    jpg_file = os.path.splitext(tif_file)[0] + '.jpg'
    jpg_path = os.path.join(output_folder, jpg_file)

    # Open the TIF image and convert to JPG
    tif_image = Image.open(tif_path)
    tif_image.save(jpg_path, 'JPEG')

# Clean up the extracted folder if desired
# os.remove(zip_path)
# shutil.rmtree(extract_path)



import numpy as np
import cv2

def distortion_free_resize(image, img_size):
    h, w = img_size

    # Resize the image while preserving aspect ratio
    aspect_ratio = image.shape[1] / image.shape[0]
    new_width = int(aspect_ratio * h)
    image = cv2.resize(image, (new_width, h))

    # Check the amount of padding needed
    pad_height = h - image.shape[0]
    pad_width = w - image.shape[1]

    # Calculate padding amounts for top, bottom, left, and right
    pad_height_top = pad_height // 2
    pad_height_bottom = pad_height - pad_height_top
    pad_width_left = pad_width // 2
    pad_width_right = pad_width - pad_width_left

    # Pad the image with random noise
    image = np.pad(image, ((pad_height_top, pad_height_bottom), (pad_width_left, pad_width_right), (0, 0)), mode='constant', constant_values=np.random.randint(0, 256, size=(2,)))

    # Transpose and flip the image
    # image = np.transpose(image, (1, 0, 2))
    # image = np.fliplr(image)

    return image
