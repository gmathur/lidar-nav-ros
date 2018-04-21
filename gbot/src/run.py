#!/usr/bin/env python
import curses
from robot_pilot import RobotPilot

def main(win):
    # Open driver
    driver = RobotPilot()
    driver.open()
    driver.forward()

    try:
        win.nodelay(True)
        key=""
        win.clear()                
        win.addstr("Drive using W A S D - Q to quit")
        while True:          
            try:                 
               key = win.getkey()
               key = key.upper()
               if key == 'Q':
                  break
            except Exception as e:
               # No input   
               pass  
    finally:
        driver.close()

curses.wrapper(main)

