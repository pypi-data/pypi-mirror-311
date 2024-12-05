from __future__ import annotations

import logging

from typing import TYPE_CHECKING
from typing import Any

from cleo.helpers import argument
from cleo.helpers import option

from poetry.console.commands.command import Command as BaseCommand

from openfund.core.api_tools.binance_tools import BinanceTools
from openfund.core.base_collector import Collector
from openfund.core.services.um_futures_collector import KLinesCollector

if TYPE_CHECKING:
    from collections.abc import Callable


logger = logging.getLogger(__name__)


class OpenfundCommand(BaseCommand):

    name = "openfund"

    description = "Open fund command."

    arguments = [
        argument("key", "Setting key.", optional=True),
        # argument("value", "Setting value.", optional=True, multiple=True),
    ]

    options = [
        option("start", None, "start service."),
        option("stop", None, "stop service."),
        option("pause", None, "pause service."),
        option("resume", None, "resume service."),
        # option("unset", None, "Unset configuration setting."),
        # option("local", None, "Set/Get from the project's local configuration."),
    ]

    def __init__(self) -> None:
        logger.debug("------- OpenfundCommand init ...")
        super().__init__()
        self._collector: Collector = None

    def handle(self) -> int:
        from poetry.utils._compat import metadata

        logger.debug("------- OpenfundCommand handle ...")
        # Client
        key = self.argument("key")

        logger.debug("------- key is %s ...", key)
        if key == "times":

            logger.debug(
                "------- BinanceTools.time is %s  -------", BinanceTools.get_time()
            )

            return 0

        if key == "account":

            logger.debug(
                "------- BinanceTools.account is %s  -------",
                BinanceTools().get_account(),
            )

            return 0

        if key == "klines" and self.option("start"):

            self._collector = KLinesCollector()
            logger.debug("------- Collector startting ... -------")
            return self._collector.start()

        if key == "klines" and self.option("pause"):
            logger.debug("------- Collector pause ! -------")
            if self._collector is not None:
                return self._collector.pause()
            return 0
        if key == "klines" and self.option("resume"):
            logger.debug("------- Collector resume ! -------")
            if self._collector is not None:
                return self._collector.resume()
            return 0

        if key == "klines" and self.option("stop"):
            logger.debug("------- Collector stop ! -------")
            if self._collector is not None:
                return self._collector.stop()
            return 0

        # The metadata.version that we import for Python 3.7 is untyped, work around
        # that.
        version: Callable[[str], str] = metadata.version

        self.line(
            f"""\
        <info>Openfund - Funder for Python

        Version: {version('poetry_plugin_openfund')}
        """
        )

        return 0
