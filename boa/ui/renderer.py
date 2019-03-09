import curses
import pwd

from boa.ui.overlays import Overlays
from boa.ui.state import State
from boa.ui.stats import Stats


class Renderer:
    def __init__(self, scr):
        self.screen = scr
        self.state = State(scr)

    def render(self):
        self.render_line_with_attrs(
            0, 0, self.state.width, curses.A_REVERSE | curses.A_BOLD)
        version_str = 'Boa v0.1.0'
        self.screen.addstr(0, self.state.width - len(version_str),
                           version_str, curses.A_REVERSE | curses.A_BOLD)

        if self.state.overlay_id == None:
            self.screen.addstr(self.state.viewer_offset_y, self.state.viewer_offset_x,
                               self.state.current_entry.full_name, curses.A_BOLD)

            self.render_stat_headers(1)

            if self.state.voffset > 0:
                self.screen.addstr(self.state.viewer_offset_y + 1,
                                   self.state.viewer_offset_x, '…')
            if self.state.voffset + self.state.viewer_height < len(self.state.current_entry.sub_entries):
                self.screen.addstr(
                    self.state.viewer_offset_y + self.state.viewer_height, self.state.viewer_offset_x, '…')

            for i in range(0, self.state.viewer_height):
                index = i + self.state.voffset
                if index < len(self.state.current_entry.sub_entries):
                    self.render_entry(
                        self.state.current_entry.sub_entries[index], self.state.viewer_offset_x + 2, self.state.viewer_offset_y + i + 1)

            self.render_line_with_attrs(
                0, self.state.height - 2, self.state.width, curses.A_REVERSE | curses.A_BOLD)
            self.screen.addstr(
                self.state.height - 2, 0, self.state.selected_entry.full_name, curses.A_REVERSE | curses.A_BOLD)
            keys = 'View Info <CTRL+I>'
            self.screen.addstr(self.state.height - 2, self.state.width
                               - len(keys), keys, curses.A_REVERSE | curses.A_BOLD)

        else:
            Overlays.render_overlay(
                self.state.overlay_id, self.screen, self.state, self.state.selected_entry)

    def render_entry(self, entry, x, y):
        attr = curses.A_REVERSE if y == (
            self.state.cy - self.state.voffset + self.state.viewer_offset_y + 1) else curses.A_NORMAL
        self.render_line_with_attrs(x, y, self.state.viewer_width - x, attr)
        self.screen.addstr(y, x, entry.name, attr)
        if not entry.name == '..':
            self.render_stats(entry, y, attr)

    def render_stat_headers(self, y):
        right_pad = 0
        for i in range(Stats.count(), 0, -1):
            index = i - 1
            width = Stats.widths[index]
            header = "{0:^{1}}".format(Stats.headers[index], width)
            right_pad += width
            self.screen.addstr(y, (self.state.viewer_offset_x + self.state.viewer_width)
                               - right_pad, header, curses.A_REVERSE | curses.A_BOLD)

    def render_stats(self, entry, y, attr):
        right_pad = 0
        for i in range(Stats.count(), 0, -1):
            index = i - 1
            width = Stats.widths[index]
            str = Stats.format_header(index, entry)
            right_pad += width
            self.screen.addstr(
                y, (self.state.viewer_offset_x + self.state.viewer_width) - right_pad, str, attr)

    def render_line_with_attrs(self, x, y, width, attrs):
        self.screen.addstr(y, x, ' ' * width, attrs)
