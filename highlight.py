import curses
import time

class highlight:
    def __init__(self):
        curses.init_pair(2, curses.COLOR_BLUE, -1)
        curses.init_pair(3, curses.COLOR_RED, -1)
        curses.init_pair(4, curses.COLOR_GREEN, -1)
        curses.init_pair(5, curses.COLOR_YELLOW, -1)
        curses.init_pair(6, curses.COLOR_MAGENTA, -1)

    def check(self, l, count, keyword, line):
        if len(keyword) > 1:
            if count + len(keyword) > len(line):
                return False
            else: 
                chck = 0
                for i in range(len(keyword)):
                    if keyword[i] == line[count + i]:
                        chck += 1
                if chck == len(keyword):
                    return len(keyword)
        else:
            if l == keyword:
                return True
            else:
                return False
    
    def load_lang(self, filename):
        if filename.endswith(".py") == True:
            from .syntax_lang import pyth
            self.syntax_lang = pyth

    def syntax_highlight(self, row, line, stdscr):
        start = time.time()
        d = []
        count = 0
        keyword = ""
        color = 0
        while count < len(line):
            l = line[count]
            for key in self.syntax_lang.lang_pack:
                if str(key[0]) == l:
                    d.append(str(key))
            for i in d:
                ch = self.check(l, count, i, line)
                if ch == len(i) or ch == True:
                    color = self.syntax_lang.lang_pack[str(i)]
                    keyword = i
                    break
                else:
                    keyword = ""
                    color = False
            if color != False:
                if l == "\x22":
                    amogus = False
                    ct = 1
                    while ct < len(line[count:]):
                        if line[count + ct] == "\x22":
                            stdscr.addstr(row, count, line[count:count + ct + 1], curses.color_pair(6))
                            count += ct
                            amogus = True
                            break
                        ct += 1
                    if amogus == False:
                        stdscr.addstr(row, count, l)                        
                elif ch == True:
                    stdscr.addstr(row, count, l, curses.color_pair(int(color)))
                elif ch == len(i):
                    stdscr.addstr(row, count, line[count:count + len(keyword)], curses.color_pair(int(color)))
                    count += len(keyword) - 1
            else:
                stdscr.addstr(row, count, l)
            count += 1
        self.timer = time.time() - start
        
