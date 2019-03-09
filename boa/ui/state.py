class State:
    FILE_INFO = 'file-info'

    def __init__(self, scr):
        self.cy = 0
        self.voffset = 0
        self.height, self.width = scr.getmaxyx()
        self.viewer_offset_x = 0
        self.viewer_offset_y = 1
        self.viewer_height = self.height - 4
        self.viewer_width = self.width
        self.current_entry = None
        self.selected_entry = None

        self.overlay_id = None

    def update_selected(self):
        self.selected_entry = self.current_entry.sub_entries[self.cy]
