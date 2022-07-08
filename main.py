import pygame
from engine import clock, user_input, handler, animation

from engine.window import Window
from engine.filehandler import *


WINDOW_CAPTION = "RPG Game"
WINDOW_SIZE = [1280, 720]
FB_SIZE = [360, 202]

FPS = 30

Window.create_window(WINDOW_CAPTION, WINDOW_SIZE[0], WINDOW_SIZE[1], pygame.RESIZABLE, 16)
# window.set_icon()
fb = pygame.Surface(FB_SIZE, 0, 32).convert_alpha()

# --------- testing ----------- #

animation.load_and_parse_aseprite_animation("assets/sprites/player.json")
image = animation.Category.get_category("player").get_animation("idle").get_registry()


# ----------------------------- #
clock.start()
while Window.running:
    fb.fill((255, 255, 255))
    image.update()
    fb.blit(image.get_frame(), (100, 100))

    # rescale framebuffer to window
    Window.instance.blit(pygame.transform.scale(fb, (Window.WIDTH, Window.HEIGHT)), (0,0))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            Window.running = False
        elif e.type == pygame.KEYDOWN:
            # keyboard press
            user_input.key_press(e)
        elif e.type == pygame.KEYUP:
            # keyboard release
            user_input.key_release(e)
        elif e.type == pygame.MOUSEMOTION:
            # mouse movement
            user_input.mouse_move_update(e)
        elif e.type == pygame.MOUSEBUTTONDOWN:
            # mouse press
            user_input.mouse_button_press(e)
        elif e.type == pygame.MOUSEBUTTONUP:
            # mouse release
            user_input.mouse_button_release(e)
        elif e.type == pygame.WINDOWRESIZED:
            # window resized
            Window.handle_resize(e)
            fbsize = fb.get_size()
            user_input.update_ratio(Window.WIDTH, Window.HEIGHT, fbsize[0], fbsize[1])
    pygame.display.flip()
    clock.update()


pygame.quit()

