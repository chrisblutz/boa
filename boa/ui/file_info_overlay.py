import curses
import pwd


class FileInfoOverlay:
    ID = 'file-info'

    def render_file_info(screen, state, path_entry):
        y = 1
        screen.addstr(y, 0, ' ' * state.width,
                      curses.A_REVERSE | curses.A_BOLD)
        header = 'File Information'
        screen.addstr(y, (state.width // 2) - (len(header) // 2),
                      header, curses.A_REVERSE | curses.A_BOLD)

        info_map = FileInfoOverlay.get_info_map(path_entry)

        length = len(max(info_map.keys(), key=len)) + 1
        for key, value in info_map.items():
            y += 1
            key_str = "{0:>{1}} ".format(key, length)
            screen.addstr(y, 0, key_str, curses.A_REVERSE)
            screen.addstr(y, length + 2, value)

        for i in range(y + 1, state.height - 2):
            screen.addstr(i, 0, ' ' * (length + 1), curses.A_REVERSE)

        screen.addstr(state.height - 2, 0, ' ' * state.width,
                      curses.A_REVERSE | curses.A_BOLD)
        keys = 'Go Back <ESC>'
        screen.addstr(state.height - 2, state.width - len(keys),
                      keys, curses.A_REVERSE | curses.A_BOLD)

    def get_info_map(entry):
        info_map = {}
        info_map['Name'] = entry.path.name
        info_map['Path'] = entry.full_name
        size = ''
        if entry.is_dir:
            size = '-'
        else:
            size = "{0:.2f} {1}".format(entry.size, entry.size_unit)
            if entry.size_unit != 'B' or entry.size != entry.size_bytes:
                size += " ({0} bytes)".format(entry.size_bytes)
        info_map['Size'] = size
        info_map['Last Modified'] = entry.datetime_modified
        info_map['Owner'] = pwd.getpwuid(entry.stat.st_uid)[0]
        mount = ''
        if not entry.is_dir:
            mount = '-'
        elif entry.mountpoint:
            mount = "Yes ({})".format(entry.mounted)
        else:
            mount = 'No'
        info_map['Mountpoint?'] = mount
        return info_map
