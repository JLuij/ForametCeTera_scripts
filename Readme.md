## Scripts used in the paper ForametCeTera, a novel CT scan dataset to expedite classification research of (non-)foraminifera
By Joost Luijmes, Tristan van Leeuwen and Willem Renema

### Installation
**Pre-requisites** \
An installation of conda (e.g. by installing miniconda)

**Instructions** 
- Clone this repository in your preferred way 
- Create a conda environment using the included `environment.yml` by navigating to the cloned repository in the command line and running `conda env create -f environemt.yml`
- Run the scripts in the `ForametCeTera` conda environment
<br>
<br>
  
`stack.py` is a script that can be run on the command line:
```
$ python stack.py --data-dir /path/to/Reconstruction/specimen/ 
```
`segment.ipynb` and `technical_validation.ipynb` are interactive files.


<br>
<br>
<br>

A screenshot made in [3D slicer software](https://www.slicer.org/) of > 63 intensity values of specimens of ForametCeTera. Use the provided scripts to segment the data at different intensity thresholds.
![Preview of the dataset specimens (intensity values > 63 only)](<Assets/Dataset specimens preview.png>)
