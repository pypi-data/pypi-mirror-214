# progress.py

import sys
import datetime as dt
import time
from time import strftime
from time import gmtime

import threading
from typing import (
    Optional, Type, Generator, Iterable,
    Union, Any, Callable, Literal
)

from represent import BaseModel, Modifiers

__all__ = [
    "Spinner",
    "spinner",
    "format_seconds"
]

def format_seconds(
        seconds: float,
        length: Optional[int] = None,
        side: Optional[Literal['left', 'right', 'center']] = None) -> str:
    """
    Formats the time in seconds.

    :param seconds: The seconds.
    :param length: The length of the string.
    :param side: The side to set the message in the padding.

    :return: The time message.
    """

    message = strftime("%H:%M:%S", gmtime(seconds))

    if side is None:
        return message
    # end if

    if length is None:
        length = len(message)

    else:
        length = max(length, len(message))
    # end if

    length -= len(message)

    if side.lower() == "right":
        message = f"{0: <{length}}{message}"

    elif side.lower() == "left":
        message = f"{message}{0: <{length}}"

    elif side.lower() == "center":
        message = f"{0: <{length / 2}}{message}{0: <{length / 2 + length % 2}}"

    else:
        raise ValueError(
            f"side must be one of 'left', 'right', "
            f"or 'center', not: {side}."
        )
    # end if

    return message
# end format_seconds

class Spinner(BaseModel):
    """
    A class to create a terminal spinning wheel.

    Using this object it is able to create a context manager for
    continuously print a progress wheel, and a message.

    attributes:

    - delay:
        The delay between output updates of iterations.

    - message:
        The printed message with the progress wheel.

    - silence:
        The value to silence the output.

    >>> with Spinner(message="Processing")
    >>>     while True:
    >>>         pass
    >>>     # end while
    >>> # end Spinner
    """

    modifiers = Modifiers(excluded=["spinner_generator"])

    RUNNING = False

    DELAY = 0.25

    instances = []

    ELEMENTS = '/-\\|'

    def __init__(
            self,
            title: Optional[str] = None,
            message: Optional[str] = None,
            delay: Optional[Union[int, float, dt.timedelta]] = None,
            silence: Optional[bool] = None,
            stay: Optional[Callable[[], bool]] = None,
            counter: Optional[bool] = False,
            clean: Optional[bool] = True,
            elements: Optional[Iterable[str]] = None,
            complete: Optional[Union[bool, str]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param title: The title of the process.
        :param message: The message to display.
        :param delay: The delay value.
        :param silence: The value to hide the progress bar.
        :param stay: A function to keep or break the loop.
        :param counter: The value to add a counter of seconds to the message.
        :param clean: The value to clean the message after exiting.
        :param elements: The elements to show.
        :param complete: The value for a complete message.
        """

        if complete is True:
            complete = "Complete"
        # end if

        if elements is None:
            elements = self.ELEMENTS
        # end if

        self.message = message
        self.complete = complete
        self.title = title or ""
        self.delay = delay or self.DELAY
        self.silence = silence
        self.stay = stay
        self.counter = counter
        self.clean = clean
        self.elements = elements

        self.spinner_generator = self.spinning_cursor()

        self.running = False

        self.start = None
        self.time = None
        self.output = None
    # end __init__

    def __enter__(self) -> Any:
        """Enters the object to run the task."""

        self.spin()

        return self
    # end __enter__

    def __exit__(
            self,
            exception_type: Type[Exception],
            exception: Exception,
            traceback
    ) -> Optional[bool]:
        """
        Exists the spinner object and ends the task.

        :param exception_type: The exception type.
        :param exception: The exception value.
        :param traceback: The traceback of the exception.

        :return: The status value
        """

        self.stop()

        if exception is not None:
            return False
        # end if

        return True
    # end __exit__

    def stop(self) -> None:

        self.running = False

        Spinner.instances.remove(self)

        Spinner.RUNNING = bool(Spinner.instances)

        if self.delay:
            time.sleep(self.delay)
        # end if

        if self.clean or self.complete:
            sys.stdout.write(
                ('\b' * len(self.output)) +
                (' ' * len(self.output)) +
                ('\b' * len(self.output))
            )
            sys.stdout.flush()
        # end if

        if self.complete:
            self.output = self.create_message(
                cursor="", text=self.complete
            )

            sys.stdout.write(self.output + "\n")
            sys.stdout.flush()
        # end if
    # ene stop

    def spin(self) -> None:
        """Runs the spinner."""

        self.running = True

        self.start = time.time()
        self.time = time.time()

        threading.Thread(target=self._run).start()

        Spinner.instances.append(self)
    # end start

    def create_message(
            self,
            cursor: Optional[str] = None,
            text: Optional[str] = None
    ) -> str:
        """
        Creates the message to display.

        :param cursor: The current spinner cursor.
        :param text: The text message.

        :return: The total output message.
        """

        text = text or ""
        cursor = cursor or ""

        message = self.title

        if not message:
            message = ""

        else:
            message += ": "
        # end if

        message += text

        if not message:
            message = ""

        else:
            message += " "
        # end if

        if self.counter:
            current = self.time - self.start

            message += format_seconds(current)
        # end if

        if not cursor:
            return message + " "
        # end if

        return message + " " + cursor + " "
    # end create_message

    def spinning_cursor(self) -> Generator[str, None, None]:
        """
        Returns the current spinner value.

        :return: The current state of the cursor.
        """

        while True:
            for cursor in self.elements:
                self.time = time.time()

                if self.silence:
                    continue
                # end if

                self.output = self.create_message(
                    cursor=cursor, text=self.message
                )

                yield self.output
            # end for
        # end while
    # end spinning_cursor

    def _run(self) -> None:
        """Runs the spinning wheel."""

        delay = self.delay

        if isinstance(delay, dt.timedelta):
            delay = delay.total_seconds()
        # end if

        while (
            self.running and
            (
                (self.stay is None) or
                (callable(self.stay) and self.stay())
            )
        ):
            Spinner.RUNNING = True

            next_output = next(self.spinner_generator)

            sys.stdout.write(next_output)
            sys.stdout.flush()

            if delay:
                time.sleep(delay)
            # end if

            sys.stdout.write('\b' * len(next_output) * 2)
            sys.stdout.flush()
        # end while
    # end spinner_task
# end Spinner

spinner = Spinner