# Given the following directory structure
#   data-dir/
#   ├── stack1/{stack1_j}.png
#   ├── stack2/{stack2_j}.png
#   └── etc.
# Generate an .nrrd file for each stack<i>
#   and output it in `save-dir`

# Run in terminal with `python stack.py --data-dir "your/data/directory"

import os
from argparse import ArgumentParser
import concurrent.futures
from pathlib import Path
import skimage
import nrrd
import numpy as np


file_extension = 'png'

def process_stack(stack_dir, save_dir, verbose=False):
    
    save_path = save_dir / f"Group-scan_{stack_dir.name}.nrrd"
    
    image_paths = list(stack_dir.glob(f"*.{file_extension}"))
    # Ignore default images
    image_paths = [x for x in image_paths if 'spr' not in x.name and 'visual' not in x.name]
    image_paths.sort()
    
    if (verbose): print(f'{stack_dir.name}: Found {len(image_paths)} \'{file_extension}\' files')

    # Stack the images one by one
    stack = [skimage.io.imread(path, mode='L') for path in image_paths]
    stacked_images = np.stack(stack)
    
    if (verbose): print(f'{stack_dir.name}:  Done! Stacked data shape: {stacked_images.shape}')

    print(f'{stack_dir.name}: Writing .nrrd file to {save_path}')
    nrrd.write(str(save_path), stacked_images)

    if (verbose): print(f'{stack_dir.name}: Done!')


if __name__ == "__main__":
    parser = ArgumentParser("ForametCeTera - Construct 3D group-scan .nrrds from cross-sectional images.")
    parser.add_argument("--data-dir", type=Path, required=True, help="Path to where the folders containing .png cross-sections reside.")
    parser.add_argument("--save-dir", type=Path, default=None, help="Path to where the group-scan .nrrd files are saved. Defaults to data-dir.")
    args = parser.parse_args()
    
    if args.save_dir is None:
        args.save_dir = args.data_dir
    
    # Optionally exclude some directories you don't want to convert into group-scans
    #   by adding them to the `exclude` list
    exclude = []
    stack_dirs = []
    
    # Check which directories in data_dir contain >2 .png files
    print(f'Found the following directories that contain >2 .{file_extension} files')
    for directory in list(args.data_dir.iterdir()):
        if directory in exclude:
            continue
        
        generator = directory.glob(f'*.{file_extension}')
        try:
            for i in range(2):
                next(generator)
            stack_dirs.append(directory)
            print(directory)
        except:
            pass
    
    
    # ---------------------------------------------------------------------------- #
    #                IF YOU RUN INTO RAM ISSUES, LOWER max_workers!!               #
    # ---------------------------------------------------------------------------- #
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_stack, stack_dir, args.save_dir, verbose=True) for stack_dir in stack_dirs]
        
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")

