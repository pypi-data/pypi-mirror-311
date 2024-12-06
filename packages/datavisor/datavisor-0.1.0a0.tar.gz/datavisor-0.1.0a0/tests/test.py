from io_ops import VisorWriter, VisorReader
from config import Config, ImageDimensions, Entry, EntryMetadata
from data_handler import ImageHandler

# Create a configuration
config = Config(
    data_type='image',
    # image_dimensions=ImageDimensions(width=240, height=240),
    max_entries_per_file=2000
)

# Create a VisorWriter
writer = VisorWriter(config, output_dir='./output')

# Create an ImageHandler
handler = ImageHandler(config)

# Process some images and write them to .visor files
import os
import glob

base_path = "/home/umar/Documents/code/packages/datavisor/samples"

files_list = glob.glob(os.path.join(base_path, "*.jpg"))

entries = []
for path in files_list:
    with open(path, 'rb') as f:
        image_data = f.read()
    # Simulating OCR data (replace this with actual OCR if available)
    ocr_data = [["word1"], ["word2"], ["word3"],["word1"], ["word2"], ["word3"],["word1"], ["word2"], ["word3"],["word1"], ["word2"], ["word3"],["word1"], ["word2"], ["word3"],["word1"], ["word2"], ["word3"],["word1"], ["word2"], ["word3"],["word1"], ["word2"], ["word3"]]  # Example OCR data
    entry = handler.process(image_data, path, ocr_data)
    entries.append(entry)

writer.write_entries(entries)
writer.finalize()

print("Writing complete. Now reading...")

# Create a VisorReader
reader = VisorReader(metadata_file='./output/visor_metadata.json')

# Print summary of the dataset
reader.print_summary()

# Iterate over all entries
for i, entry in enumerate(reader):
    if entry:
        print(entry.ocr_data)
        print(f"Entry {i}: Image: {entry.metadata.original_name}, Size: {entry.dimensions.width}x{entry.dimensions.height}, Word count: {entry.metadata.word_count}")
    else:
        print(f"Entry {i}: None")

# Try to get a specific entry
entry_5 = reader.get_entry(4)  # Remember, indexing starts at 0
if entry_5:
    print(f"5th entry: {entry_5.metadata.original_name}")
else:
    print("5th entry not found")

# Get metadata for the last entry
last_index = len(reader) - 1
metadata_last = reader.get_metadata(last_index)

if metadata_last:
    print(f"Metadata for last entry: {metadata_last}")
else:
    print("Metadata for last entry not found")

print("Test complete.")