"""
Class with methods to show DFI results.
Composition of the class Connection.
"""

import logging
from copy import deepcopy
from typing import List, Optional, Tuple, Union

import geopandas as gpd
import pandas as pd
from keplergl import KeplerGl
from shapely.geometry import Polygon

from dfi import validate
from dfi.connect import Connect
from dfi.models import Polygon as ModelPolygons
from dfi.polygons import Polygons

logger = logging.getLogger(__name__)


class Show:
    """
    Visualisation methods to build use case on top of the queries from DFI.

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
        self.polygons = Polygons(self.conn)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.conn!r})"

    def __str__(self) -> str:
        return f"""Instance of dfi.{self.__class__.__name__} composed with: {self.conn!s}"""

    def map(
        self,
        list_polygons: Optional[List[ModelPolygons]] = None,
        list_polygons_by_names: Optional[List[str]] = None,
        df_records: Optional[pd.DataFrame] = None,
        list_dfs: Optional[Union[gpd.GeoDataFrame, pd.DataFrame]] = None,
        map_height: int = 1200,
        config: Optional[dict] = None,
    ) -> KeplerGl:
        """
        Helper method to crete a kepler map with the given input layers, to reproduce proposed
        examples in the example notebooks.

        Parameters
        ----------
        list_polygons: Optional[List[str]]
            List of polygons, as list of vertices [[lon1, lat1], [lon2, lat2], ...].
        list_polygons_by_names: Optional[List[str]]
            List of polygon names as they are named in the auxiliary Polygon DB.
        df_records: Optional[pd.DataFrame]
            Dataframe of records with record_id, timestamp, latitude, longitude as its columns.
        list_dfs: Optional[Union[gpd.GeoDataFrame, pd.DataFrame]] = None,
            Generic list of any dataframe or geodataframe to be visualised on the map.
        map_height: int = 1200
            Parameter passed to the KeplerGl instance as it is, overriding the default.
        config: Optional[dict] = None
            Parameter passed to the KeplerGl instance as it is.

        Return
        -------
        Instance of a kepler map with the given data to visualise.

        Example
        -------
        >>> from dfi import Client
        >>> dfi = Client(dfi_token, instance_name, namespace, base_url)
        >>> dfi.show.map()  # creates an empty Kepler map
        """
        if list_polygons is None:
            list_polygons = []

        list_polygons_as_vertices = []
        for poly in list_polygons:
            # from bounding boxes to vertices
            validate.polygon(poly)
            if isinstance(poly[0], float):
                list_polygons_as_vertices += [from_bbox_to_polygon_list(poly)]
            else:
                list_polygons_as_vertices += [poly]

        dict_polygons = {f"polygon {idx}": poly for idx, poly in enumerate(list_polygons_as_vertices)}

        if list_polygons_by_names is not None:
            dict_polygons.update(
                {poly_name: self.polygons.get_vertices(poly_name) for poly_name in list_polygons_by_names}
            )

        kepler_data = {}

        if len(dict_polygons) > 0:
            kepler_data.update(
                {
                    "polygons": gpd.GeoDataFrame(
                        dict_polygons.keys(),
                        geometry=[Polygon(x) for x in dict_polygons.values()],
                    )
                }
            )

        if df_records is not None:
            validate.df_records(df_records)
            kepler_data.update({"records": df_records.copy()})

        if list_dfs is not None:
            for idx, df in enumerate(list_dfs):
                kepler_data.update({f"df_{idx}": df.copy()})

        if config is None:
            return KeplerGl(data=deepcopy(kepler_data), height=map_height)
        return KeplerGl(data=deepcopy(kepler_data), height=map_height, config=config)


def from_bbox_to_polygon_list(bounding_box: List[float]) -> Tuple[Tuple[float, float]]:
    """Convert a bounding box, passed as a list [min_lon, min_lat, max_lon, max_lat] into a tuple of vertices"""
    validate.bounding_box(bounding_box)
    min_lon, min_lat, max_lon, max_lat = bounding_box
    return ((max_lon, max_lat), (max_lon, min_lat), (min_lon, min_lat), (min_lon, max_lat), (max_lon, max_lat))
