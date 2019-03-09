from boa.files.path_entry import PathEntry


class Stats:
    headers = ['Modified', 'Size']
    formats = ['string', 'float-unit']
    widths = [12, 12]
    dimensions = [12, (12, 7, 3, 2)]
    values = [PathEntry.get_modified,
              (PathEntry.get_size, PathEntry.get_size_units)]
    allow_on_dirs = [True, False]

    def count():
        return len(Stats.headers)

    def format_header(index, entry):
        if not Stats.allow_on_dirs[index] and entry.is_dir:
            return ''
        format = Stats.formats[index]
        if format == 'float-unit':
            width, full, dec, un = Stats.dimensions[index]
            value_func, unit_func = Stats.values[index]
            value = value_func(entry)
            units = unit_func(entry)
            float_str = "{0:{2}.{3}f} {1:>{4}}".format(
                value, units, full, dec, un)
            return "{0:^{1}}".format(float_str, width)
        elif format == 'string':
            width = Stats.dimensions[index]
            value_func = Stats.values[index]
            value = value_func(entry)
            format_str = "{0:^" + str(width) + "}"
            return "{0:^{1}}".format(value, width)
