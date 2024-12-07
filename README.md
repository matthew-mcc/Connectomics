## Functional Brain Connectivity for Autism Spectrum Disorder ##

This repository contains a multitude of notebooks, downloaded data, parsed data, notes, images and scripts aimed at analyzing the ABIDE dataset. Although the important notebooks are commented and labeled, some extra code has been included as this project is still currently
a work in progress. There are many ideas present in this repository that did not work as expected, or different ways of doing things. They have been included, and will often be found as poorly-commented files, or large sections of notebooks that have been commented out 
completely. Below is a description of the important notebooks, and places to look for those who are interested.

__Directory Setup__

As this was part of a class, at the University of Calgary, there are some other notes and notebooks that are not directly related to this research. However, everything relevant to the exploration of _Functional Brain Connectivity for ASD_ is located in the `Research_Project`
directory. Below is a description of where to look for certain things.

_Data_
- Raw data is found in the `Data` and `Data_AAL` directories (raw time series, as Adjacency matrices).
- Processed data can be found in the `Binary_Notebooks` directory, in which we have Brodmann Area mapping and Binary Output.
- The `Binary_Output` directory contains network metrics and matrices for generated graphs for each participant, at varying thresholding values. Furthermore, there is an `Averaged` directory which contains the averaged values across all thresholds.
- We also have some misc. spreadsheets as output. If any data is not organized effectively into directories, it is likely an idea that was not used in the final research, and as such is not particularly relevant.

_Notebooks_
- Many file paths are non-localized, meaning that they pointed to somewhere else on a personal computer. This was particularly relevant for large files that could not make it into the repository on the cloud.
- Primary notebooks for this project include: `statistics.ipynb`, `generalNetworkStatistics.ipynb`, `binary_thresholding.ipynb`, `nullModels.ipynb`, `nonNodalResults.ipynb` and `alternativeApproach.ipynb`.
- Although this breaks some paths, I have collected the important notebooks and made copies of them, stored underneath the `PrimaryCode` directory. __This is the best place to start looking.__

  
__Notebooks & Scripts__

Below will be a short description of each of the above mentioned "Primary Notebooks".

`statistics`

This notebook handles various initial statistical tests and analysis for this project. Very few implementations were used for the final report, this was more of a workspace to try different things.

`generalNetworkStatistics`

This notebook handles all of the general network statistics, as well as comparisons with Null Models.

`binary_thresholding`

This notebook contains all of the relevant code for parsing the raw data and creating graphs and networks from them. Included here is also the thresholding process, and any little things that might have been required to ready our raw data for analysis.

`nullModels`

This notebook contains code for a variety of null models, and incomplete implementations of them. A few different null models were attempted, however, very few in this notebook are actually succesful.

`nonNodalResults`

This notebook contains statistical and general analysis of non-nodal (global) results. Many graphs, figures and tables are present in this notebook, attempting to gain insight into the averaged connectomes at a global scale.

`alternativeApproach`

This notebook contains the majority of the statistical tests and various analysis for individual regions. This is a nodal based approach, and contains many used and unused functions, cells, methods, etc... 
For all nodal-based results that are present in the report, this is where the code is located.

__Disclaimer__

As this is a work in progress, the directory setup and relevant code is not meant to be distributed and ready to use simply from cloning. Ideally this readme provides a decent summary of the repository, however, don't expect to be able to clone the repository and replicate
all of the results and findings. This is primarily apparent in the directories and file paths for various functions, as they have mutated and evolved over the course of this project.
