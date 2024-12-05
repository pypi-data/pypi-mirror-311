from abc import ABC, ABCMeta
from dataclasses import dataclass
from enum import Enum, auto
from typing import Self, Optional

from edri.dataclass.directive import ResponseDirective
from edri.dataclass.event import Event


class MiddlewareMeta(ABCMeta):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        # Dynamically create the list of methods from the class being created
        required_methods = []
        for base in cls.__mro__:
            for method_name, method in base.__dict__.items():
                if callable(method) and not method_name.startswith('__'):
                    required_methods.append(method_name)

        # Check if at least one method is implemented in the subclass
        if not any(attr in cls.__dict__ for attr in required_methods):
            raise TypeError(
                f"Class '{cls.__name__}' must implement at least one of the following methods: {", ".join(required_methods)}. "
                "Ensure that your class provides an implementation for at least one of these methods."
            )


@dataclass
class MiddlewareControl:
    """
    Encapsulates the outcome of middleware processing with details on the action type, optional data, errors,
    and an optional replacement event.
    """

    class ActionType(Enum):
        """Enum to define middleware processing actions."""
        CONTINUE = auto()
        STOP = auto()
        REPLACE_EVENT = auto()

    action: ActionType
    event: Optional[Event] = None

    @classmethod
    def continue_processing(cls) -> Self:
        """Creates a MiddlewareControl instance indicating processing should continue."""
        return cls(action=cls.ActionType.CONTINUE)

    @classmethod
    def stop_processing(cls, directive: Optional[ResponseDirective] = None) -> Self:
        """Creates a MiddlewareControl instance indicating processing should stop."""
        return cls(action=cls.ActionType.STOP)

    @classmethod
    def replace_event(cls, event: Event) -> Self:
        """
        Creates a MiddlewareControl instance that replaces the current event with a new one.

        Args:
            event (Event): The event that should replace the current event in processing.

        Returns:
            MiddlewareControl: An instance with action set to REPLACE_EVENT.
        """
        return cls(action=cls.ActionType.REPLACE_EVENT, event=event)


class Middleware(ABC, metaclass=MiddlewareMeta):
    """
    Abstract base class for middleware components.
    Middleware classes derived from this must implement at least one of
    'process_request' and 'process_response'.
    """

    def process_request(self, event: Event) -> MiddlewareControl:
        """
        Method to process the request before it reaches the main application logic.
        Should be implemented in a subclass.

        :param event: The request event to be processed.
        """
        raise NotImplementedError("Must implement process_request or process_response")

    def process_response(self, event: Event) -> MiddlewareControl:
        """
        Method to process the response before it is sent to the client.
        Should be implemented in a subclass.

        :param event: The response event to be processed.
        """
        raise NotImplementedError("Must implement process_request or process_response")

    @classmethod
    def __getattr__(cls, name):
        prefix = "is_"
        if name.startswith(prefix):
            capability_name = f"process_{name[len(prefix):]}"
            method = cls.__dict__.get(capability_name)
            return callable(method)
        raise AttributeError("type object '%s' has no attribute '%s'", cls.__name__, name)
