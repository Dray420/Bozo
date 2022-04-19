import curses
import argparse
import sys
import util.status
import util.highlight


class w:
    def __init__(self, ln, co, width, row=0, col=0, h_col=0):
        self.lines = ln - 1
        self.cols = co
        self.w_row = row
        self.w_col = col
        self.h_c = 0
        self.width = width
        self.h_w = self.width

    @property
    def bottom(self):
        return self.w_row + self.lines - 1

    def up(self, cu):
        if cu.row == self.w_row - 1 and self.w_row > 0:
            self.w_row -= 1

    def down(self, buffer, cu):
        if cu.row == self.bottom + 1 and self.bottom < len(buffer) - 1:
            self.w_row += 1
    
    def t(self, cu):
        return cu.row - self.w_row, cu.col - self.w_col

    def left(self, cu):
        if cu.col < 3 and self.h_c != 0:
            self.h_c -= 1
            self.h_w -= 1
            s = True
        else:
            s = False
        return s
        
    def right(self, cu, buffer):
        if cu.col > self.width - 4 and len(buffer[cu.row]) > cu.virtual_col:
            self.h_c += 1
            self.h_w += 1
            t = True
        else:
            t = False
        return t

class Buffer:
    def __init__(self, lines):
        self.lines = lines

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, index):
        return self.lines[index]

    @property
    def bottom(self):
        return len(self) - 1

    def undo(self, cu, window):
        f = open("temporary/log.txt")
        last_expression = f.readlines()[-1]
        if last_expression.startswith("REMOVE") == True:
            self.insert(cu, str(last_expression[6:]))
            for i in range(len(str(last_expression[6:]))):
                window.right(cu, self)
                cu.right(self, window)
            f.writelines(f.readlines()[:-1])

    def insert(self, cu, char):
        try:
            current = self.lines.pop(cu.row)
            new = current[:cu.virtual_col] + char + current[cu.virtual_col:]
            self.lines.insert(cu.row, new)
        except IndexError:
            new = char
            self.lines.insert(cu.row, new)
        
    def new_line(self, cu):
        try:
            current = self.lines.pop(cu.row)
            self.lines.insert(cu.row, current[:cu.virtual_col])
            self.lines.insert(cu.row + 1, current[cu.virtual_col:])
        except IndexError:
            self.lines.insert(cu.row + 1, "")

    def backspace(self, cu, buffer):
        if cu.col > 0:
            current = self.lines.pop(cu.row)
            n_ew = current[0:cu.virtual_col - 1] + current[cu.virtual_col:]
            self.lines.insert(cu.row, n_ew)
        elif cu.col == 0 and cu.row == 0:
            pass
        else:
            current = self.lines.pop(cu.row)
            cu.backspace_up(buffer)
            after = self.lines.pop(cu.row)
            new = after + current[:cu.virtual_col]
            self.lines.insert(cu.row, new)

