from antelope.connection.connect import dbconnect
from antelope.connection import import_schemas
from antelope.utils.os_utils import get_config
from antelope.utils.analysis_utils import import_analysis, reload_analysis
from IPython import embed
import getpass
from types import SimpleNamespace
import antelope.scripts.hold_conn as hold


def run():

    # first check config file exists
    config = get_config()
    if config is None:
        print("Config file not found.")
        print("Please run `antelope-config` to generate a configuration file.")
        exit()

    # connect to database
    username = input("Please enter your username: ")
    password = getpass.getpass("Please enter your password: ")

    global conn
    conn = dbconnect(username, password)
    global tables
    tables = import_schemas.schema(conn)

    if hold.conn is None:
        hold.conn = conn
    if hold.tables is None:
        hold.tables = tables

    for key, val in tables.items():
        globals()[key] = val

    # import analysis functions
    analysis_functions = import_analysis(conn, tables)
    for folder, fcts in analysis_functions.items():
        # make class
        if folder not in globals():
            globals()[folder] = SimpleNamespace()
        for fct in fcts:
            setattr(globals()[folder], fct.name, fct)

    def reload():
        """
        Global function to relaod all analysis functions interactively
        """
        analysis_functions = reload_analysis(conn, tables)
        for folder, fcts in analysis_functions.items():
            # make class
            if folder not in globals():
                globals()[folder] = SimpleNamespace()
            for fct in fcts:
                setattr(globals()[folder], fct.name, fct)

    # start ipython session
    embed()
