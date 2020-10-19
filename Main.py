import pygame as pg
import numpy as np
from math import*
from Maps import Maps
from Raycasting import Raycasting

pg.init()
screen_Size = (500,400)
screen = pg.display.set_mode(screen_Size)

pg.display.set_caption("FranEngine2")

player_Pos = [2,2]
move_Vel = 10
rot_Speed = 2
fov = 60

ray_Step = fov/screen_Size[0]

direction = [-1.0,0.0]
plane = [0.0,0.66]

run = True

startFrameTime=0
Map = Maps.load(1)

while run:
    startFrameTime = pg.time.get_ticks()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    keys = pg.key.get_pressed()

     # To rotate the view we have to rotate the camera plane
    if keys[pg.K_a]:
        old_direction = direction[0]
        direction[0] = direction[0] * cos(rot_Speed) - direction[1] * sin((rot_Speed))
        direction[1] = old_direction * sin(rot_Speed) + direction[1] * cos((rot_Speed)) 
        old_Plane = plane[0]
        plane[0]= plane[0] * cos(rot_Speed) - plane[1] * sin(rot_Speed)
        plane[1]= old_Plane * sin(rot_Speed) + plane[1] * cos(rot_Speed)
    if keys[pg.K_d]:
        old_direction = direction[0]
        direction[0] = direction[0] * cos(-rot_Speed) - direction[1] * sin(-rot_Speed)
        direction[1] = old_direction * sin(-rot_Speed) + direction[1] * cos(-rot_Speed) 
        old_Plane = plane[0]
        plane[0]= plane[0] * cos(-rot_Speed) - plane[1] * sin(-rot_Speed)
        plane[1]= old_Plane * sin(-rot_Speed) + plane[1] * cos(-rot_Speed)

    # Moving to the sides in dev

    if keys[pg.K_LEFT]:
            player_Pos[0] += move_Vel * (direction[0] * cos(radians(90)) - direction[1] * sin(radians(90)))
            player_Pos[1] += move_Vel * (direction[0] * sin(radians(90)) + direction[1] * cos(radians(90)))
    if keys[pg.K_RIGHT]:
            player_Pos[0] -= move_Vel * (direction[0] * cos(radians(90)) - direction[1] * sin(radians(90)))
            player_Pos[1] -= move_Vel * (direction[0] * sin(radians(90)) + direction[1] * cos(radians(90)))


    # And here we have some movement(conventional)
    if keys[pg.K_UP]:
        if Map[int(player_Pos[0] + direction[0] * move_Vel)][int(player_Pos[1])] == 0:
            player_Pos[0] += direction[0] * move_Vel
        if Map[int(player_Pos[0])][int(player_Pos[1] + direction[1]* move_Vel)] == 0:
            player_Pos[1] += direction[1] * move_Vel
    if keys[pg.K_DOWN]: 
        if Map[int(player_Pos[0] - direction[0] * move_Vel)][int(player_Pos[1])] == 0:
            player_Pos[0] -= direction[0] * move_Vel
        if Map[int(player_Pos[0])][int(player_Pos[1] - direction[1] * move_Vel)] == 0:
            player_Pos[1] -= direction[1] * move_Vel
    
    # Drawing celling and floor
    screen.fill((145,145,145)) #floor
    pg.draw.rect(screen,(60,255,220),(0,0,screen_Size[0],screen_Size[1]//2)) #ceilling  

    Raycasting.casting3D(screen,screen_Size,player_Pos,direction,plane,fov,Map,ray_Step)

    pg.display.update() 

    frame_time = (pg.time.get_ticks() - startFrameTime)/ 1000

    move_Vel = frame_time * 1
    rot_Speed = frame_time * 3
    #fps counter
    fpscounter = str(round(1000/(pg.time.get_ticks()-startFrameTime)))
    
