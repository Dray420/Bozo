# Default statusbar at the bottom
import curses
import platform


class status:
    def __init__(self):
        self.save_status = "Not saved"
        self.col = 0
        self.ln = 0
        curses.init_color(23, 255, 215, 0)
        curses.init_color(21, 46, 52, 64)
        curses.init_color(22, 0, 255, 0)
        curses.init_color(24, 76, 86, 106)
        curses.init_pair(7, 21, 22)
        curses.init_pair(8, 21, 23)
        curses.init_pair(9, 22, 24)

    def refresh(self, col, ln):
        self.col = col
        self.ln = ln
    
    def statusbar(self, filename, cu, stdscr, timer):
        for i in range(curses.COLS):
            stdscr.addstr(curses.LINES - 2, i, " ", curses.color_pair(1))
        left = "  ln " + str(cu.virtual_col) + ", ln " + str(cu.row) + "  "
        rightleft = "  " + str(filename) + "  "
        right = "  BOZO  "
        leftright = "  OS: " + str(platform.system()) + "  "
        stdscr.addstr(curses.LINES - 2, curses.COLS - len(left), left, curses.color_pair(7))
        stdscr.addstr(curses.LINES - 2, 0, right, curses.color_pair(7))
        stdscr.addstr(curses.LINES - 2, curses.COLS // 2, rightleft, curses.color_pair(7))
        stdscr.addstr(curses.LINES - 2, 0 + len(right), leftright, curses.color_pair(9))
        
