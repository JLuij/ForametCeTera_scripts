# import tifffile as tf
from collections import defaultdict
import imageio
import nrrd
import numpy as np

import os
import glob

def main(tiff_stack_path = None, nrrd_output_path = None, scaling = 1.0, show_preview = False):
    ## Change these paths to your relevant directories
    # tiff_stack_path = r'path/to/directory/with/tiff stack'
    # nrrd_output_path = r'path/to/output.nrrd'

    file_extension = r'.png'
    tiff_paths = glob.glob(os.path.join(tiff_stack_path, '*' + file_extension))
    tiff_paths = [x for x in tiff_paths if '000' in x]
    print(f'Found {len(tiff_paths)} \'{file_extension}\' files')

    # Stack the images one by one
    print('Stacking...', end='')
    try:
        stack = [np.array(imageio.imread(path, mode='L')) for path in tiff_paths]
        stacked_images = np.stack(stack)
    except Exception as e:
        print(e)
        shape_count = defaultdict(int)
        for i in stack:
            shape_count[i.shape] += 1
        for k, v in shape_count.items():
            print(f'{k}: {v}')
        min_count = min(shape_count.values())
        min_shape_name = [idx for idx, x in enumerate(stack) if x.shape == min_count]
        print(min_shape_name)
        print(tiff_paths[min_shape_name])
        
    print(f' Done! Stacked data shape: {stacked_images.shape}')


    # Optionally show a preview
    # show_preview = True
    if show_preview:
        import matplotlib.pyplot as plt
        
        shape = stacked_images.shape
        plt.imshow(stacked_images[shape[0]//2, :, :])
        plt.show()
        plt.imshow(stacked_images[:, shape[1]//2, :])
        plt.show()

    # Optionally downsize the volume. `scaling` < 1 downsizes the volume e.g. 0.5 halves the
    #   volume shape. NOTE: by default, spline interpolation will be applied
    # scaling = 0.5
    if scaling != 1.0:
        from scipy.ndimage import zoom
        
        print(f'Resizing as provided scaling != 1 but {scaling}...', end='')
        
        ## Uses spline interpolation by default (order=3)
        stacked_images = zoom(stacked_images, scaling, order=3)
        print(f' Done! Stacked data shape is now: {stacked_images.shape}')

    print(f'Writing .nrrd file to {nrrd_output_path}')
    nrrd.write(nrrd_output_path, stacked_images)

    print('Done!')

    del stack
    del stacked_images