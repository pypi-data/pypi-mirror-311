# test_annotations.py

from datavisor import VisorWriter, VisorReader
from datavisor import Config
from datavisor import AnnotationHandler

# Create a configuration for annotations
config = Config(
    data_type='annotation',
    max_entries_per_file=2000
)

# Create a VisorWriter for annotations
writer = VisorWriter(config, output_dir='./output')

# Create an AnnotationHandler
handler = AnnotationHandler(config)

# Process some .json files and write them to .visor files
import os
import glob
import json

# Replace this path with the path to your .json files
base_path = "/home/umar/Documents/code/packages/datavisor/samples"

# Get a list of all .json files in the directory
files_list = glob.glob(os.path.join(base_path, "*.json"))

entries = []
original_annotations = []

for path in files_list:
    with open(path, 'r') as f:
        annotation_data = json.load(f)
    # Assuming no OCR data; set to None or load if available
    ocr_data = None  # or load OCR data if you have it
    entry = handler.process(annotation_data, ocr_data)
    entries.append(entry)
    original_annotations.append(annotation_data)  # Keep original for verification

# Write entries to .visor files
writer.write_entries(entries)
writer.finalize()

print("Writing complete. Now reading...")

# Create a VisorReader
reader = VisorReader(metadata_file='./output/visor_metadata.json')

# Print summary of the dataset
reader.print_summary()

# Iterate over all entries and verify the data
for i, (original_annotation, entry) in enumerate(zip(original_annotations, reader)):
    if entry:
        print(f"Entry {i}:")
        print(f"Original Annotation Keys: {list(original_annotation.keys())}")
        print(f"Read Annotation Keys: {list(entry.annotation.keys())}")
        # Compare the original annotation with the one read from the file
        if original_annotation == entry.annotation:
            print("Annotation data matches.")
        else:
            print("Mismatch in annotation data!")
    else:
        print(f"Entry {i}: None")

print("Test complete.")
