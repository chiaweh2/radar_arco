import os
from glob import glob
from obstore.store import LocalStore
from virtualizarr.registry import ObjectStoreRegistry
from virtualizarr.parsers import HDFParser
from virtualizarr import open_virtual_dataset

project_directory = "/lustre/desc1/scratch/chiaweih/SPol.precip/chiaw112212/spol_moments_v2.0_20220525_000000/rhi/20220525/"
project_url = f"file://{project_directory}"
registry = ObjectStoreRegistry({project_url: LocalStore(prefix=project_directory)})
parser = HDFParser()

# get all cfradial1 files
cfradial1_files = glob(os.path.join(project_directory,'cfrad.*.nc'))
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
      url=project_url+filename,
      parser=parser,
      registry=registry,
    )

    # save to kerchunk json
    vds.vz.to_kerchunk(file_path, format='json')