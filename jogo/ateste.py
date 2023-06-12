import curses
import time

scre = curses.initscr()
curses.start_color()

curses.cbreak()
curses.curs_set(0)
scre.addch(1, 1, ord(chr(0x1F0BB)))
scre.refresh()
time.sleep(10)
curses.nocbreak()
curses.endwin()   
print((chr(0x1F0BB)))