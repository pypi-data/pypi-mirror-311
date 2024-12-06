import inspect
import pandas as pd
from pathlib import Path
from antelope.utils.hash_utils import hash_tables, list_to_datajoint, code_hash
import json


def antelope_analysis(cls):
    """
    This is a class decorator used to reduce boilerplate code in analysis functions.
    """

    # initialise with connection
    def __init__(self, conn):
        super(cls, self).__init__(conn)

    cls.__init__ = __init__

    # inherit from AnalysisBase
    class Child(cls, AnalysisBase):
        __doc__ = cls.__doc__
        pass

    return Child


class AnalysisBase:
    name: str
    query: str
    returns: dict
    args: dict
    hidden: bool = False

    def __init__(self, conn):
        self.conn = conn
        self.tables = conn.tables

    def run(self, *args):
        raise NotImplementedError

    def get_directory(self):
        for i in self.__class__.__bases__:
            if i.__name__ != "AnalysisBase":
                return i.__module__.split(".")[-1]

    def __call__(self, restriction={}, *args, **kwargs):

        # first, check everything initialized
        if not all([self.name, self.query, self.returns]):
            raise TypeError("Function not properly defined")

        # append built-in restriction
        if hasattr(self, "key"):
            restriction = {**restriction, **self.key}

        # get primary keys from restriction
        if isinstance(self.query, str):
            table = self.tables[self.query].proj()
        elif isinstance(self.query, list):
            table = self.tables[self.query[0]]
            for q in self.query[1:]:
                table = table * self.tables[q].proj()
        dataset = (table & restriction).proj().fetch(as_dict=True)

        # loop through primary keys and run function
        results = []
        for primary_key in dataset:

            result = self.run(primary_key, *args, **kwargs)
            answer = primary_key.copy()
            for i, key in enumerate(self.returns.keys()):
                if len(self.returns.keys()) == 1:
                    answer[key] = result
                else:
                    answer[key] = result[i]
            results.append(answer)

        if len(results) == 1:
            return results[0]
        else:
            return results

    def save_result(self, filepath="./result.pkl", restriction={}, *args, **kwargs):
        """
        Runs the function, and saves the pickled result to disk along with the reproducibility json.
        """

        # get argument dictionary
        full_args = get_full_args_dict(self, *args, **kwargs)

        tables = list_to_datajoint(self.tables, self.hash)

        # hash tables
        data_hash = hash_tables(tables, restriction)
        codehash = code_hash(self)

        # save reproducibility
        reproducibility = {
            "name": self.get_directory() + "." + self.name,
            "restriction": restriction,
            "arguments": full_args,
            "data_hash": data_hash,
            "code_hash": codehash,
        }

        # run function
        result = self(restriction, *args, **kwargs)
        result = pd.DataFrame(result)

        # save result
        result.to_pickle(filepath)

        with open(Path(filepath).with_suffix(".json"), "w") as f:
            json.dump(reproducibility, f, indent=4)

    def reproduce(self, json_path, result_path):
        """
        Loads a reproducibility json and runs the function with the same arguments,
        checking the data hash and code hash.
        """

        with open(json_path, "r") as f:
            reproducibility = json.load(f)

        tables = list_to_datajoint(self.tables, self.hash)

        # hash tables
        data_hash = hash_tables(tables, reproducibility["restriction"])
        codehash = code_hash(self)

        # assert everything is the same
        assert (
            reproducibility["name"] == self.get_directory() + "." + self.name
        ), "Function incorrect."
        assert (
            reproducibility["data_hash"] == data_hash
        ), "Data has changed since last function run."
        assert (
            reproducibility["code_hash"] == codehash
        ), "Code has changed since last function run."
        print("Reproducibility checks passed.")
        print("Running function...")

        # run function
        result = self(reproducibility["restriction"], **reproducibility["arguments"])

        # save result
        result = pd.DataFrame(result)
        result.to_pickle(result_path)

    def check_hash(self, json_path):
        """
        Loads a reproducibility json and runs the function with the same arguments,
        checking the data hash and code hash.
        """

        with open(json_path, "r") as f:
            reproducibility = json.load(f)

        # tables to hash
        tables = list_to_datajoint(self.tables, self.hash)

        # hash tables
        data_hash = hash_tables(tables, reproducibility["restriction"])
        codehash = code_hash(self)

        # check conditions
        if not reproducibility["name"] == self.get_directory() + "." + self.name:
            return "Function incorrect."
        elif not reproducibility["data_hash"] == data_hash:
            return "Data has changed since last function run."
        elif not reproducibility["code_hash"] == codehash:
            return "Code has changed since last function run."
        else:
            return "Reproducibility checks passed."


def get_full_args_dict(func, *args, **kwargs):

    # Get the signature of the function
    sig = inspect.signature(func.run)

    # Create a dictionary of the default values
    defaults = {
        k: v.default
        for k, v in sig.parameters.items()
        if v.default is not inspect.Parameter.empty and k != "restriction"
    }

    # Get the names of all parameters
    param_names = [k for k in sig.parameters.keys() if k != "key"]

    # Update the defaults dictionary with provided args
    args_dict = dict(zip(param_names, args))

    # Combine the defaults, provided args, and provided kwargs
    full_args = {**defaults, **args_dict, **kwargs}

    return full_args
