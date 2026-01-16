import os
from glob import glob
from obstore.store import HTTPStore
from virtualizarr.registry import ObjectStoreRegistry
from virtualizarr.parsers import HDFParser
from virtualizarr import open_virtual_dataset

project_directory = "special_projects/ard_radar/kerchunk/"
project_url_root = "https://data.gdex.ucar.edu/"
project_url = f"{project_url_root}{project_directory}"
registry = ObjectStoreRegistry({project_url: HTTPStore(url=project_url)})
parser = HDFParser()

# get all cfradial1 files
cfradial1_files = glob(os.path.join('/gdex/data/',project_directory,'cfrad.*.nc'))
cfradial1_files = sorted(cfradial1_files)

for file in cfradial1_files :
    filename = os.path.basename(file)
    output_filename = filename.removesuffix('.nc')
    output_filename = output_filename+'.json'
    file_path = os.path.join(project_directory, output_filename)

    if os.path.exists(file_path):
       continue

    # create virtual dataset
    vds = open_virtual_dataset(
      url=project_url_root+project_directory+filename,
      parser=parser,
      registry=registry,
    )

    # save to kerchunk json
    vds.vz.to_kerchunk(file_path, format='json')