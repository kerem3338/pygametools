"""
Zu 2.5D Tool Kit
    By Zoda

<<--------------------------------------------------->>
Zu 2.5D Tool Kit, making 2.5D games with pygame easy.
<<--------------------------------------------------->>
"""
import pygame
import os
import math

__version__=0.1
#if os.environ["HIDE_INFO_TEXT"]!="hide":
#    print(f"ZU 2.5D Projection Tool by Zoda" \
#           "Version : {__version__}")
  

class ObjSprite25D:
    """
    ObjSprite25D
    
    size: tuple
        Description: Size of every side
    source: pygame.Surface
        Description: Source File
        
    """
    def __init__(self,size:tuple,source:pygame.Surface):
        self.size=size
        self.source=source
        
    def get_side(self,side_index) -> pygame.Surface:
        """
        
        [INFORMATION] Side Index;
            0 : Top
            1 : Bottom
            2 : Side 0 (camera-facing surface)
            3 : Side 1 (back of the surface facing the camera)
            4 : Side 2 (left side of the surface facing the camera)
            5 : Side 3 (right side of the surface facing the camera)
        """
        line=0
        if side_index>3:
            line+=1
            side_index-=3
        
        return self.source.subsurface((0*side_index,line,*self.size))
        
class Object25D:
    "TODO"
    def __init__(self,sprite:pygame.Surface,align:str):
        self.sprite=sprite
        self.align=align

    