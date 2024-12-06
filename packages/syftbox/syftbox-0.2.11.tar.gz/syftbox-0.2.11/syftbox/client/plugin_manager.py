from __future__ import annotations

from typing_extensions import Optional

from syftbox.client.base import Plugins, SyftClientInterface
from syftbox.client.exceptions import SyftPluginException
from syftbox.client.plugins.apps import AppRunner
from syftbox.client.plugins.sync.manager import SyncManager


class PluginManager(Plugins):
    def __init__(
        self,
        client: SyftClientInterface,
        sync_manager: Optional[SyncManager] = None,
        app_runner: Optional[AppRunner] = None,
        **kwargs,
    ):
        self.__client = client
        self.__sync_manager = sync_manager
        self.__app_runner = app_runner

    @property
    def sync_manager(self):
        """the sync manager. lazily initialized"""
        if self.__sync_manager is None:
            try:
                self.__sync_manager = SyncManager(self.__client)
            except Exception as e:
                raise SyftPluginException(f"Failed to initialize sync manager - {e}") from e
        return self.__sync_manager

    @property
    def app_runner(self):
        """the app runner. lazily initialized"""
        if self.__app_runner is None:
            try:
                self.__app_runner = AppRunner(self.__client)
            except Exception as e:
                raise SyftPluginException(f"Failed to initialize app runner - {e}") from e
        return self.__app_runner

    def start(self):
        self.sync_manager.start()
        self.app_runner.start()

    def stop(self):
        if self.__sync_manager is not None:
            self.__sync_manager.stop()

        if self.__app_runner is not None:
            self.__app_runner.stop()
