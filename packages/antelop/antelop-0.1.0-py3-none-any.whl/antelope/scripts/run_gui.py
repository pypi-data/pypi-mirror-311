import os
from pathlib import Path
from antelope.utils.os_utils import cp_st_config
import runpy
import sys
import warnings


def run():

    try:

        import streamlit

    except ImportError:

        print(
            """
Antelope GUI is not installed. Please install using:

pip install antelope[gui]

Or run the command line version using:

antelope-python
        """
        )

    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            # copy streamlit config to home if it doesn't exist
            cp_st_config()

            app = Path(os.path.abspath(__file__)).parent / "app.py"

            sys.argv = ["streamlit", "run", str(app)]
            runpy.run_module("streamlit", run_name="__main__")
