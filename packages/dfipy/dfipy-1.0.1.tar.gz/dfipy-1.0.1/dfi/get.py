"""
Class with DFI getters, wrappers of the DFI python API.
Composition of the class Connection.
"""
import json
import logging
import warnings
from datetime import datetime
from time import sleep
from typing import Any, List, Optional, Tuple, Union

import pandas as pd
import requests
import sseclient
from tqdm import tqdm

from dfi import models, validate
from dfi.connect import Connect

logger = logging.getLogger(__name__)

NUM_ATTEMPTS = 3


class Get:
    """
    Class responsible to call the HTTP API and submit queries.

    It can be accessed via the a dfi.Client class instance or it must be instantiated
    with a dfi.Connect instance as argument.

    Parameters
    ----------
    conn : Connect
        Instance of a Connect with the credentials and namespace of the DFI connection.

    Examples
    --------
    Access via the Client class:

        >>> from dfi import Client
        >>> dfi = Client(dfi_token, instance_name, namespace, base_url)
        >>> dfi.get.entities(time_interval=[start_time, end_time])

    Or access only the Get class directly:

        >>> from dfi.connect import Connect
        >>> from dfi.get import Get
        >>> conn = dfi.Connect(api_token, instance_name, namespace, base_url)
        >>> dfi_get = dfi.Get(conn)
        >>> dfi_get.entities(time_interval=[start_time, end_time])

    """

    def __init__(self, conn: Connect) -> None:
        self.conn = conn

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.conn!r})"

    def __str__(self) -> str:
        return f"""Instance of dfi.{self.__class__.__name__} composed with: {self.conn!s}"""

    def api_version(self) -> str:
        """
        Returns the version of the Data Flow Index API.
        """
        with self.conn.api_get("version", stream=False, params=None) as response:
            return response.text

    def records_count(
        self,
        time_interval: Optional[models.TimeInterval] = None,
        polygon: Optional[models.Polygon] = None,
        entities: Optional[List[str]] = None,
    ) -> int:
        """
        Returns the number of records stored in the DFI engine after optional
        time, space and entity ids constraints.

        If all the variables are None it returns the total number of records in the
        database. Start_time and end_time must be both valid datetime, with
        start_time < end_time or both None.

        Parameters
        ----------
        time_interval: Optional[models.TimeInterval] = None
            Tuple with the Lower bound and the upper bound time constraints.
        polygon: Optional[models.Polygon] = None
            List of vertices [[lon1, lat1], [lon2, lat2], ...] or a list of four
            floats representing the bounding box extremes as [lon_min, lat_min, lon_max, lat_max].
            Non-valid input will raise an error.
        entities: Optional[List[str]] = None
            List of entity ids. It must be passed as list also for a single element.

        Returns
        -------
        The number of records stored in the DFI engine.

        Example
        -------
        >>> from dfi import Client
        >>> dfi = Client(dfi_token, instance_name, namespace, base_url)
        >>> start_time = datetime.strptime("2022-01-01T08:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        >>> end_time = datetime.strptime("2022-01-01T08:30:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        >>> entities = ["299eb59a-e47e-48c0-9ad5-89a9ce1303f4"]
        >>> dfi.get.records_count(
        ...     time_interval = (start_time, end_time),
        ...     polygon = None,
        ...     entities = entities,
        ... )

        """
        validate.time_interval(time_interval)
        validate.polygon(polygon)
        validate.entities(entities)

        params = {"instance": self.conn.qualified_instance_name}

        if polygon is None and entities is None:
            if time_interval is not None:
                params["startTime"], params["endTime"] = unpack_and_convert_time_interval(time_interval)
            with self.conn.api_get("count", params=params) as response:
                return self._receive_count(response)

        if polygon is None and entities is not None:
            if time_interval is not None:
                params["startTime"], params["endTime"] = unpack_and_convert_time_interval(time_interval)
            sum_records = 0
            for uid in entities:
                with self.conn.api_get(f"entities/{uid}/count", params=params) as response:
                    sum_records += self._receive_count(response)
            return sum_records

        if isinstance(polygon[0], list) or isinstance(polygon[0], tuple):
            payload = {}
            if time_interval is not None:
                payload["startTime"], payload["endTime"] = unpack_and_convert_time_interval(time_interval)
            if entities is not None:
                payload["include"] = entities
            payload["vertices"] = polygon
            with self.conn.api_post("polygon/count", payload=payload, params=params) as response:
                return self._receive_count(response)

        if isinstance(polygon[0], float):
            if time_interval is not None:
                params["startTime"], params["endTime"] = unpack_and_convert_time_interval(time_interval)
            if entities is not None:
                params["include"] = entities

            min_lng, min_lat, max_lng, max_lat = polygon
            with self.conn.api_get(
                f"bounding-box/{min_lng}/{min_lat}/{max_lng}/{max_lat}/count", params=params
            ) as response:
                return self._receive_count(response)

    def records(
        self,
        time_interval: Optional[models.TimeInterval] = None,
        polygon: Optional[models.Polygon] = None,
        entities: Optional[List[str]] = None,
        add_payload_as_json: bool = False,
    ) -> pd.DataFrame:
        """
        Get the records of the entities appearing within the given time, space and entity ids constraints.

        List of entities and polygon can not be left both to None.

        Start time and end time passed in the time_interval must be both valid datetime,
        with start_time < end_time or both None.

        Parameters
        ----------
        time_interval: Optional[models.TimeInterval] = None
            Tuple with the Lower bound and the upper bound time constraints.
        polygon: Optional[models.Polygon]
            List of vertices [[lon1, lat1], [lon2, lat2], ...] or a list of four
            floats representing the bounding box extremes as [lon_min, lat_min, lon_max, lat_max].
            Non-valid input will raise an error.
        entities: Optional[List[str]] = None
            List of entity ids. It must be passed as list also for a single element.
        add_payload_as_json: bool = False
            If True it parses the payload as a JSON string into the column payload.

        Returns
        -------
        Dataframe with the records of the entities found in polygon, given the input constraints.

        Example
        -------
            >>> from dfi import Client
            >>> dfi = Client(dfi_token, instance_name, namespace, base_url)
            >>> start_time = datetime.strptime("2022-01-01T08:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
            >>> end_time = datetime.strptime("2022-01-01T08:30:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
            >>> entities=["299eb59a-e47e-48c0-9ad5-89a9ce1303f4"]
            >>> dfi.get.records(
            ...     time_interval = (start_time, end_time),
            ...     polygon = None,
            ...     entities = entities,
            ...     add_payload_as_json=True
            ... )
        """
        validate.time_interval(time_interval)
        validate.polygon(polygon)
        validate.entities(entities)

        params = {"instance": self.conn.qualified_instance_name}

        if polygon is None:
            if entities is None:
                raise ValueError("You have to pass a list of entity ids or a polygon, or both.")
            if time_interval is not None:
                params["startTime"], params["endTime"] = unpack_and_convert_time_interval(time_interval)

            df_entities = pd.DataFrame(columns=["entity_id", "timestamp", "longitude", "latitude", "payload"])
            for uid in entities:
                with self.conn.api_get(f"entities/{uid}/history", params=params) as response:
                    data = self._receive_history(response)
                    logger.debug("Uid: %s \nHistory length: %i", uid, len(data))
                    data_formatted = []

                    for item in data:
                        if add_payload_as_json:
                            try:
                                payload = json.loads(item["payload"])
                            except Exception as err:
                                payload = {}
                                logger.debug("Failed to parse payload to JSON: %s for item %s", err, str(item))
                        else:
                            payload = item["payload"]
                        data_formatted.append(
                            [
                                item["id"],
                                datetime.strptime(item["time"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                                item["coordinate"][0],
                                item["coordinate"][1],
                                payload,
                            ]
                        )
                    df_single_entity = pd.DataFrame(
                        data_formatted, columns=["entity_id", "timestamp", "longitude", "latitude", "payload"]
                    )
                    df_entities = pd.concat([df_entities, df_single_entity])
            return df_entities

        payload = {}
        if time_interval is not None:
            payload["startTime"], payload["endTime"] = unpack_and_convert_time_interval(time_interval)

        if entities is not None:
            payload["include"] = entities

        streamed_data = []

        if isinstance(polygon[0], (list, tuple)):
            # polygon passed by VERTICES
            payload["vertices"] = polygon
            with self.conn.api_post("polygon/history", params=params, payload=payload) as response:
                streamed_data = self._receive_history(response)

        if isinstance(polygon[0], float):
            # polygon passed as a BOUNDING BOX
            min_lng, min_lat, max_lng, max_lat = polygon
            with self.conn.api_get(
                f"bounding-box/{min_lng}/{min_lat}/{max_lng}/{max_lat}/history", params=params
            ) as response:
                streamed_data = self._receive_history(response)

        data_formatted = []
        for item in streamed_data:
            if add_payload_as_json:
                try:
                    payload = json.loads(item.get("payload"))
                except Exception as err:
                    payload = {}
                    logger.error("Failed to parse payload to JSON: %s", err)
            else:
                payload = item.get("payload")
            data_formatted.append(
                [
                    item["id"],
                    datetime.strptime(item["time"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                    item["coordinate"][0],
                    item["coordinate"][1],
                    payload,
                ]
            )
        return pd.DataFrame(data_formatted, columns=["entity_id", "timestamp", "longitude", "latitude", "payload"])

    def entities(
        self,
        time_interval: Optional[models.TimeInterval] = None,
        polygon: Optional[models.Polygon] = None,
    ) -> List[Union[str, int]]:
        """
        Get the list of entity ids within a space and optional time constraint.

        If time constraints are not passed, the whole dataset is returned.
        Start time and end time passed in the time_interval must be both valid datetime, with
        start_time < end_time or both None.

        Parameters
        ----------
        time_interval: Optional[models.TimeInterval] = None
            Tuple with the Lower bound and the upper bound time constraints.
        polygon: Optional[models.Polygon] = None
            List of vertices [[lon1, lat1], [lon2, lat2], ...] or a list of four
            floats representing the bounding box extremes as [lon_min, lat_min, lon_max, lat_max].
            Non valid input will raise an error.

        Returns
        -------
        List of unique entities in time interval and polygon.

        Example
        -------
        >>> from dfi import Client
        >>> dfi = Client(dfi_token, instance_name, namespace, base_url)
        >>> start_time = datetime.strptime("2022-01-01T08:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        >>> end_time = datetime.strptime("2022-01-01T08:30:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        >>> pimlico_tube_station =  [
        ...     [-0.13410870522207574, 51.48932327401289],
        ...     [-0.1355577905032419, 51.48887697878598],
        ...     [-0.1339996342869938, 51.487266398812636],
        ...     [-0.13279985400049554, 51.487508959676234],
        ...     [-0.13230124401115972, 51.4875768764868],
        ...     [-0.1319428680814667, 51.487955268294115],
        ...     [-0.1322389177630896, 51.4883918703234],
        ...     [-0.1322389177630896, 51.48887697878598],
        ...     [-0.13301799587057417, 51.48930386996324],
        ...     [-0.13410870522207574, 51.48932327401289],
        ... ]
        >>> dfi.get.entities(
        ...     time_intervals = (start_time, end_time),
        ...     polygon = pimlico_tube_station,
        ... )
        """

        validate.time_interval(time_interval)
        validate.polygon(polygon)

        params = {"instance": self.conn.qualified_instance_name}
        payload = {}

        if polygon is None:
            if time_interval is not None:
                payload["startTime"], payload["endTime"] = unpack_and_convert_time_interval(time_interval)
            with self.conn.api_get("entities", params=params, stream=True) as response:
                return self._receive_entities(response)

        if isinstance(polygon[0], list) or isinstance(polygon[0], tuple):
            # polygon passed by VERTICES
            if time_interval is not None:
                payload["startTime"], payload["endTime"] = unpack_and_convert_time_interval(time_interval)
            payload["vertices"] = polygon
            with self.conn.api_post("polygon/entities", params=params, payload=payload) as response:
                return self._receive_entities(response)

        if isinstance(polygon[0], float):
            # polygon passed as a BOUNDING BOX
            params = {"instance": self.conn.qualified_instance_name}
            if time_interval is not None:
                params["startTime"], params["endTime"] = unpack_and_convert_time_interval(time_interval)
            min_lng, min_lat, max_lng, max_lat = polygon
            with self.conn.api_get(
                f"bounding-box/{min_lng}/{min_lat}/{max_lng}/{max_lat}/entities", params=params, stream=True
            ) as response:
                self._receive_entities(response)

    def _receive_entities(self, response: requests.models.Response) -> List[Any]:
        """
        Helper function to parse clients events as entities and optionally show the progress bar.
        """
        client = sseclient.SSEClient(response)
        results = []
        results_found = False
        previous = 0
        for event in (pbar := tqdm(client.events(), disable=not self.conn.progress_bar)):
            if event.event == "keepAlive":
                continue
            elif event.event == "finish":
                break
            elif event.event == "message":
                results_found = True
                results += [json.loads(event.data)]

                if self.conn.progress_bar:
                    len_results = len(results)
                    if len_results != previous and len_results % 50 == 0:
                        previous = len(results)
                        pbar.set_description(f"Collecting {previous} records")
                        sleep(0.1)  # to avoid Google Colab being overwhelmed

                continue
            elif event.event == "queryError":
                _raise_query_error_event(event)
            else:
                _raise_unexpected_event_found(event)

        if not results_found:
            _raise_message_event_not_reached()
        return results

    def _receive_history(self, response: requests.models.Response) -> List[Any]:
        """
        Helper function to parse clients events as history and optionally show the progress bar.
        """
        client = sseclient.SSEClient(response)

        results = []
        results_found = False
        previous = 0
        for event in (pbar := tqdm(client.events(), disable=not self.conn.progress_bar)):
            if event.event == "keepAlive":
                continue
            elif event.event == "finish":
                break
            elif event.event == "message":
                results_found = True
                results += json.loads(event.data)

                if self.conn.progress_bar:
                    len_results = len(results)
                    if len_results != previous and len_results % 50 == 0:
                        previous = len(results)
                        pbar.set_description(f"Collecting {previous} records")
                        sleep(0.1)  # to avoid Google Colab being overwhelmed

                continue
            elif event.event == "queryError":
                _raise_query_error_event(event)
            else:
                _raise_unexpected_event_found(event)

        if not results_found:
            _raise_message_event_not_reached()
        return results

    def _receive_count(self, response: requests.models.Response) -> int:
        """
        Helper function to parse clients events as counts and optionally show the progress bar.
        """
        client = sseclient.SSEClient(response)

        results = 0
        previous = 0
        results_found = False
        for event in (pbar := tqdm(client.events(), disable=not self.conn.progress_bar)):
            if event.event == "keepAlive":
                continue
            elif event.event == "finish":
                break
            elif event.event == "message":
                results_found = True
                results = json.loads(event.data)

                if self.conn.progress_bar:
                    if results != previous and results % 50 == 0:
                        previous = results
                        pbar.set_description(f"Collecting {previous} records")
                        sleep(0.1)  # to avoid Google Colab being overwhelmed
                continue
            elif event.event == "queryError":
                _raise_query_error_event(event)
            else:
                _raise_unexpected_event_found(event)

        if not results_found:
            _raise_message_event_not_reached()
        return results


def unpack_and_convert_time_interval(time_interval: models.TimeInterval) -> Tuple[str, str]:
    """from time interval to start_time, end_time in isoformat."""
    # The user can give None to one of the two values here.
    # The time interval validation manages the available options.
    start_time, end_time = time_interval
    if start_time is not None:
        start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if end_time is not None:
        end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return start_time, end_time


def _raise_query_error_event(event: sseclient.Event) -> None:
    """helper to raise a QueryError response error"""
    msg = f"event returned QueryError: {event.data}"
    logger.error(msg)
    raise validate.DFIResponseError(msg)


def _raise_unexpected_event_found(event: sseclient.Event) -> None:
    """helper to raise a an unexpected event was found"""
    msg = f"Unexpected event in bagging area: {event}"
    logger.error(msg)
    raise validate.DFIResponseError(msg)


def _raise_message_event_not_reached() -> None:
    """helper to raise a warning if the "message" event was not reached."""
    # see DFIS-694
    msg = "DFI provided no 'message' events."
    logger.warning(msg)
    warnings.warn(msg)
