from collections.abc import Callable


class Event:
    """The Event class."""

    def __init__(self) -> None:
        self._subscribers: list[Callable] = []

    def subscribe(self, subscriber) -> None:
        """Subscribe."""
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber) -> None:
        """Unsubscribe."""
        self._subscribers.remove(subscriber)

    def notify(self, *args, **kwargs) -> None:
        """Notify."""
        for subscriber in self._subscribers:
            subscriber(*args, **kwargs)
