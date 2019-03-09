import curses

from boa.ui.state import State


class Inputs:
    def handle(key, state):
        if state.overlay_id == None:
            if key == curses.KEY_UP:
                Inputs.move_up(state)
            elif key == curses.KEY_DOWN:
                Inputs.move_down(state)
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                if state.selected_entry.is_dir and not state.selected_entry.perm_denied:
                    if state.selected_entry.expand():
                        state.current_entry.collapse()
                        state.current_entry = state.selected_entry
                        state.cy = 0
                        state.voffset = 0
                        state.update_selected()
            elif key == ord('i') & 0x1f:
                state.overlay_id = State.FILE_INFO
        elif state.overlay_id == State.FILE_INFO:
            if key == 27:
                state.overlay_id = None

    def move_up(state):
        if state.cy > 0:
            state.cy -= 1
        if state.cy < state.voffset:
            state.voffset -= 1
        state.update_selected()

    def move_down(state):
        if state.cy < len(state.current_entry.sub_entries) - 1:
            state.cy += 1
        if state.cy > state.voffset + state.viewer_height - 1:
            state.voffset += 1
        state.update_selected()
