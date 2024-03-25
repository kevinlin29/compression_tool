import argparse
import os
from tqdm import tqdm
import py7zr

def decompress_arw_files(archive_path, destination_path):
    """
    Decompresses the LZMA archive and extracts the ARW files to the specified destination.
    """
    with py7zr.SevenZipFile(archive_path, 'r') as archive:
        archive.extractall(path=destination_path)
    print(f"Extracted files to {destination_path}")


def compress_arw_files(arw_files, destination_path, archive_name="compressed_arw.7z"):
    """
    Compresses multiple ARW files into a single LZMA archive.
    """
    output_file = os.path.join(destination_path, archive_name)
    with py7zr.SevenZipFile(output_file, 'w') as archive:
        for arw_file in arw_files:
            archive_name = os.path.basename(arw_file)
            archive.writeall({archive_name: arw_file})
    return output_file

def find_arw_files(directory):
    """
    Returns a list of ARW files in the specified directory.
    """
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith('.arw')]

def main():
    parser = argparse.ArgumentParser(description="Compress or decompress ARW files.")
    parser.add_argument("mode", type=str, choices=["compress", "decompress"], help="Operation mode: compress or decompress ARW files.")
    parser.add_argument("source_dir", type=str, help="Directory containing ARW files to compress or the directory to save extracted files.")
    parser.add_argument("destination_dir", type=str, help="Directory to save the compressed archive or the path of the LZMA archive to decompress.")

    args = parser.parse_args()

    if args.mode == "compress":
        # Ensure destination directory exists
        os.makedirs(args.destination_dir, exist_ok=True)

        # Find all ARW files in the source directory
        arw_files = find_arw_files(args.source_dir)

        if not arw_files:
            print("No ARW files found in the source directory.")
            return

        # Compress all ARW files into a single archive
        print("Compressing files...")
        archive_path = compress_arw_files(arw_files, args.destination_dir)
        print(f"All files compressed into {archive_path}")
    elif args.mode == "decompress":
        # Decompress the specified archive
        print("Decompressing files...")
        decompress_arw_files(args.destination_dir, args.source_dir)
        print("Decompression completed.")

if __name__ == "__main__":
    main()
