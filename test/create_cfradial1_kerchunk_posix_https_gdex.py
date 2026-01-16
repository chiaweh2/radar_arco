"""
Create kerchunk posix json files for all cfradial1 files in gdex ard_radar project

- The json files will be in the scratch space first
- The posix json files will have suffix .posix.json
- The https json files will have suffix .https.json (text replacement from posix to https)
- The sudo cp is needed to move the files to gdex

"""

import os
from glob import glob
from obstore.store import LocalStore
from virtualizarr.registry import ObjectStoreRegistry
from virtualizarr.parsers import HDFParser
from virtualizarr import open_virtual_dataset


project_directory = "/gdex/data/special_projects/ard_radar/kerchunk/"
scratch_directory = "/lustre/desc1/scratch/chiaweih/SPol.precip/chiaw112212/spol_moments_v2.0_20220525_000000/rhi/20220525/"
project_url = f"file://{project_directory}"
registry = ObjectStoreRegistry({project_url: LocalStore(prefix=project_directory)})
parser = HDFParser()

# get all cfradial1 files
cfradial1_files = glob(os.path.join(project_directory,'cfrad.*.nc'))
cfradial1_files = sorted(cfradial1_files)

for file in cfradial1_files :

    filename = os.path.basename(file)
    output_filename = filename.removesuffix('.nc')
    output_filename_posix = output_filename+'.posix.json'
    output_filename_https = output_filename+'.https.json'
    file_path_posix = os.path.join(scratch_directory, output_filename_posix)
    file_path_https = os.path.join(scratch_directory, output_filename_https)

    # start with posix json
    if os.path.exists(file_path_posix):
        continue

    # create virtual dataset
    vds = open_virtual_dataset(
      url=project_url+filename,
      parser=parser,
      registry=registry,
    )

    # save to kerchunk json
    vds.vz.to_kerchunk(file_path_posix, format='json')

    # convert to https json
    with open(file_path_posix, 'r', encoding='utf-8') as f:
        content = f.read()
        # Replace both escaped and unescaped versions
        content = content.replace('\\/gdex\\/data\\/', 'https:\\/\\/data.gdex.ucar.edu\\/')
        content = content.replace('/gdex/data/', 'https://data.gdex.ucar.edu/')
        # save https json
        with open(file_path_https, 'w', encoding='utf-8') as outf:
            outf.write(content)

    # copy posix json from scratch to gdex
    os.system(f'sudo -u gdexdata cp {file_path_posix} {project_directory}')
    # copy https json from scratch to gdex
    os.system(f'sudo -u gdexdata cp {file_path_https} {project_directory}')

    # clean up scratch
    os.remove(file_path_posix)
    os.remove(file_path_https)
