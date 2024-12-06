from antelope.connection import import_schemas
from antelope.utils.os_utils import get_config
from antelope.utils.analysis_base import AnalysisBase
from antelope.utils.hash_utils import dfs_functions, dfs_functions_not_tables
import importlib
import pkgutil
import inspect
import types
import sys
from pathlib import Path
import json
import ast


def import_analysis(conn, tables):

    # built in analysis functions
    analysis = importlib.import_module("antelope.analysis")
    functions = {}
    for _, name, _ in pkgutil.iter_modules(analysis.__path__):
        module = importlib.import_module(f"antelope.analysis.{name}")
        for _, cls in module.__dict__.items():
            if (
                inspect.isclass(cls)
                and issubclass(cls, AnalysisBase)
                and cls != AnalysisBase
            ):
                setattr(cls, "local", False)
                setattr(cls, "folder", name)
                if name not in functions:
                    functions[name] = []
                functions[name].append(cls(conn))

    # user defined analysis functions
    user_analysis = get_config()["analysis"]["folders"]
    for folder in user_analysis:
        sys.path.append(str(folder))
        for file in Path(folder).rglob("*.py"):
            module = importlib.import_module(file.stem)
            for _, cls in module.__dict__.items():
                if (
                    inspect.isclass(cls)
                    and issubclass(cls, AnalysisBase)
                    and cls != AnalysisBase
                ):
                    setattr(cls, "local", True)
                    setattr(cls, "folder", file.stem)
                    if file.stem not in functions:
                        functions[file.stem] = []
                    functions[file.stem].append(cls(conn))

    # add functions to functions
    new_functions = {}
    for folder_name, outer_folder in functions.items():
        new_functions[folder_name] = []
        for outer_function in outer_folder:

            # patch run method
            new_functions[folder_name].append(
                patch_functions(outer_function, functions, tables)
            )

    return new_functions


def instantiate_from_db(key, tables):

    # pull function definition from database
    function, name = (tables["AnalysisFunction"] & key).fetch1(
        "function", "analysisfunction_name"
    )

    # deserialise and instantiate
    function = json.loads(function)
    parsed = ast.parse(function)
    for node in ast.walk(parsed):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
    exec(function)
    function = locals()[class_name](tables["Experimenter"].connection)
    function.local = False
    return function


def patch_functions(self, functions, tables):
    """
    This function patches the functions to allow other functions and tables to be accessible in the run() method.
    Has to be separate from the decorator as functions haven't yet been initialised with connections when the decorator is called.
    """

    new_globals = self.run.__globals__.copy()

    # add tables that are defined in function
    new_tables = []
    if isinstance(self.query, str):
        new_tables.append(self.query)
    elif isinstance(self.query, list):
        new_tables = self.query
    if hasattr(self, "data"):
        if isinstance(self.data, str):
            new_tables.append(self.data)
        elif isinstance(self.data, list):
            new_tables += self.data
    for key in new_tables:
        new_globals[key] = tables[key]

    # add functions defined in calls
    if hasattr(self, "calls"):
        for fct in self.calls:
            if "." in fct:
                folder, function = fct.split(".")
                if folder not in new_globals:
                    new_globals[folder] = types.SimpleNamespace()
                for fct_inner in functions[folder]:
                    if fct_inner.name == function:
                        setattr(new_globals[folder], function, fct_inner)
            else:
                folder = Path(inspect.getsourcefile(self.__class__.__bases__[0])).stem
                for fct_inner in functions[folder]:
                    if fct_inner.name == fct:
                        new_globals[fct] = fct_inner

    new_run = types.FunctionType(
        self.run.__code__,
        new_globals,
        self.run.__name__,
        self.run.__defaults__,
        self.run.__closure__,
    )
    self.run = new_run

    # compute all tables to hash for later
    hash = dfs_functions(self, functions)
    self.hash = hash

    return self


def split_trials(data, mask):
    """
    Split trials based on mask

    Inputs:
    mask: tuple of data, timestamps
    data: tuple of data, timestamps

    Returns:
    list of tuples of data, timestamps
    """

    mask_data, mask_time = mask
    data_data, data_time = data

    start_times = mask_time[mask_data == 1]
    stop_times = mask_time[mask_data == -1]

    mask = (data_time[:, None] >= start_times) & (data_time[:, None] <= stop_times)
    trials = [
        (data_data[mask[:, i]], data_time[mask[:, i]]) for i in range(mask.shape[1])
    ]

    return trials


