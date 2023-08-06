"""
Class with DFI analytic methods, leveraging on the python api wrappers to gain analytical information.
Composition of the class Connect.
"""

import logging
from datetime import timedelta
from typing import Optional

import geopandas as gpd
import h3.api.numpy_int as h3
import pandas as pd
from shapely.geometry import Polygon

from dfi import models, validate
from dfi.connect import Connect
from dfi.get import Get

logger = logging.getLogger(__name__)


class Analyse:
    """
    Class with analytical methods to build use cases on top of the DFI's queries.

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
        >>> dfi.analyse.records_in_hexagons(uid, resolution, period)

    Or access only the Analyse class directly:

        >>> from dfi.connect import Connect
        >>> from dfi.get import Analyse
        >>> conn = dfi.Connect(api_token, namespace, instance_name, base_url)
        >>> dfi_analyse = dfi.Analyse(conn)
        >>> dfi_analyse.records_in_hexagons(uid, resolution, period)

    """

    def __init__(self, dfi_conn: Connect) -> None:
        self.conn: Connect = dfi_conn
        self.get = Get(self.conn)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.conn!r})"

    def __str__(self) -> str:
        return f"""Instance of dfi.{self.__class__.__name__} composed with: {self.conn!s}"""

    def add_spatiotemporal_hashing(
        self,
        df_records: pd.DataFrame,
        h3_resolution: int,
        time_resolution_min: int,
    ) -> gpd.GeoDataFrame:
        """
        Binning the records of a given dataframe of records by time (period) and space (H3 resolution)
        and with optional additional spatial and temporal constraints.

        Parameters
        ----------
        df_records: pd.DataFrame
            Dataframe with the records we want to hash.
        h3_resolution: int
            Uber's H3 h3_resolution. Allowed numbers are > 1 and < 15.
        time_resolution_min: int
            Time interval in minutes for timestamp binning.

        Returns
        -------
        A copy of df_records casted to a GeoDataFrame with 3 extra columns: [hex_id, period_start, period_end] and
        with "geometry" column the geometry of the H3 hexagon where the record appeared.

        The input dataframe is copied, and not modified in place.

        Example
        -------
        >>> from dfi import Client
        >>> dfi = Client(dfi_token, instance_name, namespace, base_url)
        >>> df_records = dfi.get.records(entities=[entity_id], time_interval=(start_time, end_time))
        >>> dfi.analyse.add_spatiotemporal_hashing(df_records, h3_resolution=11, time_resolution_min=15)

        """
        validate.df_records(df_records)
        validate.h3_resolution(h3_resolution)

        df_records["hex_id"] = [
            h3.geo_to_h3(lat, lon, h3_resolution) for lat, lon in zip(df_records["latitude"], df_records["longitude"])
        ]
        df_records = df_records.assign(period_start=lambda df: df["timestamp"].round(f"{time_resolution_min}min"))
        df_records = df_records.assign(period_end=lambda df: df.period_start + timedelta(minutes=time_resolution_min))

        return gpd.GeoDataFrame(
            df_records,
            geometry=df_records["hex_id"].apply(lambda idx: Polygon(h3.h3_to_geo_boundary(idx, geo_json=True))),
        )

    def records_for_entity_id_with_spatiotemporal_hashing(
        self,
        entity_id: str,
        h3_resolution: int,
        time_resolution_min: int,
        time_interval: Optional[models.TimeInterval] = None,
        polygon: Optional[models.Polygon] = None,
    ) -> pd.DataFrame or gpd.GeoDataFrame:
        """
        Binning the records of a device id by time (time_resolution_min) in minutes
        and space (h3_resolution) with a valid resolution of H3,
        and with additional spatial and temporal constraints, from the parameters
        to a DFI query (entity_id, polygon, time_interval=(start_time, end_time)).

        Parameters
        ----------
        entity_id : str
            unique identifier of a device we want to analyse.
        h3_resolution: int
            Uber's H3 h3_resolution. Allowed numbers are > 1 and < 15.
        time_resolution_min: int
            Time interval in minutes for timestamp binning.
        time_interval: Optional[models.TimeInterval] = None
            Tuple with the Lower bound and the upper bound time constraints.
        polygon: Optional[models.Polygon] = None
            List of vertices [[lon1, lat1], [lon2, lat2], ...] or a list of four
            floats representing the bounding box extremes as [lon_min, lat_min, lon_max, lat_max].
            Non valid input will raise an error.

        Returns
        -------
        A dataframe with the history of the loaded records from DFI by the constraints space and time,
        with extra columns with the binning of H3 resolution and time resolution.

        From there you can get the unique hexagons from where the devices are appearing.

        Example
        -------
        >>> from dfi import Client
        >>> dfi = Client(dfi_token, instance_name, namespace, base_url)
        >>> start_time = datetime.strptime("2022-01-01T08:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        >>> end_time = datetime.strptime("2022-01-01T08:30:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        >>> entity="299eb59a-e47e-48c0-9ad5-89a9ce1303f4"
        >>> dfi.analyse.records_for_entity_id_with_spatiotemporal_hashing(
        ...     entity_id=entity,
        ...     h3_resolution=11,
        ...     time_resolution_min=15,
        ...     time_interval=(start_time, end_time),
        ...     polygon=polygon
        ... )


        """
        df_records = self.get.records(entities=[entity_id], polygon=polygon, time_interval=time_interval)

        if len(df_records) == 0:
            logger.debug("No history found for entity %s", entity_id)
            return gpd.GeoDataFrame(
                columns=[
                    "entity_id",
                    "latitude",
                    "longitude",
                    "timestamp",
                    "hex_id",
                    "period_start",
                    "period end",
                ]
            )

        return self.add_spatiotemporal_hashing(
            df_records,
            h3_resolution=h3_resolution,
            time_resolution_min=time_resolution_min,
        )

    def add_heatmap_aggregation(
        self,
        df_records: pd.DataFrame,
        h3_resolution: int,
        colorscale_colum_name: str = "num_records",
        colorscale_log_transform: bool = True,
    ) -> pd.DataFrame:
        """
        Aggregates the records by the H3 hexagons at the given resolution.

        Parameters
        ----------
        df_records: pd.DataFrame
            Dataframe with the records we want to aggregate.
        h3_resolution: int
            Uber's H3 resolution. Allowed numbers are > 1 and < 15.
        colorscale_colum_name: str = "num_records"
            Name of the column with the colorscale for visualisation.
        colorscale_log_transform: bool = True,
            Log transform the colorscale.

        Returns
        -------
        Returns the given dataframe with extra `hex_id`, `num_records` and `color` columns.
        The operation happens in place.

        Example
        -------
        >>> from dfi import Client
        >>> dfi = Client(dfi_token, instance_name, namespace, base_url)
        >>> df_records = dfi.get.records(entities=[entity_id], time_interval=(start_time, end_time))
        >>> dfi.analyse.heatmap_aggregation(df_records, h3_resolution=11)

        """
        return (
            df_records.assign(
                hex_id=lambda df: [
                    h3.geo_to_h3(lat, lon, resolution=h3_resolution)
                    for lat, lon in zip(df["latitude"], df["longitude"])
                ]
            )
            .pipe(_aggregate_records, "hex_id")
            .assign(hex_id=lambda df: df.hex_id.map(hex).str[2:])
        )

    def records_for_entity_id_with_heatmap_aggregation(
        self,
        entity_id: str,
        h3_resolution: int,
        time_interval: Optional[models.TimeInterval] = None,
        polygon: Optional[models.Polygon] = None,
        colorscale_colum_name: str = "num_records",
        colorscale_log_transform: bool = True,
    ) -> pd.DataFrame:
        """
        Aggregates the records by the H3 hexagons at the given resolution, from the parameters
        to a DFI query (entity_id, polygon, start_time, end_time)

        Parameters
        ----------
        entity_id : str
            unique identifier of a device we want to analyse.
        h3_resolution: int
            Uber's H3 h3_resolution. Allowed numbers are > 1 and < 15.
        time_interval: Optional[models.TimeInterval] = None
            Tuple with the Lower bound and the upper bound time constraints.
        polygon: Optional[models.Polygon] = None
            List of vertices [[lon1, lat1], [lon2, lat2], ...] or a list of four
            floats representing the bounding box extremes as [lon_min, lat_min, lon_max, lat_max].
            Non valid input will raise an error.
        colorscale_col: str = "num_records"
            Name of the column with the colorscale for visualisation.
        colorscale_log_transform: bool = True,
            Log transform the colorscale.

        Returns
        -------
        Returns the queried records dataframe with extra `hex_id`, `num_records` and `color` columns.

        Example
        -------
        >>> from dfi import Client
        >>> dfi = Client(dfi_token, instance_name, namespace, base_url)
        >>> start_time = datetime.strptime("2022-01-01T08:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        >>> end_time = datetime.strptime("2022-01-01T08:30:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        >>> entity="299eb59a-e47e-48c0-9ad5-89a9ce1303f4"
        >>> dfi.analyse.records_for_entity_id_with_heatmap_aggregation(
        ...     entity_id=entity,
        ...     h3_resolution=11,
        ...     polygon=polygon,  # a valid polygon
        ...     time_interval=(start_time,end_time),
        ... )

        """
        df_records = self.get.records(entities=[entity_id], polygon=polygon, time_interval=time_interval)

        if len(df_records) == 0:
            logger.debug("No history found for entity %s", entity_id)
            return gpd.GeoDataFrame(
                columns=[
                    "entity_id",
                    "latitude",
                    "longitude",
                    "timestamp",
                    "hex_id",
                    "period_start",
                    "period end",
                ]
            )

        return self.add_heatmap_aggregation(
            df_records,
            h3_resolution=h3_resolution,
            colorscale_colum_name=colorscale_colum_name,
            colorscale_log_transform=colorscale_log_transform,
        )


def _aggregate_records(df_input: pd.DataFrame, hex_id: str) -> pd.DataFrame:
    return (
        df_input.groupby(hex_id)
        .agg(
            num_records=("entity_id", "count"),
            num_devices=("entity_id", "nunique"),
            first_ping=("timestamp", "min"),
            last_ping=("timestamp", "max"),
        )
        .reset_index()
    )
