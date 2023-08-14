import os
from tqdm import tqdm

import stackUtil

# root_dir = r'E:\Scans Joost Luijmes'
# stack_dirs = os.listdir(root_dir)

# exclude = [
# 'γ1.2__Rec', 
# 'A2.2__Rec', 
# 'B2.2__Rec', 
# 'D2.2__Rec', 
# 'θ2.2__Rec', 
# 'B3.2__Rec', 
# 'E1.2__Rec', 
# 'A1.2__Rec', 
# 'B1.3__Rec', 
# ]
# stack_dirs = [x for x in stack_dirs if x not in exclude]

# print(stack_dirs)

# quit()

stack_dirs = [
    r'C:\Users\Joost\Desktop\D1.2__Rec',
    r'C:\Users\Joost\Desktop\θ1.2__Rec'
]

for stack_dir in tqdm(stack_dirs):
    # full_path = os.path.join(root_dir, stack_dir)
    full_path = stack_dir
    full_out = os.path.join(full_path, f'{stack_dir}.nrrd')
    
    print(full_path)
    
    stackUtil.main(full_path, full_out)