"connection package"

__version__ = "0.3.3"

from functools import singledispatch

from snowflake.connector import DatabaseError, DataError, InterfaceError, ProgrammingError
from snowflake.connector.cursor import ResultMetadata

from .conn import Connection, Cursor, available_connections, default_connection_name, getconn
from .jwt import RestInfo, get_rest_info, get_token
from .utils import pytype_conn, set_loglevel, with_connection, with_connection_args, with_rest, with_rest_args


@singledispatch
def pytype(meta, best_match: bool = False) -> type:  # type: ignore
    raise TypeError(f"{meta} is not an instance of ResultMetadata or DataType")


@pytype.register(ResultMetadata)
def _(meta: ResultMetadata, best_match: bool = False):
    return pytype_conn(meta, best_match)


try:
    from snowflake.snowpark.types import DataType

    from .utils_snowpark import getsess, pytype_sess, with_session

    @pytype.register(DataType)
    def _(meta: DataType, _: bool = False):
        return pytype_sess(meta)

except ImportError:
    pass

__all__ = [
    "DatabaseError",
    "DataError",
    "InterfaceError",
    "ProgrammingError",
    "ResultMetadata",
    "Connection",
    "Cursor",
    "available_connections",
    "default_connection_name",
    "getconn",
    "getsess",
    "get_token",
    "get_rest_info",
    "RestInfo",
    "pytype",
    "set_loglevel",
    "with_connection",
    "with_connection_args",
    "with_session",
    "with_rest",
    "with_rest_args",
]
