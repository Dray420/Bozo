#!/usr/bin/env python
import curses

class move:
    def move(self, last_cursor_location, cu, stdscr, buffer, window):
        cu.col = 0
        cu.virtual_col = 0
        cu.row = curses.LINES - 1
        stdscr.erase()
        curses.echo()
        line = stdscr.getstr()
        if int(line) > len(buffer) - 1 or int(line) < 0:
            cu.row, cu.col, cu.virtual_col = last_cursor_location[0], last_cursor_location[1], last_cursor_location[2]
        else:
            cu.row = int(line)
            window.w_row = int(line)
        curses.noecho()
        
        
