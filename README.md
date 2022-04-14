# live_cams
A gui to get the live views from Basler cameras in the lab

## Installation from source
Here are the instructions to install the program from source using Anaconda to resolve the dependencies.

 * Download [Miniconda](https://docs.conda.io/en/latest/miniconda.html) if you do not already have it.
 * Clone this repository
 ```
 $ git clone git@github.com:TammeWollweber/Live_cams.git
 $ cd Live_cams
 ```
 * Create a conda environment using the environment.yml file provided:
   ```
   $ conda env create -f environment.yml
   $ conda activate live_cams
   ```
 * You can now run the program directly by running `./run_local`
 * Alternately, you can add the current snapshot to your environment using
   ```
   $ pip install -e .
   ```
   The executable `live_cams` will then be available in your path.