def instantiate_function(key, tables):
    """
    Function loads an analysis function from the masks table and returns an instantiation of it
    """
    # pull function definition from database
    function, name = (tables["MaskFunction"] & key).fetch1(
        "mask_function", "maskfunction_name"
    )

    # deserialise and instantiate
    function = json.loads(function)
    exec(function)
    function = locals()[name](tables["Experimenter"].connection)

    # patch functions to function
    functions = import_analysis(tables["Experimenter"].connection, tables)
    for folder_name, outer_folder in functions.items():
        function = patch_functions(function, functions, tables)

    return function


def get_docstring(function_string, name):
    """
    Gets docstring from function string
    """

    exec(json.loads(function_string))
    function = locals()[name]
    docstring = function.__doc__
    return docstring


def reload_analysis(conn, tables):
    """
    Reloads analysis functions and repatches them if the underlying script has changed
    """

    analysis = importlib.import_module("antelope.analysis")
    functions = {}
    for _, name, _ in pkgutil.iter_modules(analysis.__path__):
        module_name = f"antelope.analysis.{name}"
        if module_name in sys.modules:
            # reload module if it's already loaded
            module = importlib.reload(sys.modules[module_name])
        else:
            module = importlib.import_module(module_name)

        for _, cls in module.__dict__.items():
            if (
                inspect.isclass(cls)
                and issubclass(cls, AnalysisBase)
                and cls != AnalysisBase
            ):
                if name not in functions:
                    functions[name] = []
                functions[name].append(cls(conn))

    # user-defined analysis functions
    user_analysis = get_config()["analysis"]["folders"]
    for folder in user_analysis:
        sys.path.append(str(folder))
        for file in Path(folder).iterdir():
            if file.suffix != ".py":
                continue
            module_name = file.stem
            if module_name in sys.modules:
                # reload module if it's already loaded
                module = importlib.reload(sys.modules[module_name])
            else:
                module = importlib.import_module(module_name)

            for _, cls in module.__dict__.items():
                if (
                    inspect.isclass(cls)
                    and issubclass(cls, AnalysisBase)
                    and cls != AnalysisBase
                ):
                    if module_name not in functions:
                        functions[module_name] = []
                    functions[module_name].append(cls(conn))

    # add functions to new_functions with patched run method
    new_functions = {}
    for folder_name, outer_folder in functions.items():
        new_functions[folder_name] = []
        for outer_function in outer_folder:
            # patch run method
            new_functions[folder_name].append(
                patch_functions(outer_function, functions, tables)
            )

    return new_functions


def publish_function(function, analysis_functions, username, tables):

    admin_tables = import_schemas.schema_admin(tables["Experimenter"].connection)

    # first check all functions called by this function
    functions = dfs_functions_not_tables(function, analysis_functions)
    # hacky change this
    if len(functions) == 0:
        functions = [function]

    # publish all functions
    new = 0
    with tables["Experimenter"].connection.transaction:
        for fct in functions:

            # make key
            insert_dict = {}
            insert_dict["experimenter"] = username
            insert_dict["analysisfunction_name"] = fct.name
            insert_dict["folder"] = fct.folder

            # check if in database
            if tables["AnalysisFunction"] & insert_dict:
                update = True
                insert_dict["analysisfunction_id"] = (
                    tables["AnalysisFunction"] & insert_dict
                ).fetch1("analysisfunction_id")
            else:
                update = False
                new += 1
                insert_dict["analysisfunction_id"] = (
                    max(
                        (tables["AnalysisFunction"] & {"experimenter": username}).fetch(
                            "analysisfunction_id"
                        ),
                        default=1,
                    )
                    + new
                )

            # add other attributes
            insert_dict["function"] = json.dumps(
                inspect.getsource(fct.__class__.__bases__[0])
            )
            if hasattr(fct, "hidden"):
                if fct.hidden:
                    insert_dict["hidden"] = "True"
                else:
                    insert_dict["hidden"] = "False"
            else:
                insert_dict["hidden"] = "False"
            insert_dict["analysisfunction_description"] = fct.__doc__

            if update:
                tables["AnalysisFunction"].update1(insert_dict)
            else:
                tables["AnalysisFunction"].insert1(insert_dict)
