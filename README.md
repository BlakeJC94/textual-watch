# Textual Watch
---
Widget for Textual Framework that emulates the `watch` shell command

This is an offshoot from a side-project where I needed to build a quick TUI using the
[Textual](https://github.com/Textualize/textual) library to pipe output from several shell commands
into a few widgets in the terminal.

Suggestions and feedback is welcome here, feel free to open a PR or raise an issue for further
discussion.

## Installation
Clone this repo and install it locally with `pip`:
```bash
$ git clone https://github.com/BlakeJC94/textual-watch
$ cd textual_watch
$ pip install .
```

## Quickstart

To write a simple app to monitor disk usage, we can write a simple disk space monitor with the
following in a simple python script:

```python
# spaced.py
from textual.app import App
from textual.widgets import Placeholder

from textual_watch import WatchShell


class Demo(App):
    async def on_mount(self) -> None:
        widget = WatchShell(
            "df -h",
            interval=3.0,
            title="current disk space",
        )
        await self.view.dock(widget, edge="left", size=100)

    async def on_load(self, event):
        await self.bind("q", "quit")


Demo.run()
```

Run the script `$ python3 spaced.py` to see the output. Press `q` to close the TUI (since the
command is executed asynchronously on another thread, there's no delay in registering key presses).
