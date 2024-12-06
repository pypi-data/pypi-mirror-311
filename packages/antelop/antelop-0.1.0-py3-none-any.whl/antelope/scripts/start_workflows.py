from antelope.connection import connect, import_schemas
from antelope.utils.os_utils import get_config
from antelope.utils.analysis_utils import import_analysis
import os
import types

config = get_config()
username = os.environ.get("DB_USER")
password = os.environ.get("DB_PASS")

if username is None or password is None:
    raise Exception("Please set the DB_USER and DB_PASS environment variables")

conn = connect.dbconnect(username, password)
tables = import_schemas.schema(conn)

for key, val in tables.items():
    globals()[key] = val

# import analysis functions
analysis_functions = import_analysis(conn, tables)
for folder, fcts in analysis_functions.items():
    # make class
    if folder not in globals():
        globals()[folder] = types.SimpleNamespace()
    for fct in fcts:
        setattr(globals()[folder], fct.name, fct)
