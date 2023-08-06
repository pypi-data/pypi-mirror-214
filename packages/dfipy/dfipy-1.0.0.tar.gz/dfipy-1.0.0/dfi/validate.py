"""
Module with private validator methods used across classes.

Some will be improved and delegated to the DFI API.

Example
-------
>>> from dfi import validate
>>> validate.df_records(df_records)
"""
import json
import logging
from datetime import datetime
from typing import List, Optional

import pandas as pd
import requests

from dfi import models

logger = logging.getLogger(__name__)


class DFIResponseError(Exception):
    """Raised when an error propagated back from the HTTP API"""


class DFIResponseWarning(Warning):
    """Raised when some exceptional case is propagated back from the HTTP API"""


class DFIDataFrameColumnsNameError(Exception):
    """Raised when the column names of a dataframe are not as expected"""


class DFIInputValueError(Exception):
    """Raised when the user passes a wrong input value to the DFI query"""


class DFIInputValueOutOfBoundError(Exception):
    """Raised when the user passes a wrong input value to the DFI query"""


def df_records(df_rec: pd.DataFrame) -> None:
    """
    Check the column names are correct.
    """
    for col_name in ["entity_id", "latitude", "longitude", "timestamp"]:
        if col_name not in df_rec.columns:
            raise DFIDataFrameColumnsNameError(f"Column name {col_name} expected in df_records but not found.")


def h3_resolution(h3_res: int) -> None:
    """check the input is within an acceptable range."""
    if (h3_res < 1) or (h3_res > 15):
        raise DFIInputValueOutOfBoundError(
            f"Resolution is incorrect. It must be between 1 and 15. User passed {h3_res}"
        )


def vertices_response(vert: Optional[models.Polygon], resp: requests.models.Response) -> None:
    if vert is None:
        msg = f"Polygon vertices can not be retrieved from the json response: {resp.json()}"
        logger.error(msg)
        raise DFIResponseError(msg)


def list_polygons_response(vert: Optional[models.Polygon], resp: requests.models.Response) -> None:
    if vert is None:
        msg = f"Polygon list can not be retrieved from the json response: {resp.json()}"
        logger.error(msg)
        raise DFIResponseError(msg)


def response(
    resp: requests.models.Response,
    url: str,
    headers: dict,
    params: dict,
    payload: Optional[dict] = None,
) -> None:
    """
    Log the response of a request with the given parameters. Raise an error if status code is not 20x.
    """
    # prevent from showing the user token to terminal and logs
    headers = headers.copy()
    headers["X-API-TOKEN"] = "Bearer XXX"

    msg = f"""Response status code {resp.status_code}.
Query URL: {url},
HEADER: {json.dumps(headers, sort_keys=True, indent=4)},
PARAMS: {json.dumps(params, sort_keys=True, indent=4)}
"""
    if payload is not None:
        msg += f"PAYLOAD: {json.dumps(payload, sort_keys=True, indent=4)}"

    if int(resp.status_code / 10) != 20:
        msg += f" Status Code {resp.status_code}. "
        msg += resp.text
        logger.error(msg)
        raise DFIResponseError(msg)

    logger.debug(msg)


def time_interval(time_interv: Optional[models.TimeInterval] = None) -> None:
    """
    Validate input datetimes are both given and compatible.
    """
    if time_interv is None:
        return
    if len(time_interv) != 2:
        msg = f"Time interval is not an interval with two dates. User passed {time_interv}"
        raise DFIInputValueError(msg)

    start_time, end_time = time_interv

    if start_time is None and end_time is None:
        return
    if (start_time is None and end_time is not None) or (start_time is not None and end_time is None):
        msg = (
            "start_time and end_time must be both initialised or both None. "
            f"User passed start_time={start_time}, end_time={end_time}"
        )
        raise DFIInputValueError(msg)

    if not isinstance(start_time, datetime):
        msg = f"Start time should be of type datetime. User passed {start_time}"
        raise DFIInputValueError(msg)

    if not isinstance(end_time, datetime):
        msg = f"End time should be of type datetime. User passed {end_time}"
        raise DFIInputValueError(msg)

    if not start_time < end_time:
        msg = f"Start time {start_time} happened after than end time {end_time}."
        raise DFIInputValueError(msg)


