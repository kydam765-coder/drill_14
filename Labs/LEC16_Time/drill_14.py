import time

from pico2d import *


CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
FRAME_COLUMNS = 5
FRAME_ROWS = 3
FRAME_COUNT = 14
ANIMATION_FPS = 12.0
BIRD_WIDTH = 150
BIRD_HEIGHT = 138


class Bird:
    def __init__(self, image):
        self.image = image
        self.frame = 0

    def update(self, frame_time):
        self.frame = (self.frame + ANIMATION_FPS * frame_time) % FRAME_COUNT

    def draw(self, x, y):
        column = int(self.frame) % FRAME_COLUMNS
        row = int(self.frame) // FRAME_COLUMNS
        left = round(column * self.image.w / FRAME_COLUMNS)
        right = round((column + 1) * self.image.w / FRAME_COLUMNS)
        top = round(row * self.image.h / FRAME_ROWS)
        bottom = round((row + 1) * self.image.h / FRAME_ROWS)
        self.image.clip_draw(
            left,
            self.image.h - bottom,
            right - left,
            bottom - top,
            x,
            y,
            BIRD_WIDTH,
            BIRD_HEIGHT,
        )


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        image = load_image('bird_animation.png')
        bird = Bird(image)
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
            bird.update(frame_time)
            clear_canvas()
            bird.draw(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
            update_canvas()
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
