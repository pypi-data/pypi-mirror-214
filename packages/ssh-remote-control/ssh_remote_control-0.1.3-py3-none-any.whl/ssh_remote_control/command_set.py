from .command import SensorCommand, ServiceCommand
from .sensor import Sensor


class CommandSet:
    """The CommandSet class."""

    def __init__(
        self,
        name: str,
        service_commands: list[ServiceCommand] | None = None,
        sensor_commands: list[SensorCommand] | None = None,
    ) -> None:
        self.name = name
        self.service_commands = service_commands or []
        self.sensor_commands = sensor_commands or []

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
        """Get a service command."""
        return self.service_commands_by_key[key]

    def get_sensor_command(self, key: str) -> SensorCommand:
        """Get a sensor command."""
        return self.sensor_commands_by_sensor_key[key]

    def get_sensor(self, key: str) -> Sensor:
        """Get a sensor."""
        return self.sensors_by_key[key]

    def remove_service_command(self, key: str) -> None:
        """Remove a service command."""
        command = self.get_service_command(key)
        self.service_commands.remove(command)

    def remove_sensor(self, key: str) -> None:
        """Remove a sensor.

        Remove the sensor command if it doesnt have any other sensors.
        """
        command = self.get_sensor_command(key)
        command.remove_sensor(key)

        if not command.sensors_by_key:
            self.sensor_commands.remove(command)
