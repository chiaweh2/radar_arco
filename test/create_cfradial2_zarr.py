import os
from glob import glob
import pyart         # needed for xradar in my env for some reason ()
import xradar as xd


def fix_string_encoding(ds):
    """Convert fixed-length unicode strings to object dtype for Zarr compatibility"""
    ds = ds.copy()  # Create a mutable copy
    for var in ds.variables:
        if ds[var].dtype.kind == 'U':  # Unicode string
            ds[var] = ds[var].astype(str).astype(object)
    return ds

if __name__ == "__main__":
    project_directory = "/lustre/desc1/scratch/chiaweih/SPol.precip/chiaw112212/spol_moments_v2.0_20220525_000000/rhi/20220525/"

    # get all cfradial1 files
    cfradial1_files = glob(os.path.join(project_directory,'cfrad.*.nc'))
    cfradial1_files = sorted(cfradial1_files)

    for file in cfradial1_files :
        filename = os.path.basename(file)
        output_filename = filename.removesuffix('.nc')
        output_filename = output_filename+'.zarr'
        file_path = os.path.join(project_directory, output_filename)

        if os.path.exists(file_path):
            continue
        
        # Read CFRadial1 file
        try:
            dtree = xd.io.open_cfradial1_datatree(file)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue

        # Apply to all nodes in the datatree
        dtree = dtree.map_over_datasets(fix_string_encoding)
        
        # Write to Zarr
        dtree.to_zarr(file_path)