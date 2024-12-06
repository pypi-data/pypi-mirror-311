import os
import time
from PIL import Image
import json
import io
from io_ops import VisorReader
import random
import subprocess
from tqdm import tqdm

def clear_cache():
    try:
        subprocess.run(["sudo", "sh", "-c", "echo 3 > /proc/sys/vm/drop_caches"], check=True)
    except subprocess.CalledProcessError:
        print("Warning: Failed to clear OS cache. Make sure you have sudo privileges.")

def process_image(img):
    # Perform more intensive image processing
    img = img.copy()
    img = img.resize((100, 100))
    img = img.convert('L')  # Convert to grayscale
    return img

def read_individual_files(samples_folder):
    start_time = time.time()
    total_word_count = 0
    file_count = 0
    
    image_files = [f for f in os.listdir(samples_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    for filename in tqdm(image_files, desc="Processing individual files"):
        img_path = os.path.join(samples_folder, filename)
        json_path = os.path.join(samples_folder, os.path.splitext(filename)[0] + '.json')
        
        with Image.open(img_path) as img:
            processed_img = process_image(img)
        
        try:
            with open(json_path, 'r') as f:
                ocr_data = json.load(f)
            total_word_count += len(ocr_data.get('ocr_data', []))
        except FileNotFoundError:
            print(f"Warning: JSON file not found for {filename}")
        
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
        with Image.open(io.BytesIO(entry.data)) as img:
            processed_img = process_image(img)
        
        total_word_count += len(entry.ocr_data)
        file_count += 1
    
    end_time = time.time()
    return end_time - start_time, total_word_count, file_count

def run_test(test_func, *args):
    times = []
    for i in range(1):
        clear_cache()
        time.sleep(1)
        print(f"\nRun {i+1}/5:")
        result = test_func(*args)
        times.append(result[0])
    return min(times), result[1], result[2]

def main():
    samples_folder = './../samples'
    output_folder = './output'
    
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
    speedup = individual_time / visor_time
    print(f"\nSpeedup (Visor vs Individual): {speedup:.2f}x")
    
    if results["Individual files"][1] != results["Visor format"][1]:
        print("Warning: Word counts differ between methods. Results may not be directly comparable.")
    
    if results["Individual files"][2] != results["Visor format"][2]:
        print("Warning: File counts differ between methods. Results may not be directly comparable.")

if __name__ == "__main__":
    main()