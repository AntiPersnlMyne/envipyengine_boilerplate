# envipyengine_boilerplate
Boilerplate abstraction class for the Python interface of ENVI (envipyengine) by nv5geospatialsoftware.

## Motivation
During my undergrad senior project, I was motivated to utilize ENVI software to aid with processing historical manuscripts. There are two main options for using ENVI headless: 1) IDL 2) Python. NV5 provides their own Python library - ENVI Py Engine - which is conveinent. 

What is NOT conveinent is how minimal the documentation for the library is:
`https://envi-py-engine.readthedocs.io/en/latest/envipyengine_api.html`

**However**, one isn't not _supposed_ to use this library as a standalone entity. Its intended purpose is as a tool being used by the `ENVI Modeler` (a feature within ENVI itself) to convert ENVI "block code" into a Python executable. Should you still desire to use this library manually, carry on.

## Contents
This repository includes two main objects:
1) An approachable guide on how to use ENVI Py Engine, for those unfamiliar with IDL and/or ENVI
2) A boilerplate class - named `Task` - that provides an easy(er) interface to the Envi Py Engine

## Disclaimer
There is a very minimal chance this will be updated past ver. `1.0`. The ENVI Py Engine has been updated recently (as of writing, 2025), but contains fractional ENVI capabilities, compared to pure IDL routines. It is the author's recommendation to use IDL via `idlpy` (a complimentary IDL-Python bridge included with your (probable) installation of ENVI). Or use the Envi Modeler from within ENVI itself.



# How ENVI Py Engine works
The ENVI Py Engine supports "class" based programming, meaning each task (ENVI's name for a function) is its own object.
The idea: You create a task object, then set properties on it

Example on executing a 2% Linear Stretch Task:

```python
import envi_task # Boilerplate class
import cv2       # OPTIONAL: Display image

# Create task parameters
stretch_params = dict(
  PERCENT=[2.0], # range: 0-50.0
  BRIGHTNESS=50  # range: 0-100
)

# Set task object
stretch_task = Task("LinearPercentStretchRaster", stretch_params)

# Create ENVI readable input file (raster) out of image
stretch_task.set_inputRaster("./baboon.png")

# Execute task
stretch_task.task_execute()

# OPTIONAL: Display image
image_path = stretch_task.getOutputRasterURL()
image = cv2.imread(image_path)

cv2.imshow("2% Linear Stretch", image)
cv2.waitKey(0)
```

### Setting up a task
Setting which ENVI task you want to execute requires passing in a string to the Task class. The string is the name of the task, defined by ENVI. To find a total list of tasks and their names, execute the following:

```python
import envi_task # Boilerplate class
blank_task = Task()
blank_task.task_list()
```

This prints the names of all tasks ENVI Py Engine can perform. Copy the name from the console into your code.
Example setting Task to do Forward PCA Transform:

```python
import envi_task # Boilerplate class
blank_task = Task()
blank_task.task_list()

blank_task.set_taskName("ForwardPCATransform")

# Or, declare the task object with the taskname

pca_task = Task("ForwardPCATransform")
```


### Setting a task's parameters
Some tasks have additional parameters. ENVI Py Engine does not allow for traditional arguments to be passed (e.g., add(arg1, arg2)). Instead, ENVI Py Engine expects Python dictionary variables containing all of the parameters' names and their values. 

To find out what parameters a task takes, there's three methods (#2 is most reliable):
1) Search for your task here (`https://www.nv5geospatialsoftware.com/docs/routines-159.html`), and scroll down to the "Properties" section. Each property labeled "required" must be in your task parameters dictionary. Properies not labeled required are optional, and ENVI will provide default values.  
2) Open ENVI software. In ENVI 6.1 (and similar editions), go to the "Toolbox" and search "Run Task". Search for your task (e.g., Linear Percent Stretch Raster). Click the black dropdown arrow next to "OK", and click "Save Parameter Values...". Opening that exported file will reveal all of the parameters ENVI expects from a task, and more importantly, the datatype Python will expect them in.
3) After creating a task object WITH a task name, run `task.task_parameters()`. This is ENVI Py Engine's built-in help menu for parameters.


### Input / Output rasters
A raster is an image file format that ENVI utilizes. The only difference is that rasters are type dict(ionary), and have metadata attached. The important part of a raster is its "URL" field, which is its filepath on your local machine. This allows you to treat it like a normal image file (e.g., displaying the image with cv2.imread). 

The Task class allows you to set an input raster with an image's filepath (URL) or with a raster object (as ENVI tasks will output).

Example using filepath:
```python
import envi_task # Boilerplate class

pca_task = Task("ForwardPCATransform")
pca_task.set_inputRaster("./baboon.png")
```

Example using raster object:
```python
import envi_task # Boilerplate class

stretch_params = dict(
  PERCENT=[2.0], 
  BRIGHTNESS=50 
)
stretch_task = Task("LinearPercentStretchRaster", stretch_params)
stretch_task.task_execute()

pca_task = Task("ForwardPCATransform")
pca_task.set_inputRaster(stretch_task.getOutputRaster())
```


### Task execution and getting results
After setting all parameters, executing the task is as simple as `task.task_execute()`. 

There's two main results you'd want to extract: 
1) The raster (as input for another task)
2) The raster URL (image file path)

Note: If you perform a DiceByRaster - which splits up a raster into sub-tiles (e.g., DiceRasterByPixel) - and wish to perform tasks on each sub-raster, to store all sub rasters: 
`subtile_out_rasters = subtile_task.task_result`


