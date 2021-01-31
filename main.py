import random
import time
"""
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 64, auto_write=False)
"""

decay = 10   # After it switches off, how fast should cells light fade (values per 0.1 seconds)
density = 0.3  # Initial density of cells when generating new world (0.0 - 1.0)
conway_speed = 1  # number of seconds for each generation

class GameOfLife:
    state = None
    past_state_string = None
    density = None

    def __init__(self, density):
        self.state = {}
        self.past_state_string = []
        self.density = density
        self.randomise()

    def randomise(self):
        self.past_state_string = []
        for x in range(0, 8):
            self.state[x] = {}
            for y in range(0, 8):
                if random.random() < self.density:
                    self.state[x][y] = True
                else:
                    self.state[x][y] = False

    def get_repeat_count(self):
        return self.past_state_string.count(self.get_state_string())

    def get_state(self):
        return self.state

    def get_state_at(self, x, y):
        while x < 0:
            x = x + 8
        while x > 7:
            x = x - 8
        while y < 0:
            y = y + 8
        while y > 7:
            y = y - 8
        return self.state[x][y]

    def get_state_string(self):
        hash = ""
        for x in range(0, 8):
            for y in range(0, 8):
                if self.get_state_at(x, y):
                    hash = hash + "T"
                else:
                    hash = hash + "F"
        return hash

    def iterate(self):
        next_state = {}
        for x in range(0, 8):
            next_state[x] = {}
            for y in range(0, 8):
                neighbours = 0
                if self.get_state_at(x - 1, y - 1):
                    neighbours += 1
                if self.get_state_at(x - 1, y):
                    neighbours += 1
                if self.get_state_at(x - 1, y + 1):
                    neighbours += 1
                if self.get_state_at(x, y - 1):
                    neighbours += 1
                if self.get_state_at(x, y + 1):
                    neighbours += 1
                if self.get_state_at(x + 1, y - 1):
                    neighbours += 1
                if self.get_state_at(x + 1, y):
                    neighbours += 1
                if self.get_state_at(x + 1, y + 1):
                    neighbours += 1
                if self.get_state_at(x, y):
                    if neighbours < 2:
                        next_state[x][y] = False
                    elif neighbours == 2 or neighbours == 3:
                        next_state[x][y] = True
                    else:
                        next_state[x][y] = False
                else:
                    if neighbours == 3:
                        next_state[x][y] = True
                    else:
                        next_state[x][y] = False
        self.state = next_state
        self.past_state_string.append(self.get_state_string())


reds = {}
greens = {}
blues = {}
for x in range(0, 8):
    reds[x] = {}
    greens[x] = {}
    blues[x] = {}
    for y in range(0, 8):
        reds[x][y] = 0
        greens[x][y] = 0
        blues[x][y] = 0

red = GameOfLife(density=density)
green = GameOfLife(density=density)
blue = GameOfLife(density=density)
tick = 0

while True:
    if tick % (conway_speed * 10) == 0:
        red.iterate()
        green.iterate()
        blue.iterate()

        print(red.get_repeat_count(), green.get_repeat_count(), blue.get_repeat_count())
        if red.get_repeat_count() > 10:
            red.randomise()
        if green.get_repeat_count() > 10:
            green.randomise()
        if blue.get_repeat_count() > 10:
            blue.randomise()

        print("           -------            ")
        for y in range(0, 8):
            for x in range(0, 8):
                if red.get_state_at(x, y):
                    print('\x1b[0;30;41m \x1b[0m', end="")
                else:
                    print(" ", end="")
            print("     ", end='')
            for x in range(0, 8):
                if green.get_state_at(x, y):
                    print('\x1b[0;30;42m \x1b[0m', end="")
                else:
                    print(" ", end="")
            print("     ", end='')
            for x in range(0, 8):
                if blue.get_state_at(x, y):
                    print('\x1b[0;30;44m \x1b[0m', end="")
                else:
                    print(" ", end="")

            print("")

    for y in range(0, 8):
        for x in range(0, 8):
            if red.get_state_at(x, y):
                reds[x][y] = 255
            else:
                reds[x][y] = min(200, max(reds[x][y] - decay, 0))

            if green.get_state_at(x, y):
                greens[x][y] = 255
            else:
                greens[x][y] = min(200, max(greens[x][y] - decay, 0))

            if blue.get_state_at(x, y):
                blues[x][y] = 255
            else:
                blues[x][y] = min(200, max(blues[x][y] - decay, 0))

    """
    i = 0
    for x in range(0, 7):
        for y in range(0, 7):
            pixels[i] = (reds[x][y], greens[x][y], blues[x][y])
            i = i + 1
    pixels.show()
    """

    tick = tick + 1
    time.sleep(0.1)
