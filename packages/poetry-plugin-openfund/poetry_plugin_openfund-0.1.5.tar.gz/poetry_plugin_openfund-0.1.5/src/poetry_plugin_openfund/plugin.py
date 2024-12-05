from __future__ import annotations

import logging

from importlib import import_module
from typing import TYPE_CHECKING

from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.console.commands.command import Command

from poetry_plugin_openfund.openfund import OpenfundCommand

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


# def load_command(name: str) -> Callable[[], Command]:
#     words = name.split(" ")
#     module = import_module("poetry_plugin_openfund." + ".".join(words))
#     command_class = getattr(module, "".join(c.title() for c in words) + "Command")
#     command: Command = command_class()
#     return command


def factory_command():
    return OpenfundCommand()


class OpenfundApplicationPlugin(ApplicationPlugin):
    def __init__(self) -> None:
        logger.debug("------- OpenfundApplicationPlugin init ...")
        super().__init__()

    def activate(self, application):
        logger.debug("------- OpenfundApplicationPlugin activate ...")
        # factory = load_command("openfund")
        # factory = factory_command
        application.command_loader.register_factory("openfund", factory_command)
