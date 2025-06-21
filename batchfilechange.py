import os

def batch_rename_files(directory):
    # Walk through all files in directory and subdirectories
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Check if file ends with .dex
            if filename.endswith('.dex'):
                # Create new filename by replacing .dex with .png
                new_filename = filename[:-4] + '.png'
                
                # Get full file paths
                old_file = os.path.join(root, filename)
                new_file = os.path.join(root, new_filename)
                
                # Rename the file
                try:
                    os.rename(old_file, new_file)
                    print(f'Renamed: {filename} -> {new_filename}')
                except OSError as e:
                    print(f'Error renaming {filename}: {e}')

if __name__ == '__main__':
    directory = '/Users/hongtang/Downloads/archive (1)/'
    batch_rename_files(directory)
    print('Batch rename complete!')
