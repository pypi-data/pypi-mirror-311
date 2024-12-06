import os
import json

def create_sample_jsons(folder_path, sample_text):
    # Get all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # For each image file, create a corresponding JSON file
    for image_file in image_files:
        # Create the data for this image
        data = {
            "ocr_data": sample_text.split()  # Split the text into words
        }

        # Create the JSON file name (same as image file but with .json extension)
        json_file_name = os.path.splitext(image_file)[0] + '.json'
        json_file_path = os.path.join(folder_path, json_file_name)

        # Write the data to the JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    print(f"Created {len(image_files)} JSON files in: {folder_path}")

if __name__ == "__main__":
    # Specify the folder containing the images
    image_folder = "/home/umar/Documents/code/packages/datavisor/samples"

    # Specify the sample text to use for all images
    sample_text = "This is a sample text for OCR data. It contains multiple words and will be the same for all images."

    # Create the sample JSON files
    create_sample_jsons(image_folder, sample_text)