def entities(input_entities: Optional[List[str]]) -> None:
    """
    Validate a given list of entities is a list of strings.
    """
    if input_entities is None:
        return
    if not isinstance(input_entities, list):
        raise DFIInputValueError(f"Entities must be a list of strings. Received {input_entities}")
    if len(input_entities) == 0:
        raise DFIInputValueError("Entities must be a list of strings. Received an empty list")
    if len(set(input_entities)) < len(input_entities):
        duplicates_found = set([x for x in input_entities if input_entities.count(x) > 1])
        raise DFIInputValueError(f"Entities list must not contain duplicates. Duplicates found {duplicates_found}")


def vertices(input_vertices: Optional[List[List[float]]]) -> None:
    """
    Check input list of vertices correspond to a polygon.
    It does not check if the polygon is simple.
    """
    if input_vertices is None:
        return
    if len(input_vertices) < 3:
        raise DFIInputValueError("A polygon can not have less than 3 vertices. User passed {vertices}.")
    for vertex in input_vertices:
        if not len(vertex) == 2:
            raise DFIInputValueError("Length of each vertex must be 2. User passed {vertex}")
        if not isinstance(vertex[0], float) or not isinstance(vertex[1], float):
            raise DFIInputValueError(
                f"Coordinates must be of type float."
                f" User passed {vertex} of types ({type(vertex[0])}, {type(vertex[1])})"
            )
        lng, lat = vertex
        if not -180 < lng <= 180:
            raise DFIInputValueOutOfBoundError(f"Input longitude {lng} is out of range.")
        if not -90 < lat < 90:
            raise DFIInputValueOutOfBoundError(f"Input  latitude {lat} is out of range.")

    if not input_vertices[0] == input_vertices[-1]:
        raise DFIInputValueError("First and last vertices are expected to be identical points.")


def bounding_box(list_bbox: Optional[List[float]]) -> None:
    """
    Check input list of coordinates correspond to a bounding box, with lon, lat within the range.
    """
    if list_bbox is None:
        return
    if len(list_bbox) != 4:
        raise DFIInputValueError(f"Input bounding box parameters must be a list of 4 floats. User passed {list_bbox}")
    for value in list_bbox:
        if not isinstance(value, float):
            raise DFIInputValueError(f"Input value {value} of type {type(value)} must be a float.")

    min_lng, min_lat, max_lng, max_lat = list_bbox

    if not -180 < min_lng <= 180:
        raise DFIInputValueOutOfBoundError(f"Input min longitude {min_lng} is out of range.")
    if not -180 < max_lng <= 180:
        raise DFIInputValueOutOfBoundError(f"Input max longitude {max_lng} is out of range.")
    if not -90 < min_lat < 90:
        raise DFIInputValueOutOfBoundError(f"Input min latitude {min_lat} is out of range.")
    if not -90 < max_lat < 90:
        raise DFIInputValueOutOfBoundError(f"Input max latitude {max_lat} is out of range.")


def polygon(poly: Optional[models.Polygon]) -> None:
    """
    Check input list of coordinates correspond to a list of vertices, or a bounding box.
    """
    if poly is None:
        return
    if not isinstance(poly, (list, tuple)):
        return DFIInputValueError(f"Polygon {poly} must be of type list or tuple.")
    if len(poly) == 0:
        raise DFIInputValueError(f"Given polygon {poly} is empty.")
    if not isinstance(poly[0], (list, tuple, float)):
        return DFIInputValueError(f"Polygon {poly} must be a list of tuples or floats.")
    if isinstance(poly[0], float):
        bounding_box(poly)
    if isinstance(poly[0], (list, tuple)):
        vertices(poly)


def df_hexes_heatmap(df_h3: pd.DataFrame) -> None:
    """
    Check the column names are correct.
    """
    for col_name in ["entity_id", "latitude", "longitude", "timestamp", "hex_id", "period_start", "period end"]:
        if col_name not in df_h3.columns:
            raise DFIDataFrameColumnsNameError(f"Column name {col_name} expected in df_records but not found.")


def df_hexes(df_h3: pd.DataFrame) -> None:
    """
    Check the column names are correct.
    """
    for col_name in ["entity_id", "latitude", "longitude", "timestamp", "hex_id"]:
        if col_name not in df_h3.columns:
            raise DFIDataFrameColumnsNameError(f"Column name {col_name} expected in df_records but not found.")
