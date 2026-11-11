import time

from pico2d import *

import game_framework
import game_world
from boy import Boy
from grass import Grass


CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 600
FRAME_COLUMNS = 5
FRAME_ROWS = 3
FRAME_COUNT = 14
ANIMATION_FPS = 12.0
FLIGHT_SPEED_PPS = 180.0
BIRD_WIDTH = 150
BIRD_HEIGHT = 138
BIRD_OFFSETS = ((0, 0), (105, 45), (210, -15), (315, 25))


class Bird:
    def __init__(self, image, frame=0):
        self.image = image
        self.frame = frame % FRAME_COUNT

    def update(self, frame_time):
        self.frame = (self.frame + ANIMATION_FPS * frame_time) % FRAME_COUNT

    def draw(self, x, y, direction):
        column = int(self.frame) % FRAME_COLUMNS
        row = int(self.frame) // FRAME_COLUMNS

        left = round(column * self.image.w / FRAME_COLUMNS)
        right = round((column + 1) * self.image.w / FRAME_COLUMNS)
        top = round(row * self.image.h / FRAME_ROWS)
        bottom = round((row + 1) * self.image.h / FRAME_ROWS)

        self.image.clip_composite_draw(
            left,
            self.image.h - bottom,
            right - left,
            bottom - top,
            0,
            '' if direction > 0 else 'h',
            x,
            y,
            BIRD_WIDTH,
            BIRD_HEIGHT,
        )


class BirdFlock:
    def __init__(self, image, canvas_width):
        self.birds = [Bird(image, index * 3) for index in range(len(BIRD_OFFSETS))]
        self.offsets = BIRD_OFFSETS
        self.x = 80.0
        self.y = 300.0
        self.direction = 1
        self.speed_pps = FLIGHT_SPEED_PPS
        self.width = max(offset_x for offset_x, _ in self.offsets) + BIRD_WIDTH
        self.left_bound = 0.0
        self.right_bound = canvas_width - self.width

    def update(self, frame_time):
        distance = self.speed_pps * frame_time
        travel_range = self.right_bound - self.left_bound
        phase = (
            self.x - self.left_bound
            if self.direction > 0
            else 2 * travel_range - (self.x - self.left_bound)
        )
        phase = (phase + distance) % (2 * travel_range)

        if phase < travel_range:
            self.x = self.left_bound + phase
            self.direction = 1
        else:
            self.x = self.right_bound - (phase - travel_range)
            self.direction = -1

        for bird in self.birds:
            bird.update(frame_time)

    def draw(self):
        for bird, (offset_x, offset_y) in zip(self.birds, self.offsets):
            bird.draw(
                self.x + offset_x + BIRD_WIDTH / 2,
                self.y + offset_y,
                self.direction,
            )


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        flock_image = load_image('bird_animation.png')
        boy = Boy()
        grass = Grass()
        flock = BirdFlock(flock_image, CANVAS_WIDTH)
        flock.x = boy.x - flock.width / 2
        flock.y = boy.y + 190
        game_world.add_oject(grass, 0)
        game_world.add_oject(boy)

        previous_time = time.perf_counter()
        running = True

        while running:
            current_time = time.perf_counter()
            frame_time = current_time - previous_time
            previous_time = current_time

            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
                elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                    running = False
                else:
                    boy.handle_event(event)

            if not running:
                break

            game_framework.frame_time = frame_time
            game_world.update()
            flock.update(frame_time)
            clear_canvas()
            game_world.render()
            flock.draw()
            update_canvas()
    finally:
        game_world.clear()
        close_canvas()


if __name__ == '__main__':
    main()
