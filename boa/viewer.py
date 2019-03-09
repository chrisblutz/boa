import curses
import os
import signal
import sys
from curses import wrapper
from pathlib import Path

from boa.control.inputs import Inputs
from boa.files.path_entry import PathEntry
from boa.files.registry import Registry
from boa.ui.renderer import Renderer


def main(scr):
    curses.curs_set(0)

    path = None

    if len(sys.argv) == 1:
        path = Path.cwd()
    elif len(sys.argv) == 2:
        path = Path(os.path.abspath(sys.argv[1]))
    else:
        exit('Error: boa requires a single path as an argument.')

    base_entry = PathEntry(path)
    exp = base_entry.expand_outer()

    renderer = Renderer(scr)
    renderer.state.current_entry = base_entry
    renderer.state.update_selected()

    key = None
    while key != (ord('q') & 0x1f):
        scr.clear()
        renderer.render()
        scr.refresh()
        key = scr.getch()
        Inputs.handle(key, renderer.state)


def setup():
    signal.signal(signal.SIGINT, lambda a, b: sys.exit(0))
    os.environ.setdefault('ESCDELAY', '25')

    Registry.load()
    wrapper(main)
