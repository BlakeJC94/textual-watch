"""Simple `watch` command emulation in Textual widget"""
import subprocess
from queue import Queue, Empty
from threading import Thread
from typing import Optional

from rich.panel import Panel
from textual.widget import Widget


class WatchShell(Widget):
    """Textual widget for monitoring output from a shell command via subprocessing."""

    def __init__(
        self,
        command: str,
        *args,
        interval: float = 2.0,
        title: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Constructor.

        Args:
            command: shell command to run and monitor.
            *args: Optional args to pass through to `textual.widget.Widget`.
            interval: Interval in seconds to monitor the command, same as `-n` for `watch`.
            title: Title for widget
            **kwargs: Optional kwargs to pass through to `textual.widget.Widget`.
        """
        super().__init__(*args, **kwargs)

        self.command = command
        self.title = title if title is not None else command
        self.interval = interval

        self.queue = Queue(maxsize=1)
        self.worker = Thread(
            target=self._process,
            daemon=True,
        )

        self.output_buffer = None
        self.loading_message = "Loading"
        self.ticker, self.ticker_max = 0, 3

    def _process(self) -> None:
        """Process to run command on separate thread, put output (or errors) on a simple queue to
        pass output to Textual widget."""
        while True:
            try:
                result = subprocess.run(
                    self.command.split(), check=False, capture_output=True, text=True
                )
                output = result.stdout
            except subprocess.CalledProcessError as err:
                output = (
                    f"ERROR processing command `{self.command}` "
                    f"(returncode={err.returncode})"
                    + "\n" * 2
                    + err.stderr.decode("utf-8")
                )
            self.queue.put(output)

    def on_mount(self) -> None:
        """Set refresh rate based on `self.interval` and start a thread to monitor `self.command`
        output."""
        self.set_interval(self.interval, self.refresh)
        self.worker.start()

    def _get_loading_message(self) -> str:
        """Get nice loading message."""
        message = (
            self.loading_message
            + " "
            + "." * self.ticker
            + " " * (self.ticker_max - self.ticker)
        )
        self.ticker = (self.ticker + 1) % (self.ticker_max + 1)
        return message

    def render(self) -> Panel:
        """Main rendering method that obtains output from `self.worker` via a queue. Displays a
        loading message initially which waiting for the first execution, refreshes and updates
        widget output (or execution errors) at specified interval."""
        output = None

        try:
            output = self.queue.get(block=False)
            if output is not None:
                self.output_buffer = output
            self.queue.task_done()
        except Empty:
            if self.output_buffer is not None:
                output = self.output_buffer
            else:
                output = self._get_loading_message()

        return Panel(output, title=self.title)
