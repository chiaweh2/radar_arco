import os
import json
from glob import glob
import fsspec
from kerchunk.hdf import SingleHdf5ToZarr

project_directory = "special_projects/ard_radar/kerchunk/"
project_url = f"https://data.gdex.ucar.edu/{project_directory}"

# get file names from posix
posix_path = '/gdex/data/special_projects/ard_radar/kerchunk/'
cfradial1_files = glob(os.path.join(posix_path,'cfrad.*.nc'))
cfradial1_files = sorted(cfradial1_files)

for file in cfradial1_files :
    filename = os.path.basename(file)
    output_filename = filename.removesuffix('.nc')
    output_filename = output_filename+'.json'
    file_path = os.path.join('/lustre/desc1/scratch/chiaweih/SPol.precip/', output_filename)

    if os.path.exists(file_path):
       continue

    # Create kerchunk reference using fsspec
    remote_url = project_url + filename
    
    # Open file with fsspec
    with fsspec.open(remote_url, mode='rb') as f:
        # Generate kerchunk references
        h5chunks = SingleHdf5ToZarr(f, remote_url)
        refs = h5chunks.translate()
    
    # Save to JSON
    with open(file_path, 'w') as outf:
        json.dump(refs, outf)