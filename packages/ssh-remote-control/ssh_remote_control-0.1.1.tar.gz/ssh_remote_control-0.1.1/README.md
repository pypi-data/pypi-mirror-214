# SSH Remote Control

## Initialize

```python
from ssh_remote_control import Remote

remote = Remote("192.168.0.123", ssh_user="user", ssh_password="password")

await remote.async_update_state(True)

# Check the state
remote.state.is_online
remote.state.is_connected
```

## Initialize with default commands

```python
from ssh_remote_control.default_commands.linux import services, sensors, SensorKey

remote = Remote(
  "192.168.0.123",
  ssh_user="user",
  ssh_password="password",
  service_commands=services,
  sensor_commands=sensors
)

await remote.async_update_state(True)

# Get a sensor
sensor = remote.get_sensor(SensorKey.CPU_LOAD)
sensor.value
sensor.value_unit

# Poll a sensor
sensor = await remote.async_poll_sensor(SensorKey.TEMPERATURE)
sensor.value
sensor.value_unit
```
