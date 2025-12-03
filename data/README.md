# `data` folder readme

This folder contains input data, intermediate files, and final outputs. It stores both manually and automatically downloaded census tables, as well as lookup files. All generated outputs will be saved here.

## Usage
- Set up this folder inline with the instructions in the [main ReadMe.md](https://github.com/ONSgeo/Area_Classification/blob/main/README.md) before running the pipeline.
- Once set up, API downloaded data, intermediate data files and outputs will automatically be saved to this folder.
- File paths for intermediate data files, output and plots paths in the [`config.yaml`](https://github.com/ONSgeo/Area_Classification/blob/main/area_classification/config.yaml) have been updated to point towards this folder. 

**Important:**  
The .gitignore file has been configured to exclude all contents of this folder from version control. This means any files placed here will not be tracked by Git. Do not manually add or commit data from this folder, as it is intended to remain outside the repository.

## Support
For questions about data management, refer to the project documentation or contact the code owners.
