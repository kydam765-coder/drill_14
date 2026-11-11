from pico2d import *


CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        image = load_image('bird_animation.png')
        running = True
        while running:
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
                elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                    running = False
            clear_canvas()
            image.draw(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
            update_canvas()
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
