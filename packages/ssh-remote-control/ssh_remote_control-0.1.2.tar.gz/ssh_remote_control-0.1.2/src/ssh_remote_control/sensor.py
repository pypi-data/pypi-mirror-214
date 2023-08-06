from __future__ import annotations

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from .event import Event
from .helpers import name_to_key

if TYPE_CHECKING:
    from .command import Command

_LOGGER = logging.getLogger(__name__)

TRUE_STRINGS = ["true", "enabled", "on", "active", "1"]
FALSE_STRINGS = ["false", "disabled", "off", "inactive", "0"]


def string_to_bool(
    payload_on: str | None, payload_off: str | None, string: str
) -> bool | None:
    """String to bool."""
    if payload_on:
        if string == payload_on:
            return True
        if not payload_off:
            return False

    if payload_off:
        if string == payload_off:
            return False
        if not payload_on:
            return True

    if string.lower() in TRUE_STRINGS:
        return True

    if string.lower() in FALSE_STRINGS:
        return False


class Sensor:
    """The Sensor class."""

    value: Any | None = None
    last_known_value: Any | None = None

    def __init__(
        self,
        name: str,
        key: str | None = None,
        child_id: str | None = None,
        *,
        value_type: type | None = None,
        value_unit: str | None = None,
        value_renderer: Callable[[str], str] | None = None,
        switch_on: Command | None = None,
        switch_off: Command | None = None,
        payload_on: str | None = None,
        payload_off: str | None = None,
        options: dict | None = None,
    ) -> None:
        self.name = name
        self.key = key or name_to_key(name)
        self.value_type = value_type or str
        self.value_unit = value_unit
        self.value_renderer = value_renderer
        self.child_id = child_id
        self.switch_on = switch_on
        self.switch_off = switch_off
        self.payload_on = payload_on
        self.payload_off = payload_off
        self.options = options or {}
        self.on_update = Event()

    @property
    def is_switchable(self) -> bool:
        return self.value_type is bool and self.switch_on and self.switch_off

    def set_value(self, data: str | None) -> None:
        """Set value."""
        value_string = data
        value = None

        if data is not None and self.value_renderer:
            try:
                value_string = self.value_renderer(data)
            except Exception as exc:  # pylint: disable=broad-except
                _LOGGER.warning("%s: Value render error: %s (%s)", self.key, exc, data)

        if value_string is not None:
            try:
                if self.value_type is bool:
                    value = string_to_bool(
                        self.payload_on, self.payload_off, value_string
                    )
                elif self.value_type is int:
                    value = int(float(value_string))
                else:
                    value = self.value_type(value_string)
            except Exception as exc:  # pylint: disable=broad-except
                _LOGGER.warning("%s: Value error: %s (%s)", self.key, exc, value_string)

        self.value = value

        if value is not None:
            self.last_known_value = value

        self.on_update.notify(self)


class DynamicSensor(Sensor):
    """The DynamicSensor class."""

    value: list[Sensor]

    def __init__(
        self,
        name: str,
        key: str | None = None,
        *,
        value_type: type | None = None,
        value_unit: str | None = None,
        value_renderer: Callable[[str], str] | None = None,
        switch_on: str | None = None,
        switch_off: str | None = None,
        payload_on: str | None = None,
        payload_off: str | None = None,
        options: dict | None = None,
    ) -> None:
        super().__init__(
            name,
            key,
            value_type=value_type,
            value_unit=value_unit,
            value_renderer=value_renderer,
            switch_on=switch_on,
            switch_off=switch_off,
            payload_on=payload_on,
            payload_off=payload_off,
            options=options,
        )
        self.value = []
        self.on_child_added = Event()
        self.on_child_removed = Event()

    @property
    def children_by_key(self) -> dict[str, Sensor]:
        return {child.key: child for child in self.value}

    def set_value(self, data: list[list[str, str]] | None) -> None:
        if data is None:
            for child in self.value:
                child.set_value(None)
        else:
            data_by_key = {
                f"{self.key}_{name_to_key(child_id)}": (child_id, value_string)
                for child_id, value_string in data
            }

            for key, (child_id, _) in data_by_key.items():
                if key not in self.children_by_key:
                    self.add_child(key, child_id)

            for child in self.value:
                if child.key in data_by_key:
                    _, value_string = data_by_key[child.key]
                    child.set_value(value_string)
                else:
                    self.remove_child(child)

        self.on_update.notify(self)

    def add_child(self, key: str, child_id: str) -> None:
        """Add a child."""
        child = Sensor(
            f"{self.name} {child_id}",
            key,
            child_id,
            value_type=self.value_type,
            value_unit=self.value_unit,
            value_renderer=self.value_renderer,
            switch_on=self.switch_on,
            switch_off=self.switch_off,
            options=self.options,
        )
        self.value.append(child)
        self.on_child_added.notify(self, child)

    def remove_child(self, child: Sensor) -> None:
        """Remove a child."""
        if child.value is not None:
            child.set_value(None)

        self.value.remove(child)
        self.on_child_removed.notify(self, child)
