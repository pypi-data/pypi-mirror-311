import json
from datetime import datetime
from re import match
from typing import BinaryIO

from aiohttp import ClientConnectionError, BasicAuth, ClientSession
from loguru import logger

from idugeoserverclient.client.client_interface import IIduGeoserverClient
from idugeoserverclient.models.datastore_model import DatastoreModel
from idugeoserverclient.models.layer_model import LayerModel


class IduGeoserverClient(IIduGeoserverClient):

    def __init__(self, host: str, port: int, login: str, password: str):
        """
        Geoserver client instance
        """
        self._login = login
        self._password = password
        self._prefix = "/geoserver/rest"
        self._api_url = f"http://{host}:{port}{self._prefix}"
        logger.debug(f"Running configuration with {self._api_url} @{self._login}:{self._password}")

    async def upload_layer(
            self, workspace_name: str, file: BinaryIO, layer_type: str, created_at: str | datetime,
            replace_existing: bool = True, style_name: str | None = None, *args
    ) -> None:

        if file.name.split(".")[-1] != "gpkg":
            raise NameError("Received not .gpkg file. Please, reformat it to gpkg")

        if replace_existing:
            filtered_layers = await self.get_layers(workspace_name, layer_type, *args)
            for layer in filtered_layers:
                await self.delete_layer(workspace_name, layer.name)
                await self.delete_datastore(workspace_name, layer.name)

        if type(created_at) is str:
            created_at = datetime.strptime(created_at, "%Y-%m-%d-%H-%M-%S")
        created_at = created_at.strftime("%Y-%m-%d-%H-%M-%S")
        layer_name = f"{created_at}_{layer_type}"
        for arg in args:
            layer_name += f"_{str(arg)}"
        async with ClientSession() as session:
            try:
                async with session.put(
                    f"{self._api_url}/workspaces/{workspace_name}/datastores/{layer_name}/file.gpkg",
                    data=file,
                    headers={"Content-Type": "application/json"},
                    auth=BasicAuth(self._login, self._password)
                ) as response:
                    if response.status not in [200, 201]:
                        raise RuntimeError(
                            f"{response.status}, HTML_OF_ERROR: {(await response.read()).decode('utf-8')}"
                        )
                if style_name:
                    async with session.put(
                        f"{self._api_url}/workspaces/{workspace_name}/layers/{layer_name}",
                        data="<layer><defaultStyle><name>{}</name></defaultStyle></layer>".format(
                            style_name
                        ),
                        headers={"Content-Type": "application/xml"},
                        auth=BasicAuth(self._login, self._password)
                    ) as response:
                        if response.status not in [200, 201]:
                            raise RuntimeError(
                                f"{response.status}, HTML_OF_ERROR: {(await response.read()).decode('utf-8')}"
                            )
            except ClientConnectionError as e:
                raise ConnectionError("GEOSERVER_NOT_AVAILABLE") from e
        return

    async def get_layers(self, workspace_name: str, layer_type: str | None = None, *args) -> list[LayerModel]:
        async with ClientSession() as session:
            try:
                async with session.get(
                    f"{self._api_url}/workspaces/{workspace_name}/layers",
                    headers={"Content-Type": "application/json"},
                    auth=BasicAuth(self._login, password=self._password)
                ) as response:
                    if response.status not in [200, 201]:
                        raise RuntimeError(f"{response.status}, HTML_OF_ERROR: {(await response.read()).decode('utf-8')}")
                    data = (await response.read()).decode("utf-8")
            except ClientConnectionError as e:
                raise ConnectionError("GEOSERVER_NOT_AVAILABLE") from e
        deserialized_data: dict = json.loads(data)
        if deserialized_data["layers"] == "":
            raise RuntimeError("WORKSPACE_NOT_FOUND")
        data = deserialized_data.get("layers", {}).get("layer", [])
        if layer_type:
            pattern = f".*_{layer_type}"
            if len(args) != 0:
                pattern += f"{''.join([f'_{str(arg)}' for arg in args])}$"
            data = list(filter(
                lambda v: match(
                    pattern, v["name"]
                ), data))
        return [LayerModel(**layer) for layer in data]

    async def delete_layer(self, workspace_name: str, layer_name: str) -> None:
        async with ClientSession() as session:
            try:
                async with session.delete(
                    f"{self._api_url}/workspaces/{workspace_name}/layers/{layer_name}",
                    auth=BasicAuth(self._login, self._password)
                ) as response:
                    if response.status not in [200, 201]:
                        raise RuntimeError(f"{response.status}, HTML_OF_ERROR: {(await response.read()).decode('utf-8')}")
                    return
            except ClientConnectionError as e:
                raise ConnectionError("GEOSERVER_NOT_AVAILABLE") from e

    async def get_datastores(
            self, workspace_name: str, datastore_type: str | None = None, *args
    ) -> list[DatastoreModel]:
        async with ClientSession() as session:
            try:
                async with session.get(
                    f"{self._api_url}/workspaces/{workspace_name}/datastores",
                    headers={"Content-Type": "application/json"},
                    auth=BasicAuth(self._login, self._password)
                ) as response:
                    if response.status not in [200, 201]:
                        raise RuntimeError(f"{response.status}, HTML_OF_ERROR: {(await response.read()).decode('utf-8')}")
                    data = (await response.read()).decode("utf-8")
            except ClientConnectionError as e:
                raise ConnectionError("GEOSERVER_NOT_AVAILABLE") from e
        deserialized_data: dict = json.loads(data)
        data = deserialized_data.get("dataStores", {}).get("dataStore", [])
        if datastore_type:
            pattern = f".*_{datastore_type}"
            if len(args) != 0:
                pattern += f"{''.join([f'_{str(arg)}' for arg in args])}$"
            data = list(filter(
                lambda v: match(
                    pattern, v["name"]
                ), data))
        return [DatastoreModel(**datastore) for datastore in data]

    async def delete_datastore(self, workspace_name: str, datastore_name: str) -> None:
        async with ClientSession() as session:
            try:
                async with session.delete(
                    f"{self._api_url}/workspaces/{workspace_name}/datastores/{datastore_name}?recurse=true",
                    auth=BasicAuth(self._login, self._password)
                ) as response:
                    if response.status not in [200, 201]:
                        raise RuntimeError(f"{response.status}, HTML_OF_ERROR: {(await response.read()).decode('utf-8')}")
                    return
            except ClientConnectionError as e:
                raise ConnectionError("GEOSERVER_NOT_AVAILABLE") from e
