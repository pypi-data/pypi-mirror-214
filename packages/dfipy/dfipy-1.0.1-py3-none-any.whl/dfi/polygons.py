"""
Class with DFI polygon DB, wrappers of the DFI python API.
Composition of the class Connection, aimed at accessing the
polygon DB, where a dataset of named polygons is made available to the user.
"""

import logging
from typing import List

from dfi import validate
from dfi.connect import Connect

logger = logging.getLogger(__name__)


class Polygons:
    """
    Class responsible to call the DFI API and access the polygons DB.

    The polygon DB is a dataset of named polygons. It is made available to the user within the same
    namespace of where the DFI instances lives.

    It can be accessed via the a dfi.Client class instance or it must be instantiated
    with a dfi.Connect instance as argument.

    Parameters
    ----------
    dfi_conn : Connect
        Instance of a Connect with the credentials and namespace of the DFI connection.

    Examples
    --------
    Access via the Client class:

        >>> from dfi import Client
        >>> dfi = Client(dfi_token, instance_name, namespace, base_url)
        >>> dfi_polygons.get_vertices("my polygon name")

    Or access only the Polygons class directly:

        >>> from dfi.connect import Connect
        >>> from dfi.get import Polygons
        >>> conn = dfi.Connect(api_token, instance_name, namespace, base_url)
        >>> dfi_polygons = dfi.Polygons(conn)
        >>> dfi_polygons.get_vertices("my polygon name")

    """

    def __init__(self, dfi_conn: Connect) -> None:
        self.conn: Connect = dfi_conn

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.conn!r})"

    def __str__(self) -> str:
        return f"""Instance of dfi.{self.__class__.__name__} composed with: {self.conn!s}"""

    def get_names(self) -> List[dict]:
        """
        Retrieves a list of saved polygons.

        Example
        -------
        >>> from dfi import Client
        >>> dfi = Client(dfi_token, instance_name, namespace, base_url)
        >>> dfi.polygon.get_names()

        """

        with self.conn.api_get("polygons") as response:
            list_polygons = response.json().get("polygons")
            validate.list_polygons_response(list_polygons, response)
            return list_polygons

    def get_vertices(self, polygon_name: str) -> List[List[float]]:
        """
        Get the list of a polygon saved in the polygon database from its name.

        Parameters
        ----------
        polygon_name: str
            Name of the polygon the user wants to retrieve from the polygons database.

        Return
        -------
        List of the polygon coordinates.

        Example
        -------
        >>> from dfi import Client
        >>> dfi = Client(dfi_token, instance_name, namespace, base_url)
        >>> dfi.polygon.get_names()
        >>> dfi.polygon.get_vertices('my-first-polygon')

        """

        with self.conn.api_get("polygons/" + polygon_name) as response:
            vertices = response.json().get("vertices")
            validate.vertices_response(vertices, response)
            return vertices
