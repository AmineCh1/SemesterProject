
# README 

## Renderer Interface
### Dependencies
This program requires Python, PyQt5, VTK, and PCL.
### Example Run 
```
python Renderer.py
```
### Comments 
This program allows you to process contents on the fly and render them on a display area on the right for better comparison. 
It is then possible to store the resulting contents in either ply or vtk in a folder of your choice. 


## Projections generator
### Dependencies
This program requires VTK and Python, and ffmpeg.
### Example Run
For info, execute the following command:
```
python projections.py -h 
```
Example:
```
python projections.py reference.ply distorted.ply icoK 1 off 
```
### Comments
This program captures projected views of the model with respect to the specified parameters. 


## Experiment
### Dependencies
This program requires Python, PyQt5, and VTK.
### Example Run
```
python SubjExpLauncher.py
```
### Comments 
This program launches an experiment session. It reads batch files from the Batches folder, and stores the results in the Results folder per subject. It requires that the contents to be assessed are at the root of the SubjExp.py and SubjExpLauncher.py files. Also, changing the batch file currently read and the sticker order can be easily done by editing two lines of code that are mentioned inside the file SubjExp.py

## Statistical Analysis notebook
For completeness, a jupyter notebook where the data processing was done from the results of the experiment is provided.(HTML and ipynb versions)



