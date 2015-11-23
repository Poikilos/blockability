
import pygame
from pygame import *
import sys
import os

sample_levels = None

def get_surface_from_lief_level(string_list):
    max_rows = -1
    max_cols = -1
    result_surface = None
    rows = 0
    for line in string_list:
        cols = 0
        for char in line:
            cols += 1
            if cols > max_cols:
                max_cols = cols
        rows += 1
        if rows > max_rows:
            max_rows = rows
    
    if (max_rows >= 1) and (max_cols >= 1):
        result_surface = Surface( (max_cols,max_rows),pygame.SRCALPHA, 32)
    result_surface.convert_alpha()
    platform_mapcolor = (255,255,0,255)
    exit_mapcolor = (255,0,0,255)
    nothing_color = (0,0,0,255)
    row_index = 0
    for line in string_list:
        col_index = 0
        for char in line:
            if char == " ":
                #black
                result_surface.set_at( (col_index,row_index), nothing_color )
            elif char == "P":
                #platform
                result_surface.set_at( (col_index,row_index), platform_mapcolor )
            elif char == "E":
                #exit to next level
                result_surface.set_at( (col_index,row_index), exit_mapcolor )
            else:
                result_surface.set_at( (col_index,row_index), nothing_color )
            col_index += 1
        row_index += 1
    
    return result_surface

def main():
    global sample_levels
    
    sample_levels = list()
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P                                          E",
        "P                         PPPPPP   PPPPP  PP",
        "P                 PPPP                     P",
        "P                                          P",
        "P    PPPPPPPP                              P",
        "P                                          P",
        "P                          PPPPPPP         P",
        "P                 PPPPPP                   P",
        "P                                          P",
        "P         PPPPPPP                          P",
        "P                                          P",
        "P                     PPPPPP               P",
        "P                                          P",
        "P   PPPPPPPPPPP                            P",
        "P                                          P",
        "P                 PPPPPPPPPPP              P",
        "P                                          P",
        "P        PPPP                              P",
        "P                                          P",
        "P                                          P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    sample_levels.append(level)
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "E                                          P",
        "PP                                         P",
        "P       PPP                         PPP    P",
        "P                                          P",
        "P                  PPPP                    P",
        "P                                          P",
        "P                                          P",
        "P                                  PPPP    P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P                        PPPPP             P",
        "P                                          P",
        "P                                          P",
        "P                  PPPP                    P",
        "P                                          P",
        "P                                          P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    sample_levels.append(level)
    level_index = 0
    for this_level in sample_levels:
        level_image = get_surface_from_lief_level(this_level)
        if level_image is not None:
            pygame.image.save(level_image, str(level_index)+".png")
        level_index += 1
    playing = True
    clock = pygame.time.Clock()
    while playing:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                playing = False
        if level_image is not None:
            screen.blit(level_image,(0,0))
        clock.tick(60)
        pygame.display.flip()


if __name__ == "__main__":
    main()
