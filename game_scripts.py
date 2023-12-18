

from constants import DISP_H, DISP_W
from game_structs import Camera


def update_camera(camera: Camera, focus_location: tuple):
    if not camera.always_centered:
        camera.x = focus_location.x - DISP_W / 2
        camera.y = focus_location.y - DISP_H * 3 / 4
    else:
        limit_x = int(camera.offset * DISP_W)

        if focus_location.x < camera.x + limit_x:
            camera.x -= (camera.x + limit_x) - focus_location.x 
        elif focus_location.x > (camera.x + DISP_W) - limit_x:
            camera.x += focus_location.x - ((camera.x + DISP_W) - limit_x)

        limit_y = int(focus_location.offset * DISP_H)
        if focus_location.y < camera.y + limit_y:
            camera.y -= (camera.y + limit_y) - focus_location.y 
        elif focus_location.y > (camera.y + DISP_H) - limit_y:
            camera.y += focus_location.y - ((camera.y + DISP_H) - limit_y)