class cursor:
    def __init__(self, window, row=0, col=0):
        self.row = row
        self.col = col
        self.virtual_col = self.col
        self.last_col = 0
        self.save_status = ""
        self.w = window

    def loadfile():
        try:
            args = argparse.ArgumentParser()
            args.add_argument("filename")
            argument = args.parse_args()
            f = open(argument.filename)
            buffer = Buffer(f.read().splitlines())
            f.close()
        except:
            args = argparse.ArgumentParser()
            args.add_argument("filename")
            argument = args.parse_args()
            f = open(argument.filename, "w")
            f.close()
            f = open(argument.filename)
            buffer = Buffer(f.read().splitlines())
            f.close()

        return buffer, argument
    
    def writefile(self, argument, buffer):
        f = open(argument.filename, "w")
        for i in buffer.lines:
            f.write(str(i))
            f.write("\n")

    def cc(self, buffer):
        if len(buffer[self.row]) > self.w.h_w and self.last_col > self.w.h_w:
            self.w.h_c += self.last_col - self.w.h_w
            self.w.h_w += self.last_col - self.w.h_w
            self.col = min(curses.LINES - 1, len(buffer[self.row]))
        elif len(buffer[self.row]) < self.w.h_c or self.last_col < self.w.h_c:
            if self.last_col < self.w.h_c:
                self.w.h_w -= self.w.h_c - self.last_col
                self.w.h_c -= self.w.h_c - self.last_col
                self.col = min(0, len(buffer[self.row]))
            elif len(buffer[self.row]) < self.w.h_c:
                self.w.h_w -= self.w.h_c - len(buffer[self.row])
                self.w.h_c -= self.w.h_c - len(buffer[self.row])
                self.col = min(0, len(buffer[self.row]))
        elif self.last_col > self.w.h_c and self.last_col < self.w.h_w:
            self.col = min(self.last_col - self.w.h_c, len(buffer[self.row]))
        self.virtual_col = min(self.last_col, len(buffer[self.row]))
        
    def up(self, buffer):
        if self.row > 0:
            self.row -= 1
            self.cc(buffer)
    def backspace_up(self, buffer):
        if self.row > 0:
            self.row -= 1
            self.col = max(self.col + 1, len(buffer[self.row]) + 1)
            self.virtual_col = max(self.virtual_col + 1, len(buffer[self.row]) + 1)
    def down(self, buffer):
        if self.row < len(buffer) - 1:
            self.row += 1
            self.cc(buffer)
    def newline_down(self, buffer, window):
        if self.row < len(buffer) - 1:
            if self.row > curses.LINES - 1:
                window.w_row += 1
            self.row += 1
            self.col = 0
            self.virtual_col = 0      

    def right(self, buffer, window):
        if self.col > window.width - 4:
            if self.virtual_col < len(buffer[self.row]):
                self.virtual_col += 1
                self.last_col = self.virtual_col
        else:
            if self.col < window.cols:
                if self.virtual_col < len(buffer[self.row]):
                    self.col += 1
                    self.virtual_col += 1
                    self.last_col = self.virtual_col

    def left(self, window):
        if window.h_c == 0:
            if self.virtual_col > 0 and self.col > 0:
                self.virtual_col -= 1
                self.col -= 1
                self.last_col = self.virtual_col
        elif window.h_c != 0:
            if self.col < 3:
                self.virtual_col -= 1
                self.last_col = self.virtual_col
            else:
                self.col -= 1
                self.virtual_col -= 1
                self.last_col = self.virtual_col

def main(stdscr):
    height, width = stdscr.getmaxyx()
    buffer, argument = cursor.loadfile()
    curses.use_default_colors()
    curses.init_color(20, 216, 222, 233)
    curses.init_pair(1, curses.COLOR_WHITE, 20)
    window  = w(curses.LINES - 1, curses.COLS - 1, width)
    cu = cursor(window)
    status = util.status.status()
    highlight = util.highlight.highlight()
    highlight.load_lang(argument.filename)
    key = ""
    h = True
    while True:
        stdscr.erase()
        status.refresh(cu.virtual_col, cu.row)
        for row, line in enumerate(buffer[window.w_row:window.w_row + window.lines]):
            if h == True:
                highlight.syntax_highlight(row, line[window.h_c:window.h_w], stdscr)
            elif h == False:
                stdscr.addstr(row, 0, line[window.h_c:window.h_w])
        status.statusbar(argument.filename, cu, stdscr, highlight.timer)
        stdscr.move(*window.t(cu))
        key = stdscr.getkey()
        if key == "\x18":
            sys.exit()
        elif key == "\x17":
            cu.writefile(argument, buffer)
        elif key == "KEY_UP":
            cu.up(buffer)
            window.up(cu)
        elif key == "KEY_DOWN":
            cu.down(buffer)
            window.down(buffer, cu)
        elif key == "KEY_RIGHT":
            window.right(cu, buffer)
            cu.right(buffer, window)
            window.down(buffer, cu)
        elif key == "KEY_LEFT":
            window.left(cu)
            cu.left(window)
            window.up(cu)
        elif key == "\n":
            buffer.new_line(cu)
            cu.newline_down(buffer, window)
        elif key == "KEY_BACKSPACE":
            window.left(cu)
            buffer.backspace(cu, buffer)
            cu.left(window)
        elif key == "\x08":
            if h == True:
                h = False
            elif h == False:
                h = True
        else:
            buffer.insert(cu, key)
            window.right(cu, buffer)
            cu.right(buffer, window)


curses.wrapper(main)


