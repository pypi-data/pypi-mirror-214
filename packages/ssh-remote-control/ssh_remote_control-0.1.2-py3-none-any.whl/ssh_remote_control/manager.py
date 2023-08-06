from __future__ import annotations

from collections.abc import Sequence
from copy import deepcopy
import logging

from .command import Command, CommandExecuteError, CommandFormatError, CommandOutput
from .command_set import CommandSet
from .locker import Locker
from .sensor import Sensor

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Manager"
DEFAULT_COMMAND_TIMEOUT = 15


class Manager(CommandSet, Locker):
    """The Manager class."""

    def __init__(
        self,
        *,
        name: str = DEFAULT_NAME,
        command_set: CommandSet | None = None,
        command_timeout: int = DEFAULT_COMMAND_TIMEOUT,
        logger: logging.Logger = _LOGGER,
    ) -> None:
        Locker.__init__(self)
        CommandSet.__init__(
            self,
            name,
            deepcopy(command_set.service_commands) if command_set else None,
            deepcopy(command_set.sensor_commands) if command_set else None,
        )
        self.command_timeout = command_timeout
        self.logger = logger

    async def async_execute_command_string(
        self, string: str, command_timeout: int | None = None
    ) -> CommandOutput:
        """Execute a command string.

        Raises:
            CommandExecuteError
        """
        raise CommandExecuteError("Not implemented")

    async def async_execute_command(
        self, command: Command, context: dict | None = None
    ) -> CommandOutput:
        """Execute a command.

        Raises:
            CommandFormatError
            CommandExecuteError
        """
        await command.async_execute(self, context)

    async def async_call_service(
        self, key: str, context: dict | None = None
    ) -> CommandOutput:
        """Call a service.

        Raises:
            CommandFormatError
            CommandExecuteError
        """
        command = self.get_service_command(key)
        return await self.async_execute_command(command, context)

    async def async_poll_sensor(self, key: str, *, validate: bool = False) -> Sensor:
        """Poll a sensor.

        Raises:
            CommandFormatError (validate)
            CommandExecuteError (validate)
        """
        sensors = await self.async_poll_sensors([key], validate=validate)
        return sensors[0]

    async def async_poll_sensors(
        self, keys: Sequence[str], *, validate: bool = False
    ) -> list[Sensor]:
        """Poll multiple sensors.

        Raises:
            CommandFormatError (validate)
            CommandExecuteError (validate)
        """
        sensors = [self.get_sensor(key) for key in keys]
        commands = {self.get_sensor_command(key) for key in keys}

        for command in commands:
            try:
                await self.async_execute_command(command)
            except (CommandFormatError, CommandExecuteError):
                if validate:
                    raise

        return sensors

    async def async_set_switch(self, key: str, value: bool) -> None:
        """Set a switch.

        Raises:
            CommandFormatError
            CommandExecuteError
        """
        sensor = await self.async_poll_sensor(key, validate=True)

        if sensor.value == value:
            return

        command = sensor.switch_on if value else sensor.switch_off
        await self.async_execute_command(command, context={"id": sensor.child_id})
        await self.async_poll_sensor(key, validate=True)

    async def async_toggle_switch(self, key: str) -> None:
        """Toggle a switch.

        Raises:
            CommandFormatError
            CommandExecuteError
        """
        sensor = await self.async_poll_sensor(key, validate=True)
        command = sensor.switch_off if sensor.value else sensor.switch_on
        await self.async_execute_command(command, context={"id": sensor.child_id})
        await self.async_poll_sensor(key, validate=True)
