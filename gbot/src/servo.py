#!/usr/bin/env python

import sys
import time
import pigpio

pi = pigpio.pi()

if not pi.connected:
   exit()

class ServoControl:
    def __init__(self, pin, pi, min_pos, max_pos):
        self.pin = pin
        self.pi = pi
        self.min_pos = min_pos
        self.max_pos = max_pos
        self.set_position(1500)
        self.stop()

    def set_position(self, new_position):
        self.pi.set_servo_pulsewidth(self.pin, new_position)
        self.position = new_position
        time.sleep(0.01)

    def move_to_position(self, new_position):
        if new_position > self.max_pos:
            new_position = self.max_pos
        if new_position < self.min_pos:
            new_position = self.min_pos

        if new_position == self.position:
            # Nothing to do
            return

        step = 5 if new_position >= self.position else -5

        for pos in range(self.position, new_position, step):
            self.set_position(pos)

        self.stop()

    def get_current_position(self):
        return self.position

    def stop(self):
        self.pi.set_servo_pulsewidth(self.pin, 0)

    def close(self):
        self.move_to_position(1500)

class TiltControl(ServoControl):
    def __init__(self):
        ServoControl.__init__(self, 13, pi, 1450, 1700)

class PanControl(ServoControl):
    def __init__(self):
        ServoControl.__init__(self, 12, pi, 1350, 1650)

if __name__ == '__main__':

    tilt = TiltControl()
    try:
        tilt.move_to_position(800)
        time.sleep(1)
        tilt.move_to_position(2400)
        time.sleep(1)
        tilt.move_to_position(1500)
        time.sleep(1)

        pan = PanControl()
        pan.move_to_position(1000)
        time.sleep(1)
        pan.move_to_position(2000)
        time.sleep(1)
    finally:
        tilt.close()
        pan.close()
        pi.stop()


