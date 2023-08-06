from __future__ import annotations

import logging
from collections.abc import Sequence
from copy import deepcopy

from .command import (
    Command,
    CommandExecuteError,
    CommandFormatError,
    CommandOutput,
    SensorCommand,
    ServiceCommand,
)
from .locker import Locker
from .sensor import Sensor

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Manager"
DEFAULT_COMMAND_TIMEOUT = 15


class Manager(Locker):
    """The Manager class."""

    def __init__(
        self,
        *,
        name: str = DEFAULT_NAME,
        command_timeout: int = DEFAULT_COMMAND_TIMEOUT,
        service_commands: list[ServiceCommand] | None = None,
        sensor_commands: list[SensorCommand] | None = None,
        logger: logging.Logger = _LOGGER,
    ) -> None:
        super().__init__()
        self.name = name
        self.command_timeout = command_timeout
        self.service_commands = deepcopy(service_commands or [])
        self.sensor_commands = deepcopy(sensor_commands or [])
        self.logger = logger

    @property
    def service_commands_by_key(self) -> dict[str, ServiceCommand]:
        """Service commands by key."""
        return {command.key: command for command in self.service_commands}

    @property
    def sensor_commands_by_sensor_key(self) -> dict[str, SensorCommand]:
        """Sensor commands by sensor key."""
        result = {}
        for command in self.sensor_commands:
            result.update({key: command for key in command.sensors_by_key})
        return result

    @property
    def sensors_by_key(self) -> dict[str, Sensor]:
        """Sensors by key."""
        result = {}
        for command in self.sensor_commands:
            result.update(command.sensors_by_key)
        return result

    def add_service_command(self, command: ServiceCommand) -> None:
        """Add a service command.

        Remove existing service command with the same key.
        """
        if command.key in self.service_commands_by_key:
            self.remove_service_command(command.key)

        self.service_commands.append(command)

    def add_sensor_command(self, command: SensorCommand) -> None:
        """Add a sensor command.

        Remove existing sensors with the same keys.
        """
        for sensor in command.sensors:
            if sensor.key in self.sensors_by_key:
                self.remove_sensor(sensor.key)

        self.sensor_commands.append(command)

    def get_service_command(self, key: str) -> ServiceCommand:
        """Get a service command.

        Raises:
            KeyError
        """
        return self.service_commands_by_key[key]

    def get_sensor_command(self, key: str) -> SensorCommand:
        """Get a sensor command.

        Raises:
            KeyError
        """
        return self.sensor_commands_by_sensor_key[key]

    def get_sensor(self, key: str) -> Sensor:
        """Get a sensor.

        Raises:
            KeyError
        """
        return self.sensors_by_key[key]

    def remove_service_command(self, key: str) -> None:
        """Remove a service command.

        Raises:
            KeyError
        """
        command = self.get_service_command(key)
        self.service_commands.remove(command)

    def remove_sensor(self, key: str) -> None:
        """Remove a sensor.

        Remove the sensor command if it doesnt have any other sensors.

        Raises:
            KeyError
        """
        command = self.get_sensor_command(key)
        command.remove_sensor(key)

        if not command.sensors_by_key:
            self.sensor_commands.remove(command)

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
            KeyError
            CommandFormatError
            CommandExecuteError
        """
        command = self.get_service_command(key)
        return await self.async_execute_command(command, context)

    async def async_poll_sensor(self, key: str, validate: bool = False) -> Sensor:
        """Poll a sensor.

        Raises:
            KeyError
            CommandFormatError (validate)
            CommandExecuteError (validate)
        """
        sensors = await self.async_poll_sensors([key], validate)
        return sensors[0]

    async def async_poll_sensors(
        self, keys: Sequence[str], validate: bool = False
    ) -> list[Sensor]:
        """Poll multiple sensors.

        Raises:
            KeyError
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
            KeyError
            CommandFormatError
            CommandExecuteError
        """
        sensor = await self.async_poll_sensor(key, True)

        if sensor.value == value:
            return

        command = sensor.switch_on if value else sensor.switch_off
        await self.async_execute_command(command, context={"id": sensor.child_id})
        await self.async_poll_sensor(key, True)

    async def async_toggle_switch(self, key: str) -> None:
        """Toggle a switch.

        Raises:
            KeyError
            CommandFormatError
            CommandExecuteError
        """
        sensor = await self.async_poll_sensor(key, True)
        command = sensor.switch_off if sensor.value else sensor.switch_on
        await self.async_execute_command(command, context={"id": sensor.child_id})
        await self.async_poll_sensor(key, True)
