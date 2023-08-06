#  All Rights Reserved
#  Copyright (c) 2023 Nyria
#
#  This code, including all accompanying software, documentation, and related materials, is the exclusive property
#  of Nyria. All rights are reserved.
#
#  Any use, reproduction, distribution, or modification of the code without the express written
#  permission of Nyria is strictly prohibited.
#
#  No warranty is provided for the code, and Nyria shall not be liable for any claims, damages,
#  or other liability arising from the use or inability to use the code.

from typing import Union, Any
from zenith.Singleton import Singleton


class ServicesManager(Singleton):
    __services = dict()

    @staticmethod
    async def register_service(name: str, class_instance, overwrite: bool = False) -> None:

        """
        Register a service to the service manager.

        Attributes
        ----------
        :param name: The name of the service.
        :param class_instance: The class instance of the service.
        :param overwrite: If the service should be overwritten if it already exists.
        :return: None
        ----------
        """

        if not overwrite and name in ServicesManager.__services:
            raise Exception("Service already exists.")

        ServicesManager.__services[name] = class_instance

    @staticmethod
    async def get_service(name: str) -> Union[Any, None]:

        """
        Get a service from the service manager.

        Attributes
        ----------
        :param name: The name of the service.
        :return: The service.
        ----------
        """

        try:
            return ServicesManager.__services[name]
        except KeyError:
            return None

    @staticmethod
    async def delete_service(name: str) -> None:

        """
        Delete a service from the service manager.

        Attributes
        ----------
        :param name: The name of the service.
        :return: None
        ----------
        """

        try:
            del ServicesManager.__services[name]
        except KeyError:
            return

    @staticmethod
    async def get_all_services() -> dict:

        """
        Get all services from the service manager.

        Attributes
        ----------
        :return: All services.
        ----------
        """

        return ServicesManager.__services
