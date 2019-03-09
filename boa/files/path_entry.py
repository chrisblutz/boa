import bisect
import datetime
import os
import re
import shlex
import subprocess
from pathlib import Path

from boa.files.registry import Registry


class PathEntry:
    storage_units = ['B', 'KB', 'MB', 'GB', 'TB', 'PT', 'EB', 'ZB', 'YB']

    def __init__(self, path):
        self.path = path
        self.full_name = path.as_posix()
        self.name = path.name
        self.is_dir = path.is_dir()
        self.sub_entries = []

        self.stat = path.stat()
        self.size_bytes = -1
        self.size = -1
        self.size_unit = None
        self.datetime_modified = datetime.datetime.fromtimestamp(
            self.stat.st_mtime).strftime('%x %X')
        self.modified = str(datetime.date.fromtimestamp(self.stat.st_mtime))

        self.mountpoint = path.is_mount()
        self.mounted = None
        if self.mountpoint:
            self.mounted = self.get_mounted_device(self.full_name)

        self.type = None
        if not self.is_dir:
            ext = path.suffixes
            if len(ext) > 0:
                type = ext[len(ext) - 1]
                self.type = Registry.TYPES.get(type)

        self.perm_denied = False

        if self.is_dir:
            self.name = "{}/".format(self.name)

        if not self.is_dir:
            self.size_bytes = self.stat.st_size
            self.size, self.size_unit = PathEntry.format_storage_units(
                self.size_bytes)

    def get_mounted_device(self, name):
        out = subprocess.Popen(shlex.split("df {}".format(
            name)), stdout=subprocess.PIPE).communicate()
        m = re.search(r'(/[^\s]+)\s', str(out))
        if m:
            return m.group(1)
        else:
            return None

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    def __gt__(self, other):
        return self.name.lower() > other.name.lower()

    def expand_outer(self):
        if self.expand():
            for entry in self.sub_entries:
                if entry.is_dir and not os.access(entry.path, os.R_OK):
                    entry.perm_denied = True

    def expand(self):
        if not self.is_dir:
            return False
        try:
            dir_list = []
            file_list = []
            files = self.path.iterdir()
            for entry in files:
                if entry.is_dir():
                    dir = PathEntry(entry)
                    bisect.insort_left(dir_list, dir)
                elif entry.is_file():
                    file = PathEntry(entry)
                    bisect.insort_left(file_list, file)

            if self.path.parent != self.path:
                previous = PathEntry(self.path.parent)
                previous.name = '..'
                dir_list.insert(0, previous)

            self.sub_entries.extend(dir_list)
            self.sub_entries.extend(file_list)
        except PermissionError:
            self.perm_denied = True
            return False
        return True

    def collapse(self):
        self.sub_entries = []

    def get_size(entry):
        return entry.size

    def get_size_units(entry):
        return entry.size_unit

    def get_modified(entry):
        return entry.modified

    def get_type(entry):
        type = entry.type
        if not type:
            return ''
        else:
            return type

    def format_storage_units(value):
        unit_index = 0
        while value >= 1000:
            value /= 1000
            unit_index += 1
        return value, PathEntry.storage_units[unit_index]
