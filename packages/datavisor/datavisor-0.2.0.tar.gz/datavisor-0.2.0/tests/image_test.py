import os
import time
from PIL import Image
import json
import io
from datavisor import (
    VisorReader,
    VisorWriter,
    ConfigBuilder,
    ImageEntry,
    AnnotEntry,
    ImageHandler,
    AnnotationHandler,
)



import random
from tqdm import tqdm

def process_image(img):
    # Perform more intensive image processing
    img = img.copy()
    img = img.resize((100, 100))
    img = img.convert('L')  # Convert to grayscale
    return img

def process_annotation(annotation):
    # Simulate processing of annotation data
    # For the purpose of this test, we'll just pass
    pass

def create_visor_files(samples_folder, output_folder):
    # Build configuration
    config_builder = ConfigBuilder()
    config = (
        config_builder
        .set_data_type('image')
        .set_max_entries_per_file(100)
        .build()
    )

    # Create handlers
    image_handler = ImageHandler(config)
    annot_handler = AnnotationHandler(config)

    entries = []

    files = os.listdir(samples_folder)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    annot_files = [
        f for f in files
        if f.lower().endswith('.json') and os.path.splitext(f)[0] not in [os.path.splitext(img)[0] for img in image_files]
    ]

    # Process image files
    for filename in image_files:
        img_path = os.path.join(samples_folder, filename)
        json_path = os.path.join(samples_folder, os.path.splitext(filename)[0] + '.json')

        with open(img_path, 'rb') as img_file:
            img_data = img_file.read()

        try:
            with open(json_path, 'r') as f:
                ocr_data = json.load(f).get('ocr_data', [])
        except FileNotFoundError:
            ocr_data = []

        # Process image data into ImageEntry
        image_entry = image_handler.process(img_data, filename, ocr_data)
        entries.append(image_entry)

    # Process annotation files
    for filename in annot_files:
        json_path = os.path.join(samples_folder, filename)
        with open(json_path, 'r') as f:
            annotation_data = json.load(f)
        # Process annotation data into AnnotEntry
        annot_entry = annot_handler.process(annotation_data)
        entries.append(annot_entry)

    # Write entries to Visor files
    writer = VisorWriter(config, output_folder)
    writer.write_entries(entries)
    writer.finalize()

def read_individual_files(samples_folder):
    start_time = time.time()
    total_word_count = 0
    file_count = 0

    files = os.listdir(samples_folder)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    annot_files = [
        f for f in files
        if f.lower().endswith('.json') and os.path.splitext(f)[0] not in [os.path.splitext(img)[0] for img in image_files]
    ]

    # Process image files
    for filename in tqdm(image_files, desc="Processing individual image files"):
        img_path = os.path.join(samples_folder, filename)
        json_path = os.path.join(samples_folder, os.path.splitext(filename)[0] + '.json')

        with Image.open(img_path) as img:
            processed_img = process_image(img)

        try:
            with open(json_path, 'r') as f:
                ocr_data = json.load(f).get('ocr_data', [])
            total_word_count += len(ocr_data)
        except FileNotFoundError:
            print(f"Warning: JSON file not found for {filename}")
        file_count += 1

    # Process annotation files
    for filename in tqdm(annot_files, desc="Processing individual annotation files"):
        json_path = os.path.join(samples_folder, filename)
        with open(json_path, 'r') as f:
            annotation_data = json.load(f)
            process_annotation(annotation_data)
            total_word_count += len(annotation_data)
        file_count += 1

    end_time = time.time()
    return end_time - start_time, total_word_count, file_count

def read_visor_files(output_folder):
    start_time = time.time()
    total_word_count = 0
    file_count = 0

    metadata_file = os.path.join(output_folder, 'visor_metadata.json')
    reader = VisorReader(metadata_file)

    for entry in tqdm(reader, desc="Processing Visor files", total=len(reader)):
        if isinstance(entry, ImageEntry):            
            with Image.open(io.BytesIO(entry.data)) as img:
                processed_img = process_image(img)
            total_word_count += len(entry.ocr_data)
            file_count += 1
        elif isinstance(entry, AnnotEntry):
            process_annotation(entry.annotation)
            total_word_count += len(entry.annotation)
            file_count += 1
        else:
            print(f"Unknown entry type: {type(entry)}")

    end_time = time.time()
    return end_time - start_time, total_word_count, file_count

def run_test(test_func, *args):
    times = []
    for i in range(1):
        time.sleep(1)
        print(f"\nRun {i+1}/1:")
        result = test_func(*args)
        times.append(result[0])
    return min(times), result[1], result[2]

def main():
    samples_folder = './samples'
    output_folder = './output'

    # First, create Visor files from samples
    create_visor_files(samples_folder, output_folder)

    tests = [
        ("Individual files", lambda: run_test(read_individual_files, samples_folder)),
        ("Visor format", lambda: run_test(read_visor_files, output_folder))
    ]

    random.shuffle(tests)

    results = {}
    for name, test_func in tests:
        print(f"\nTesting: {name}")
        best_time, word_count, file_count = test_func()
        results[name] = (best_time, word_count, file_count)
        print(f"{name}: {best_time:.4f} seconds, {word_count} words, {file_count} files")

    individual_time = results["Individual files"][0]
    visor_time = results["Visor format"][0]
    speedup = individual_time / visor_time if visor_time > 0 else float('inf')
    print(f"\nSpeedup (Visor vs Individual): {speedup:.2f}x")

    if results["Individual files"][1] != results["Visor format"][1]:
        print("Warning: Word counts differ between methods. Results may not be directly comparable.")

    if results["Individual files"][2] != results["Visor format"][2]:
        print("Warning: File counts differ between methods. Results may not be directly comparable.")

if __name__ == "__main__":
    main()
