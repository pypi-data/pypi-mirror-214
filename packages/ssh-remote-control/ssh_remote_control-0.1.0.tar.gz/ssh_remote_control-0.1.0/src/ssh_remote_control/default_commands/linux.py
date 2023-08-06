from ..command import Command, SensorCommand, ServiceCommand
from ..sensor import DynamicSensor, Sensor
from .const import SensorKey, SensorName, ServiceKey, ServiceName

NAME = "Linux"

services = [
    ServiceCommand(
        "/sbin/shutdown -h now",
        ServiceName.TURN_OFF,
        ServiceKey.TURN_OFF,
    ),
    ServiceCommand(
        "/sbin/shutdown -r now",
        ServiceName.RESTART,
        ServiceKey.RESTART,
    ),
]

sensors = [
    SensorCommand(
        "cat hundi",
        [
            DynamicSensor(
                "Hundi",
                value_type=bool,
                switch_on=Command("sed -i -e 's/{id} off/{id} on/g' hundi"),
                switch_off=Command("sed -i -e 's/{id} on/{id} off/g' hundi"),
            )
        ],
    ),
    SensorCommand(
        "cat /sys/class/net/{interface}/address",
        [
            Sensor(
                SensorName.MAC_ADDRESS,
                SensorKey.MAC_ADDRESS,
            )
        ],
    ),
    SensorCommand(
        "cat /sys/class/net/{interface}/device/power/wakeup",
        [
            Sensor(
                SensorName.WOL_SUPPORT,
                SensorKey.WOL_SUPPORT,
                value_type=bool,
                payload_on="enabled",
            )
        ],
    ),
    SensorCommand(
        "/sbin/route -n | awk '($1 == \"0.0.0.0\") {{print $NF; exit}}'",
        [
            Sensor(
                SensorName.INTERFACE,
                SensorKey.INTERFACE,
            )
        ],
    ),
    SensorCommand(
        "uname -a | awk '{{print $1; print $3; print $2; print $(NF-1);}}'",
        [
            Sensor(
                SensorName.OS_NAME,
                SensorKey.OS_NAME,
            ),
            Sensor(
                SensorName.OS_VERSION,
                SensorKey.OS_VERSION,
            ),
            Sensor(
                SensorName.HOSTNAME,
                SensorKey.HOSTNAME,
            ),
            Sensor(
                SensorName.MACHINE_TYPE,
                SensorKey.MACHINE_TYPE,
            ),
        ],
    ),
    # TODO: OS_ARCHITECTURE
    SensorCommand(
        "free -m | awk 'tolower($0)~/mem/ {{print $2}}'",
        [
            Sensor(
                SensorName.TOTAL_MEMORY,
                SensorKey.TOTAL_MEMORY,
                value_type=int,
                value_unit="MB",
            )
        ],
    ),
    SensorCommand(
        "free -m | awk 'tolower($0)~/mem/ {{print $4}}'",
        [
            Sensor(
                SensorName.FREE_MEMORY,
                SensorKey.FREE_MEMORY,
                value_type=int,
                value_unit="MB",
            )
        ],
        interval=30,
    ),
    SensorCommand(
        "df -m | awk '/^\\/dev\\// {{print $6 \"|\" $4}}'",
        [
            DynamicSensor(
                SensorName.FREE_DISK_SPACE,
                SensorKey.FREE_DISK_SPACE,
                value_type=int,
                value_unit="MB",
            )
        ],
        interval=300,
        separator="|",
    ),
    SensorCommand(
        "top -bn1 | head -n3 | awk 'tolower($0)~/cpu/ "
        + "{{for(i=1;i<NF;i++){{if(tolower($i)~/cpu/)"
        + "{{idle=$(i+7); print 100-idle;}}}}}}'",
        [
            Sensor(
                SensorName.CPU_LOAD,
                SensorKey.CPU_LOAD,
                value_type=int,
                value_unit="%",
            )
        ],
        interval=30,
    ),
    SensorCommand(
        "echo $(($(cat /sys/class/thermal/thermal_zone0/temp) / 1000))",
        [
            Sensor(
                SensorName.TEMPERATURE,
                SensorKey.TEMPERATURE,
                value_type=int,
                value_unit="°C",
            )
        ],
        interval=60,
    ),
]
