import os
import glob
import logging
import pyart
import xradar as xd


def fix_string_encoding(ds):
    """
    Convert fixed-length unicode strings to object dtype for Zarr compatibility
    print out the variable names and their data types for debugging

    """
    ds = ds.copy()  # Create a mutable copy
    for var in ds.variables:
        if ds[var].dtype.kind == 'U':  # Unicode string
            logging.info(f"Variable '{var}' converted from {ds[var].dtype} {ds[var].dtype.kind}")
            ds[var] = ds[var].astype(str).astype(object)
            logging.info(f"to {ds[var].dtype}")
    return ds

if __name__ == "__main__":

    # setup constant


    # log file 
    logfile = os.path.join(os.path.dirname(__file__), 'create_cfradial2_zarr.log') 

    # Set up logging
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    

    project_directory = "/lustre/desc1/scratch/chiaweih/SPol.precip/chiaw112212/spol_moments_v2.0_20220525_000000/sur/20220525/"

    # get all cfradial1 files
    cfradial1_files = glob.glob(os.path.join(project_directory,'cfrad.*.nc'))
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

            ds_rad = pyart.io.read_cfradial(file)
            # ds_group = xr.open_dataset(file, group='sweep_0', engine='cfradial1', chunks={})
            continue

        # Apply to all nodes in the datatree
        dtree = dtree.map_over_datasets(fix_string_encoding)
        
        # Write to Zarr
        dtree.to_zarr(file_path)