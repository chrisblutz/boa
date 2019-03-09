from boa.ui.file_info_overlay import FileInfoOverlay


class Overlays:
    _overlays = {}

    def register_overlay(id, func):
        Overlays._overlays[id] = func

    def render_overlay(id, screen, state, path_entry):
        Overlays._overlays.get(id)(screen, state, path_entry)


Overlays.register_overlay(FileInfoOverlay.ID, FileInfoOverlay.render_file_info)
