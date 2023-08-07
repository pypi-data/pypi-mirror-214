from ..command import SensorCommand, ServiceCommand
from ..command_set import CommandSet
from ..sensor import Sensor
from .const import SensorKey, SensorName, ServiceKey, ServiceName

windows_cmd = CommandSet(
    "Windows",
    [
        ServiceCommand(
            "shutdown -t 0",
            ServiceName.TURN_OFF,
            ServiceKey.TURN_OFF,
        ),
        ServiceCommand(
            "shutdown -r -t 0",
            ServiceName.RESTART,
            ServiceKey.RESTART,
        ),
    ],
    [
        # TODO: MAC_ADDRESS
        # TODO: WOL_SUPPORT
        # TODO: INTERFACE
        SensorCommand(
            "for /f \"skip=1 delims=\" %i in ('wmic ComputerSystem get SystemType') "
            + "do @echo %i",
            [
                Sensor(
                    SensorName.MACHINE_TYPE,
                    SensorKey.MACHINE_TYPE,
                )
            ],
        ),
        SensorCommand(
            "hostname",
            [
                Sensor(
                    SensorName.HOSTNAME,
                    SensorKey.HOSTNAME,
                )
            ],
        ),
        SensorCommand(
            "for /f \"skip=1 delims=\" %i in ('wmic OS get Caption') do @echo %i",
            [
                Sensor(
                    SensorName.OS_NAME,
                    SensorKey.OS_NAME,
                )
            ],
        ),
        SensorCommand(
            "for /f \"skip=1 delims=\" %i in ('wmic OS get Version') do @echo %i",
            [
                Sensor(
                    SensorName.OS_VERSION,
                    SensorKey.OS_VERSION,
                )
            ],
        ),
        SensorCommand(
            "for /f \"skip=1 delims=\" %i in ('wmic OS get OSArchitecture') do @echo %i",
            [
                Sensor(
                    SensorName.OS_ARCHITECTURE,
                    SensorKey.OS_ARCHITECTURE,
                )
            ],
        ),
        SensorCommand(
            # TODO: Should return MB but number is too long
            "for /f  %i in ('wmic ComputerSystem get TotalPhysicalMemory ^| "
            + 'findstr /r "\\<[0-9][0-9]*\\>"\') '
            + "do set /a mb=%i / 1024 / 1024",
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
            "for /f  %i in ('wmic OS get FreePhysicalMemory ^| "
            + 'findstr /r "\\<[0-9][0-9]*\\>"\') '
            + "do set /a mb=%i / 1024",
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
        # TODO: FREE_DISK_SPACE
        SensorCommand(
            "for /f \"skip=1\" %i in ('wmic CPU get LoadPercentage') do @echo %i",
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
            "for /f  %i in ('wmic /namespace:\\\\root\\wmi "
            + "PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature ^| "
            + 'findstr /r "\\<[0-9][0-9]*\\>"\') '
            + "do set /a mb=(%i - 2732) / 10",
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
    ],
)
