from envipyengine import config # Configure engine path if not found
from envipyengine import Engine # Task getting and execution
from pprint import pprint       # Print Python dict

# Hardcoded filepath to task engine -- UNCOMMENT to configure engine path
# task_engine_path = "c:\\Program Files\\NV5\\ENVI61\\IDL91\\bin\\bin.x86_64\\taskengine.exe"
# config.set('engine', task_engine_path) 

class Task: 
    # Public variable
    envi_engine = Engine("ENVI")
        
# -----------------------------------------------------------------------
# Class Initialization
# -----------------------------------------------------------------------
    def __init__(self, task_name: str = "", parameters: dict = {}):
        """ Initializes `Task` object
        
        Args:
            task_name (str): The ENVI name for the task that is going to be called
            parameters (dict): A list of parameters in `{PARAMETER_NAME: parameter_value}` format that the ENVI function (task) takes in
        """
        # Private variables
        self._task_result = {}
        self._input_raster = {}
        self._parameters = dict(parameters)
        self._task_name = task_name
        self._task = self.envi_engine.task(self._task_name)

    # Print Task type as defined by taskname
    def __str__(self):
        return f"ENVI task: \"{self._task_name}\""


# -----------------------------------------------------------------------
# Attribute Setters
# -----------------------------------------------------------------------
    # Set taskname
    def set_taskName(self, task_name: str) -> None:
        """Set the ENVI task that the object performs

        Args:
            task (str): Task name, e.g. "ForwardPCATransform" for the PCA task. 
            Task name strings are as shown in taskObj.task_list()
        """
        self._task_name = task_name  

    # Set input raster by raster or by filepath


    def set_inputRaster(self, *args) -> None:
        """Setter for input raster of task. 
            Takes one of two argument types.
            1) `str` | filepath + filename 
            2) `dict` | raster object
        """

        try:
            if len(args) == 1 and isinstance(args[0], str):
                self._input_raster = dict(url=args[0], factory="URLRaster")
                self._parameters["INPUT_RASTER"] = self._input_raster

            elif len(args) == 1 and type(args) == dict: 
                self._input_raster = args
                
        except Exception as e:
            print(f"The exception is: {e}")
        
    def set_parameters(self, params: dict) -> None:
        """Updates the list of parameters passed to the ENVI function. \n
        If a duplicate exists in what's being passed into the function and what already exists,
        (e.g., if set_parameters passed INPUT_RASTER after the Task was initialized with an INPUT_RASTER),
        then params passed by set_parameters take priority.

        Args:
            params (dict): A list of parameters in `{PARAMETER_NAME: parameter_value}` format that the ENVI function (task) takes in
        """
        
        self._parameters.update(params)


# -----------------------------------------------------------------------
# Attribute Getters
# -----------------------------------------------------------------------
    # Get taskname
    def get_taskName(self) -> str:
        """
        Returns task name of ENVI function 
        """
        return self._task_name 
    
    # Get input raster 
    def get_inputRaster(self) -> dict[str,str]:
        """
        Returns the task object's input raster 
        """
        
        return self._input_raster 
    
    def get_outputRaster(self) -> dict[str,str]:
        """
        Returns result from taskObj.`task_execute()`
   
        NOTE: To get the output file path, instead call taskObj.`get_outputRasterURL()`
        """
        
        return self.task_result["outputParameters"]["OUTPUT_RASTER"]
    
    def get_outputRasterURL(self) -> str:
        """
        Returns URL (filepath) to result from taskObj.`task_execute()`
        """
        return self.task_result["outputParameters"]["OUTPUT_RASTER"]["url"]
    
    
# -----------------------------------------------------------------------
# Task Methods
# -----------------------------------------------------------------------
    # Execute task 
    def task_execute(self) -> None:
        """
        Runs the ENVI task. Returns None; to get the output, call: \n
        taskObj.`get_outputRaster()` or taskObj.`get_outputRasterURL()`
        """
        self.task_result = self._task.execute(self._parameters)

    # Print info about required task parameters
    def task_parameters(self) -> None:
        """
        Prints task parameters of current ENVI task, determined by task_name, to the console.
        """
        pprint(self._task.parameters)
        
    # Print info about tasks ENVI can call    
    def task_list(self) -> None:
        """
        Prints all available tasks ENVI can execute to the console. \n
        Copy the string of the task name to set as task_name when creating a Task object.\n
        E.g., If the console prints: "ForwardPCATransform" -> instantiate the object with: `Task("ForwardPCATransform")`
        """
        pprint(self.envi_engine.tasks())
        
    # More information about current task
    def task_details(self) -> None:
        """
        Prints information about current task, determined by task_name, to the console
        """
        print(self._task.description, type(self._task.description))

        
# -----------------------------------------------------------------------
# Help Information
# -----------------------------------------------------------------------
    # Print info on how to interface with class
    def help(self) -> None:
        print('''
              The Task class allows the user to 
              interface with the ENVI Py Engine library. 
              ENVI functions accept and produce "Rasters" (Images) of type: dict.
              Rasters additionally include metadata, stored in the dict. 
              NOTE: All additional task parameters require UPPERCASE strings.
              (except for the task name, and input/output raster filepaths) 
              \n)
              ''')
        
        print('''
              All classes REQUIRE a taskname. For options, call:\n 
              taskObj.task_list()\n
              ''')
        
        print('''
              All classes REQUIRE an input raster 
              (i.e. a path to an input file + filename).
              To set an input raster, call:\n
              taskObj.set_inputRaster()
              ''')
        
        print('''
              Raster results from ENVI tasks can be obtained with:\n 
              raster = taskObj.get_outputRaster()\n 
              Only AFTER calling:\n
              taskObj.task_execute()\n
              NOTE: To pass a Raster to another ENVI task, instead use
              taskObj.get_outputRasterURL()\n
              ''')
        
        print('''
              Output directory points to the location on local drive 
              where the output file is to be stored. If set to '*' (default),
              the program creates a temp file at execution.\n
              ''')
        
        print('''
              To find what additional task parameters a class needs,
              call:\n
              taskObj.task_parameters()\n
              Additionally, consult this website:\n 
              [https://www.nv5geospatialsoftware.com/docs/routines-159.html]\n
              While the code is written in IDL, the 'Syntax' section 
              gives information on task parameters.
              ''')
