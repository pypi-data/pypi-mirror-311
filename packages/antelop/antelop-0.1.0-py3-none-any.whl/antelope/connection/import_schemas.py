from antelope.schemas import metadata, ephys, behaviour
from antelope.utils.datajoint_utils import delete_restriction, delete_column


def schema(conn):

    # Get the schema tables
    metadata_tables, _ = metadata.schema(conn)
    ephys_tables, _ = ephys.schema(conn)
    behaviour_tables, _ = behaviour.schema(conn)

    # combine the dictionaries
    tables = {**metadata_tables, **ephys_tables, **behaviour_tables}

    # modify tables to we can access the tables from the tables
    new_tables = {}
    for name, table in tables.items():
        table.tables = tables
        table.usertable = True
        delete_col, not_delete = delete_column(table)
        table = (table & delete_restriction(table, delete_mode="False")).proj(
            *not_delete
        )  # modify tables so they're not deleted and projected
        new_tables[name] = table
    for name, table in new_tables.items():
        table.tables = new_tables
        table.connection.tables = new_tables

    return new_tables


def schema_admin(conn):
    # same as above but without delete restriction

    # Get the schema tables
    metadata_tables, _ = metadata.schema(conn)
    ephys_tables, _ = ephys.schema(conn)
    behaviour_tables, _ = behaviour.schema(conn)

    # combine the dictionaries
    tables = {**metadata_tables, **ephys_tables, **behaviour_tables}

    # modify tables to we can access the tables from the tables
    new_tables = {}
    for name, table in tables.items():
        table.tables = tables
        table.usertable = True
        new_tables[name] = table
    for name, table in new_tables.items():
        table.tables = new_tables
        table.connection.tables = new_tables

    return new_tables
