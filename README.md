Note: This is a dummy repository  
# DEEPFRACK 
DeepFrack is a novel framework developed for enhancing energy efficiency and reducing latency in deep learning workloads executed on hardware accelerators. By optimally fusing layers and implementing an asymmetric tiling strategy, DeepFrack addresses the limitations of traditional layer-by-layer scheduling. The DeepFrack project aims to build succinct and simple framework that contributes to the ongoing efforts in designing more efficient hardware accelerators for machine learning workloads.  

DeepFrack is wrapper to [Timeloop](https://timeloop.csail.mit.edu/timeloop) written in python.

This document is to serve as a guide to users for installing and using DeepFrack. This document (along with the paper) will also provide any user with additional knowledge required to go through the complete source code of DeepFrack and suggest changes. For any queries please contact Mithil Pechimuthu (pechimuthumithil@iitgn.ac.in).  

![image](https://github.com/PechimuthuMithil/DeepFrack_temp/assets/119656326/ae79b3ce-aa0f-45d5-b8d6-ec0e7591f1f4)  

# Installation
## Dependencies
DeepFrack relies on Timeloop for it's cost metrics. Hence it is absolutely necessary for the user to have timeloop installed for running DeepFrack. One can find the the installation procedure and other useful information regarding the dependencies in the [Timeloop documentation](https://timeloop.csail.mit.edu/timeloop/installation).  

# Usage
## Generating costs
Run the script file for generating all the costs for all tiles.  

## Input and Output
### Inputs
Inputs to DeepFrack are gives as paths to the following files/folders  
1) The folder that contains the yaml files of every layer in the workload.  
2) The yaml file denoting the architcture specificatios of the accelerator.  
3) The yaml file describing the mapping constraints.
4) The json files that store all the tile costs.
5) Output folder name.

### Outputs
DeepFrack will output a final log file that will show the optimal tiling, and fusion along with the total energy consumed by fusion over layer by layer scheduling. 


