# Senior-year-project
Some Quantum Optical Experiments with Single Photons and FPGA Programming

Folder 1: Final Data

This folder contains the data we collected in the lab for our final run. All the related counts are stored in '.txt' files
with appropriate file names. Along with these you will find some '.py' files named (mostly) 'post_collection.py' and
'datermine_state.py'. These files contain Python codes to perform the required calculations and generate the required graphs
for the relevant experiment.

Folder 2: Codes

Sub-folder 1: Troubleshoot

This folder contains the Python codes that can simulate the results/graphs based on theoretical predictions. 'state_prediction.py'
will give the predicted state when a photon passes through a certain, static configuration of optical elements, while
'state_prediction_with_rotation.py' will  give the graphs that one should expect when one of the components is rotated. Any
behaviour different than the prediction is an anomaly and the experimental apparatus (especially the waveplates) should be tested. 

Sub-fodler 2: FPGA

This folder contains the two main files required for FPGA programming.

- The 'rs232coincidencecounter.v' file contains all the path/circuit information. This code is written for an FPGA working at 
100 Mhz and all the sync has been done according to that. An FPGA with a different clock speed will require some changes in this
file. These changes are simple and can easily be done by following the comments in the 'rs232coincidencecounter.v' file.

- 'counts_constraints.xdc' is a constraint file that detemines the input and output ports of the FPGA. Every FPGA has different
names for each port/pin, and so will have a different '.xdc' file. The names of ports/pins can be found in the usermanual of the
FPGA. One may make changes to this specific file or create a new '.xdc' file. Vivado has an interactive menu that makes detemining
these constraints easier. 

- Once you get the '.v' and '.xdc' files right and run them through all the required steps in Vivado, you will get a '.bit' file.
This file must be burnt on the FPGA for it to start working.

Sub-folder 3: PDC

This folder contains the Python code for Photo-detection Counter (PDC). PDC is a simply software with a GUI specifically designed
for data collection in single-photon laboratories. All the sample results present in 'Final Data' folder have been acquired using
PDC. The code has been thoroughly commented and users can easily make changes to any part of the code to suit their needs.

						--- IMPORTANT NOTES FOR PDC ---

-> PDC will only work properly with Spyder that comes with Anaconda distribution. PDC uses the Python's serial library 'pyserial'
that can only be used with Anaconda installed. We tried running it with VS Code and a standalone installation of Spyder and
they don't work properly. Latest version of Anaconda can be downloaded from this link: https://www.anaconda.com/products/distribution

-> PDC looks for a 32-bit long header to start data communication. This is like a oneway handshake that must be done to make sure we
are receiving the correct data. Make sure that you send the required header after every set of registered counts. Currently
this header has been set to '10011001100010010101010101011101'. Changing this header will require changes in both the PDC and
'.v' file in sub-folder 2.

-> Make sure you have updated drivers for your serial communication device.

Contact

- For any queries or help feel free to contact me at bilal.hyder@lums.edu.pk

						
						--- Happy counting :D ---
