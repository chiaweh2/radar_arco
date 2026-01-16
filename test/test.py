import xradar as xd
files = ['/lustre/desc1/scratch/chiaweih/SPol.precip/chiaw112212/spol_moments_v2.0_20220525_000000/rhi/20220525/cfrad.20220525_015443.665_to_20220525_015709.985_SPOL_PrecipRhi2_RHI.nc']
xd.io.open_cfradial1_datatree(files[0],engine='h5netcdf')