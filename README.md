# radar_arco

Analysis-Ready Cloud-Optimized (ARCO) radar data workflows for CFRadial files using kerchunk and zarr.

## Overview

This repository demonstrates two approaches for creating analysis-ready radar data from CFRadial1 files:

1. **Kerchunk reference files** - Virtual datasets that reference original NetCDF files
2. **Zarr stores** - Cloud-optimized CFRadial2 format

## Notebooks

The `notebooks/` directory contains the main analysis workflows:

- **[radar_analysis_ready_data.ipynb](notebooks/radar_analysis_ready_data.ipynb)** - Demonstrates how to access and work with analysis-ready SPol radar data using both kerchunk and zarr approaches

## Installation

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

## Key Dependencies

- `xradar` - Radar data processing
- `kerchunk` - Virtual dataset creation
- `arm-pyart` - Python ARM Radar Toolkit
- `virtualizarr` - Virtual Zarr datasets
- `zarr` - Cloud-optimized data storage

## Data Access

Analysis-ready data is available at:
- **UCAR HPC (GLADE)**: `/gdex/data/special_projects/ard_radar/`
- **Remote access**: `https://data.gdex.ucar.edu/special_projects/ard_radar/`

## Development Scripts

The `test/` directory contains scripts for data conversion and processing workflows.

## License

BSD 3-Clause License. See [LICENSE](LICENSE) for details.
