"""
Script contains functions to enforce user permissions.
These will overwrite the table methods via monkey patching.
"""

from antelope.utils.datajoint_utils import delete_restriction
from datajoint.table import Table


class PermissionDeniedError(Exception):
    """Exception raised when a user lacks permission to perform an action."""

    def __init__(self, message="You do not have permission to delete this data."):
        self.message = message
        super().__init__(self.message)


def modify_insert1(method):
    def wrapper(self, row, **kwargs):
        if hasattr(self, "usertable"):
            for key in self.heading.primary_key:
                if (
                    self.heading.attributes[key].comment[-16:] == "(auto_increment)"
                    and key not in row.keys()
                ):
                    row[key] = max((self.proj() & row).fetch(key), default=0) + 1
            return method(self, row, **kwargs)
        else:
            return method(self, row, **kwargs)

    return wrapper


Table.insert1 = modify_insert1(Table.insert1)


def modify_insert(method):
    def wrapper(
        self,
        rows,
        replace=False,
        skip_duplicates=False,
        ignore_extra_fields=False,
        allow_direct_insert=None,
    ):
        """
        Performs insert after checking user permissions
        """
        if hasattr(self, "usertable"):
            username = self.connection.get_user().split("@")[0]
            admin = (self.tables["Experimenter"] & {"experimenter": username}).fetch1(
                "admin"
            )

            if admin == "False":
                if list((self.tables["Experimenter"] & rows).fetch("experimenter")) != [
                    username
                ]:
                    raise PermissionDeniedError(
                        "You do not have permission to insert this data."
                    )
                else:
                    return method(
                        self,
                        rows,
                        replace,
                        skip_duplicates,
                        ignore_extra_fields,
                        allow_direct_insert,
                    )
            elif admin == "True":
                return method(
                    self,
                    rows,
                    replace,
                    skip_duplicates,
                    ignore_extra_fields,
                    allow_direct_insert,
                )
        else:
            return method(
                self,
                rows,
                replace,
                skip_duplicates,
                ignore_extra_fields,
                allow_direct_insert,
            )

    return wrapper


Table.insert = modify_insert(Table.insert)


def modify_update1(method):
    def wrapper(self, row):
        """
        Performs update1 after checking user permissions
        """
        if hasattr(self, "usertable"):
            username = self.connection.get_user().split("@")[0]
            admin = (self.tables["Experimenter"] & {"experimenter": username}).fetch1(
                "admin"
            )

            if admin == "False":
                if "experimenter" not in row.keys() or row["experimenter"] != username:
                    raise PermissionDeniedError(
                        "You do not have permission to update this data."
                    )
                else:
                    return method(self, row)
            elif admin == "True":
                return method(self, row)
        else:
            return method(self, row)

    return wrapper


Table.update1 = modify_update1(Table.update1)


def modify_delete(quick_delete, delete):
    def wrapper(self, safemode=True):
        """
        Wrapper around datajoint's delete that checks user is an admin first
        """
        if hasattr(self, "usertable"):
            # first, check permissions
            username = self.connection.get_user().split("@")[0]
            admin = (self.tables["Experimenter"] & {"experimenter": username}).fetch1(
                "admin"
            )

            if admin == "False":
                raise PermissionDeniedError(
                    "You do not have permission to perform a true delete. Please use temp_delete instead."
                )
            elif admin == "True":
                if safemode:
                    return delete(self)
                else:
                    return quick_delete(self)
        else:
            if safemode:
                return delete(self)
            else:
                return quick_delete(self)

    return wrapper


Table.delete = modify_delete(Table.delete_quick, Table.delete)


def safe_delete_python(query):
    """
    Safely deletes data from the database (just changes the 'delete' attribute to True)
    These deletes cascade
    Inputs: query: the query to delete
    """

    # first, check permissions
    username = query.connection.get_user().split("@")[0]
    admin = (query.tables["Experimenter"] & {"experimenter": username}).fetch1("admin")

    # disallow if user not admin and modifying other user's data
    if (
        admin == "False"
        and f"""(`experimenter`="{username}")""" not in query.make_sql()
    ):
        raise PermissionDeniedError()

    else:
        # all updates in transaction
        update_dict = {}
        full_names = {val.full_table_name: key for key, val in query.tables.items()}
        with query.connection.transaction:

            # loop through all tables to be modified
            for tablename in query.descendants():

                # retrieve datajoint table from full name
                table = query.tables[full_names[tablename]]

                # main query
                full_query = table & (query.proj() & delete_restriction(query, "False"))

                # fetch primary keys of rows to be deleted
                data = full_query.proj().fetch(as_dict=True)

                update_dict[tablename] = data

            # now loop again to perform modifications
            for tablename, data in update_dict.items():

                # retrieve datajoint table from full name
                table = query.tables[full_names[tablename]]

                for i in data:
                    table.update1({**i, **delete_restriction(table, "True")})


Table.tmp_delete = safe_delete_python
