import pygame
import soragl as SORA
import struct

from pygame import draw as pgdraw
from pygame import math as pgmath

from soragl import (
    animation,
    scene,
    physics,
    base_objects,
    mgl,
    smath,
    signal,
    statesystem,
)

from soragl.ui import ui

# -------------------------------------------------------------- #
# setup

WW = 1280
WINDOW_SIZE = [WW, int(WW / 16 * 9)]
WW = 1280 // 3
FB_SIZE = [WW, int(WW / 16 * 9)]

# mac version -- since no opengl

# ------------------------------ #
# setup

SORA.initialize(
    {
        "fps": 30,
        "window_size": [1280, 720],
        "window_flags": pygame.RESIZABLE
        | pygame.DOUBLEBUF
        | pygame.HWSURFACE
        | pygame.OPENGL
        if SORA.get_os() == SORA.OS_WINDOWS
        else 0,
        "window_bits": 32,
        "framebuffer_flags": pygame.SRCALPHA,
        "framebuffer_size": [1280 // 3, 720 // 3],
        "framebuffer_bits": 32,
        "debug": True,
    }
)

SORA.create_context()

# if moderngl stuff setup
if SORA.is_flag_active(pygame.OPENGL):
    mgl.ModernGL.create_context(
        options={
            "standalone": False,
            "gc_mode": "context_gc",
            "clear_color": [0.0, 0.0, 0.0, 1.0],
        }
    )

# -------------------------------------------------------------- #
# imports

from scripts import singleton

from scripts.entities import player, mage, particle_scripts
from scripts.entities import peasant

# from scripts.entities import peasant, test
from scripts.attacks import fireball, attacks, short_melee
from scripts.environment import grass  # , ambient, wind

from scripts.ui import hotbar

# -------------------------------------------------------------- #

sc = scene.Scene(config=scene.load_config(scene.Scene.DEFAULT_CONFIG))
sc._config["chunkpixw"] = 500
sc._config["chunkpixh"] = 500
sc._config["render_distance"] = 2

scw = sc.make_layer(sc.get_config(), 1, [
    base_objects.TileMapDebug(),
    base_objects.SpriteRendererAspect(),
    base_objects.Collision2DAspect(),
    # base_objects.Collision2DRendererAspectDebug(),
    # base_objects.Area2DAspect(),
    base_objects.Area2DRendererAspectDebug(),
    base_objects.ScriptAspect(),
    statesystem.StateHandlerAspect(),
    base_objects.CameraAspect(),
])

scui = sc.make_layer(sc.get_config(), 0, [
    ui.UIRendererAspect(),
    base_objects.ScriptAspect(),
], ui.UI)


# scw.get_chunk(0, 0)
BG_COL = (153, 220, 80)

# -------------------------------- #
# add to scw -- game world

# -- add entities
# particle handler test
ph = scw.add_entity(particle_scripts.GravityParticleHandler(color=(255, 0, 0), life=3))
ph.position += (100, 100)
ph["interval"] = 1 / 15

# === singletons
singleton.PLAYER = scw.add_entity(player.Player())
singleton.CAMERA = singleton.PLAYER.add_component(base_objects.Camera2D())

# player
singleton.PLAYER.position += (100, 100)
ph.add_collider(singleton.PLAYER.rect)
singleton.CAMERA.set_target(singleton.PLAYER)
singleton.CAMERA.active = True

# mage
_mage = scw.add_entity(mage.Mage())
_mage.position += (200, 200)
ph.add_collider(_mage.rect)

# peasant
_peasant = scw.add_entity(peasant.Peasant())
_peasant.position += (150, 100)
ph.add_collider(_peasant.rect)


# add grass sprites for chunks in range 1 --> 3
for x in range(-1, 2):
    for y in range(-1, 2):
        # get the chunk
        _chunk = scw.get_chunk(x, y)
        _g_asset = grass.GrassHandler("assets/sprites/grass.json", grass_count=100)
        _g_asset.position = _chunk.rect.topleft
        scw.add_entity(_g_asset)


# -------------------------------- #
# add to scui - ui layer

ui_hot = scui.add_entity(hotbar.Hotbar())
ui_hot.position += (200, 200)

ui_icon = scui.add_entity(hotbar.UIIcon())


# -------------------------------- #
# push scene
scene.SceneHandler.push_scene(sc)



# -------------------------------------------------------------- #
# game loop
SORA.start_engine_time()
while SORA.RUNNING:
    # SORA.FRAMEBUFFER.fill((255, 255, 255, 255))
    # SORA.FRAMEBUFFER.fill((0, 0, 0, 255))
    SORA.FRAMEBUFFER.fill(BG_COL)
    SORA.DEBUGBUFFER.fill((0, 0, 0, 0))
    # pygame update + render
    scene.SceneHandler.update()

    if SORA.is_key_clicked(pygame.K_d) and SORA.is_key_pressed(pygame.K_LSHIFT):
        SORA.DEBUG = not SORA.DEBUG

    # # render out frames from animation.Category.get_registries_for_all(player.ANIM_CAT)
    # for y, anim in enumerate(animation.Category.get_registries_for_all(player.ANIM_CAT).values()):
    #     for x, frame in enumerate(anim.parent.sprite_sheet.frames):
    #         SORA.FRAMEBUFFER.blit(frame.get_frame(), (x * 16, y * 16))

    # # render out frames from fireball.F_ANIM_CACHE
    # for i, frame in enumerate(fireball.F_ANIM_CACHE.sprite_sheet.frames):
    #     SORA.FRAMEBUFFER.blit(frame.get_frame(), (i * 16, 16 * 4))
    # scw.add_entity(short_melee.MeleeRange(singleton.PLAYER))

    # # render out frames from animation.Category.get_registries_for_all(short_melee.M_ANIM_CAT)
    # for y, anim in enumerate(animation.Category.get_registries_for_all(short_melee.M_ANIM_CAT).values()):
    #     for x, frame in enumerate(anim.parent.sprite_sheet.frames):
    #         SORA.FRAMEBUFFER.blit(frame.getc_frame(), (x * 16, y * 16))

    # update signals
    signal.handle_signals()
    # push frame
    SORA.push_framebuffer()
    # pygame.display.flip()
    # update events
    SORA.update_hardware()
    SORA.handle_pygame_events()
    # clock tick
    SORA.CLOCK.tick(SORA.FPS)
    SORA.update_time()

# ------------------------------- #

pygame.quit()
