"""
#  PygameTool by Zoda


This Tool Created For Making Games With pygame easy.<br>
Checkout Documention For Help!

Zoda's Website: kerem3338.github.io<br>
Pygametool Documention : zoda.gitbook.io/doc/pygametool


*(This Project Under The Development Using This Library at your own risk)*
```

MIT License


Copyright (c) 2023 Kerem ATA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
"""
import pygame
import time
import datetime
from pathlib import Path
from warnings import warn
import os
import json

from pygametools import debug_mode

SOURCEPATH = Path(__file__).parents[0]

__version__='0.0.1'


def sp(path):
    return os.path.abspath(os.path.join(SOURCEPATH, path))

def isnegative(value:float):
    """Check is value negative."""
    if value>0:
        return False
    else: return True
    
def dateconvert(time):
    """Converts Datetime To (...)"""
    return str(time).replace(' ','_').replace('-','_').replace(':','_')


class ToolError(Exception):
    """
    ToolError.
    """
    def __init__(self,salary):
        super().__init__()
        self.salary=salary

    def __str__(self):return self.salary

class PointList:
    """
    
    2D Point List.

    DESCRIPTION: Generates 2D Point list.
    !CHECKLATER
    
    """
    def __init__(self,starting_value:float,decrease:float):
        self.starting_value:float=starting_value
        "Starting Value"
        self.decrease:float=decrease
        "Decrease value"

        self.pointlist:list=self._create()
        "List"
        

    def _create(self):
        size = self.starting_value * 2 + 1

        center_index = self.starting_value
    
        num_list = [[0] * size for _ in range(size)]
    
        for i in range(size):
            for j in range(size):
                distance = max(abs(center_index - i), abs(center_index - j))
                num_list[i][j] = self.starting_value - distance * self.decrease
    
        return num_list
    



class TextBox:
    def __init__(self, center_x, center_y, width, height, font_size=32, text_color=(255, 255, 255), bg_color=(0, 0, 0)):
        self.width = width
        self.height = height
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.active = False
        self.tag=""

        self.font = pygame.font.Font(None, self.font_size)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (center_x, center_y)
        self.text = ''

        self.returned=False
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.returned=True
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
class SpriteManager:
    """
    SpriteManager

    Description: Access sprites.

    image:pygame.Surface
    type:str ("normal","custom")
        * "normal" : Fixed tile size
        * "custom" : Custom sprite tile size

    """
    def __init__(self,source,type="normal"):
        if source is str:
            source=pygame.image.load(source)
        self.source:pygame.Surface=source
        self.type:str=type

        if not self.type in ("normal","custom"):
            raise ToolError(f"Sprite tile type must be 'normal' or 'custom' not '{self.type}' ")
        self.tile_size=(8,8)
    
    def get_sprites(self, x, y, size: tuple):
        """
        Gets a section of the merged sprite as individual sprites

        # Parameters:
            x: (int) X-coordinate of the section's top-left corner
            y: (int) Y-coordinate of the section's top-left corner
            size: (tuple) [int, int] Size of the section

        Returns:
            sprites: (list) List of individual sprites

        """
        sprites = []
        sprite_width = self.tile_size[0]
        sprite_height = self.tile_size[1]

        for row in range(y, y + size[1]):
            for col in range(x, x + size[0]):
                sprite = pygame.Surface((sprite_width, sprite_height),pygame.SRCALPHA,32)
                sprite.blit(self.source, (0, 0), (col * sprite_width, row * sprite_height, sprite_width, sprite_height))
                sprite=sprite.convert_alpha()
                sprites.append(sprite)

        return sprites

        
    def get_sprite(self, x, y, sprite_size: tuple = None) -> pygame.Surface:
        """
        Get sprite tile from source file.

        # Parameters:
            * x (int)
            * y (int)
            * sprite_size (tuple)
                Defined: 'None'
        """
        if sprite_size is None:
            sprite_size = self.tile_size

        subsurface:pygame.Surface=None
        
        if self.type == "normal":
            subsurface=self.source.subsurface(x * self.tile_size[0], y * self.tile_size[1], sprite_size[0], sprite_size[1])
        elif self.type == "custom":
            subsurface=self.source.subsurface(x * sprite_size[0], y * sprite_size[1], sprite_size[0], sprite_size[1])
        else:
            raise ValueError(f"Sprite tile type must be 'normal' or 'custom', not '{self.type}'")

        if debug_mode:
            #Warn If Tile Is Transparent
            array=pygame.PixelArray(subsurface)
            transparent = all(all(pixel == 0 for pixel in row) for row in array)
            if transparent: warn(f"Tile {x}x{y} is only transparent")

        return subsurface

class MergedSprite:
    """
    MergedSprite
    
    Description: Combine splitted sprites into a single sprite
    Warning: !All sprites must be the same size, this class will not work correctly if all sprites are not the same size!
    
    sprites: (list) pygame.Surface
    sprite_size: (tuple) [float/int,float/int]
        Description: Defines ALL sprites size
        Warning: All sprites must be the same size!
    size: (tuple) [float/int,float/int]
        Description: Merged sprite size (sprite_size[0]*size[0],sprite_size[1]*size[1])
        Warning: TODO
    """

    def __init__(self,sprites:list,sprite_size:tuple,size:tuple):
        self.sprites=sprites
        self.sprite_size=sprite_size
        self.size=size

        
    def convert_all(self):
        """Converts all sprites into one sprite"""
        output_sprite = pygame.Surface((self.sprite_size[0] * self.size[0], self.sprite_size[1] * self.size[1]),pygame.SRCALPHA,32)

        line = 0
        column = 0
        for sprite in self.sprites:
            output_sprite.blit(sprite.convert_alpha(), (column * self.sprite_size[0], line * self.sprite_size[1]))
            
            
            column += 1
            if column == self.size[0]:
                column = 0
                line += 1

        return output_sprite
        


class CheckBox:
    """
    CheckBox

    active: True/False
        Description: Activate CheckBox
    border_color: pygame.color.Color
    background_color: pygame.color.Color
    tick_color: pygame.color.Color
    border_size: int
    width: int
    height: int
    """
    
    def __init__(self,x:int,y:int,active,border_color="black",background_color="white",tick_color="green",border_size=3,width:int=32,height:int=32):
        self.x=x
        self.y=y
        #Look Here
        self.activated=active
        self.border_color=border_color
        self.background_color=background_color
        self.tick_color=tick_color
        self.border_size=border_size
        self.width=width
        self.height=height

        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        
    def update(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(*pygame.mouse.get_pos()):
                if self.activated:
                    self.activated=False
                else:
                    self.activated=True

    def draw(self,surface:pygame.Surface):
        pygame.draw.rect(surface,self.border_color,self.rect,self.border_size)
        if self.activated:
            pygame.draw.rect(surface,self.tick_color,pygame.Rect(self.x+self.width//4,self.y+self.height//4,self.width//2,self.height//2))
class Data:
    "#**Data Class**"
    def __init__(self):
        self.data={}
        self.file=None
    
    def openfile(self,file):
        self.file=open(file,"r+",encoding="utf-8")
        self.data=json.load(self.file)

    def save_to_file(self):
        self.file.seek(0)
        self.file.truncate()
        json.dump(self.data,self.file)


class Room:
    def __init__(self):
        self.done=False

    def update(self):pass
    def event_update(self,event):pass
    def draw(self):pass

    def loop(self):
        while not self.done:
            for event in pygame.event.get():
                self.event_update(event)
            
            self.update()
            self.draw()

           
class Frames:
    """
    Frames

    Description: Animation Frames.
    """
    def __init__(self):
        self.frames:list[pygame.Surface]=[]
        'Animation frames'

    def insertframe_file(self,file:str):
        "Insert single frame from file"
        if not os.path.exists(file):
            raise FileNotFoundError(f"{file} not found.")
        else:
            self.frames.append(pygame.image.load(file))

    def insertframes_file(self,files:list):
        "Insert multiple frames from file using list" 
        for filename in files:
            self.insertframe_file(filename)

    def insertframe_surface(self,frame:pygame.Surface):
        "Insert single frame from a pygame surface"
        self.frames.append(frame)

    def insertframes_surface(self,frames:list):
        "Insert multiple frames from surface using list"
        for frame in frames:
            self.insertframe_surface(frame)

    def insertframes_spritesheet(self,surface:pygame.Surface,frame_size:tuple):
        """
        Insert multiple frames from a spritesheet (needs to be pygame.Surface)

        WARNING: Only horizontal spritesheets can be used!
        TODO
        """
        for i in range(int(surface.get_width()/frame_size[0])):
            self.frames.append(surface.subsurface(pygame.Rect(i*frame_size[0],0,* frame_size)))

class Animation:
    """
    Animation

    Description: 2D Animation
    """
    def __init__(self,frames:Frames,frame_size:tuple):
        self.frames:Frames=frames
        self.frame_size:tuple=frame_size
        
        self.current_frame:int=0
        "Current frame"

        self.tag:str="animation"
        "[For AnimationManager] Animation Tag"

        self.id:int=0
        "[For AnimationManager] Animation Id"

     
    def next_frame(self):
        "Next frame"
        if self.current_frame+1==len(self.frames):
            self.current_frame=0
        else:
            self.current_frame+=1

    def previous_frame(self):
        "Previous frame"
        if self.current_frame == 0:
            self.current_frame = len(self.frames) - 1
        else:
            self.current_frame -= 1

class AnimationManager:
    """
    AnimationManager

    Description: Manages Multiple Animations.
    TODO
    """
    def __init__(self):
        self.animations:list[Animation]={}
        "Animations"

        self.current_animation:str=""
        "Current Animation"

    def add(self,animation:Animation,tag:str):
        "Adds New Animation With Tag"
        if not tag in self.animations:
            self.animations[tag]=animation
        else: Warning(f"Animation '{tag}' redefined!")
    
class Chooser:
    """
    Chooser
    """
    def __init__(self,sprites,x:int,y:int,viewer_size:tuple,chooser_size:tuple,chooser:pygame.Surface):
        self.sprites=sprites
        self.x=x
        self.y=y
        self.viewer_size=viewer_size
        self.chooser_size=chooser_size
        self.chooser=chooser

        self.selection=0
        self.bg="white"
        
        self.viewer=pygame.Surface((self.viewer_size[0],self.viewer_size[1]))
        self.chooser_up=pygame.transform.scale(self.chooser,(self.chooser_size[0],self.chooser_size[1]))
        self.chooser_up_rect=pygame.Rect((self.x+self.viewer_size[0])+self.chooser_size[0],self.y,*self.chooser_size)
        
        self.chooser_down=pygame.transform.scale(pygame.transform.rotate(self.chooser,-180),(self.chooser_size[0],self.chooser_size[1]))
        self.chooser_down_rect=pygame.Rect((self.x+self.viewer_size[0])+self.chooser_size[0],self.y+(self.viewer_size[1]-self.chooser_size[1]),*self.chooser_size)

    def handle_event(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            #WRITEDOC
            if pygame.mouse.get_pressed()[0] and self.chooser_up_rect.collidepoint(*pygame.mouse.get_pos()):
                if self.selection==len(self.sprites)-1:
                    self.selection=0
                else:
                    self.selection+=1

            if pygame.mouse.get_pressed()[0] and self.chooser_down_rect.collidepoint(*pygame.mouse.get_pos()):
                if self.selection-1==-1:
                    self.selection=len(self.sprites)-1
                else:
                    self.selection-=1

    

    


    def draw(self,surface):
        self.viewer.fill(self.bg)
        self.viewer.blit(pygame.transform.scale(self.sprites[self.selection],(self.viewer_size[0],self.viewer_size[1])),(0,0))
        #++++++++++++++++++++++++++++++++++++++++++++++++++#
        surface.blit(self.viewer,(self.x,self.y))
        surface.blit(self.chooser_up,self.chooser_up_rect)
        surface.blit(self.chooser_down,self.chooser_down_rect)

class Log:
    """
    Log

    Description: Log System.

    """
    def __init__(self,title=""):
        self.title=title
        self.log=f"** {self.title} - Pygametools Log System **\n"
    
    def add(self,type,text):
        self.log+=f"{type.upper()} : {text}\n"

    def tadd(self,type,text):
        """Time added Log"""
        self.log+=f"[{datetime.datetime.now()}] {type.upper()} : {text}\n"

    def quick_save(self,datereturn:bool=False,dir:str="."):
        "Quick Save"
        self.add("info","[Quick Save (Log)]")
        date=datetime.datetime.now()
        with open(f"{dir}/quick_save_{str(date).replace(' ','_').replace('-','_').replace(':','_')}.log","w",encoding="utf-8") as f:
            f.write(self.log)

        if datereturn:
            return date
    
    def save(self,filename:str=""):
        "Save the log."
        if filename=="":filename=dateconvert(datetime.datetime.now())
        self.add("info","[Log Save]")
        with open(f"log_{filename}.log","w",encoding="utf-8") as f:
            f.write(self.log)

class Text:
    def __init__(self, text, font_name, font_size, color, x, y, center_x=False, center_y=False, background="white", border=None, border_size=1, border_line_color=(255,255,255),border_color=(0, 0, 0),bg_draw=False):
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.color = color
        self.x = x
        self.y = y
        self.center_x = center_x
        self.center_y = center_y
        self.background = background
        self.border = border
        self.border_size = border_size
        self.border_color = border_color
        self.bg_draw=bg_draw
        self.font = pygame.font.SysFont(font_name, font_size)
        if self.bg_draw:
            self.rendered_text = self.font.render(self.text, True, self.color, self.background)
        else:
            self.rendered_text = self.font.render(self.text, True, self.color)
        self.text_rect = self.rendered_text.get_rect()
        

    def update_render(self):
        if self.bg_draw:
            self.rendered_text = self.font.render(self.text, True, self.color, self.background)
        else:
            self.rendered_text = self.font.render(self.text, True, self.color)
    
    def draw(self, surface):
        if self.center_x:
            self.text_rect.centerx = surface.get_rect().centerx
        else:
            self.text_rect.x = self.x
        if self.center_y:
            self.text_rect.centery = surface.get_rect().centery
        else:
            self.text_rect.y = self.y
        if self.border is not None:
                border_rect = pygame.Rect(self.text_rect.x - self.border_size, self.text_rect.y - self.border_size, self.text_rect.width + 2 * self.border_size, self.text_rect.height + 2 * self.border_size)
                pygame.draw.rect(surface, self.border_color, border_rect)
                pygame.draw.line(surface, self.background, (self.text_rect.x - self.border_size, self.text_rect.y - self.border_size), (self.text_rect.x - self.border_size, self.text_rect.bottom + self.border_size))
                pygame.draw.line(surface, self.background, (self.text_rect.x - self.border_size, self.text_rect.y - self.border_size), (self.text_rect.right + self.border_size, self.text_rect.y - self.border_size))
                pygame.draw.line(surface, self.background, (self.text_rect.right + self.border_size, self.text_rect.y - self.border_size), (self.text_rect.right + self.border_size, self.text_rect.bottom + self.border_size))
                pygame.draw.line(surface, self.background, (self.text_rect.x - self.border_size, self.text_rect.bottom + self.border_size), (self.text_rect.right + self.border_size, self.text_rect.bottom + self.border_size))
        surface.blit(self.rendered_text, self.text_rect)



class Button:
    def __init__(self, x, y,width, height, text, font_size=32, text_color=(255, 255, 255), bg_color=(0, 0, 0), center_x=None, center_y=None):
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.active = False
        self.x=x
        self.y=y
        self.font = pygame.font.Font(None, self.font_size)
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.center_x=center_x
        self.center_y=center_y
        if center_x is None or center_y is None:
            if self.x is None or self.y is None:
                raise ValueError("Either center_x and center_y or x and y should be provided.")
            else:
                self.rect.topleft = (self.x, self.y)
        else:
            self.rect.center = (center_x, center_y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.active = False

    def update_pos(self,x,y):
       self.x=x
       self.y=y

       self.rect.x=x
       self.rect.y=y
    
    def draw(self, screen):
        color = self.bg_color
        if self.active:
            color = (255, 0, 0)  # Aktif olduğunda renk değiştirme
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        
class Dialog:
    def __init__(self, message, font_size=30, font_color=(0, 0, 0), bg_color=(255, 255, 255)):
        pygame.init()
        self.font = pygame.font.SysFont(None, font_size)
        self.message = message
        self.font_color = font_color
        self.bg_color = bg_color
        
        self.clock = pygame.time.Clock()
        self.done = False
        
        self.ok_key=pygame.K_RETURN
        "Ok Key"

    def run(self,surface):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.ok_key:
                        self.done = True

                elif event.type==pygame.MOUSEBUTTONDOWN:
                    self.done=True
            surface.fill(self.bg_color)
            message_lines = self.message.split("\n")
            y_offset = surface.get_rect().height // 2 - len(message_lines) * self.font.get_linesize() // 2
            for line in message_lines:
                message_surface = self.font.render(line, True, self.font_color)
                message_rect = message_surface.get_rect(centerx=surface.get_rect().centerx, y=y_offset)
                surface.blit(message_surface, message_rect)
                y_offset += self.font.get_linesize()
            pygame.display.flip()
            self.clock.tick(60)

class TypingDialog:
    def __init__(self, message, font_size=30, font_color=(0, 0, 0), bg_color=(255, 255, 255), typing_speed=0.1):
        pygame.init()
        self.font = pygame.font.SysFont(None, font_size)
        self.message = message
        self.font_color = font_color
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
        self.done = False
        self.typing_speed = typing_speed
        
        self.ok_key=pygame.K_RETURN
        "Ok Key"

    def run(self,surface):
        current_message = ""
        i = 0
        lines = self.message.split("\n")
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.ok_key:
                        self.done = True

                elif event.type==pygame.MOUSEBUTTONDOWN:
                    self.done=True
            
            surface.fill(self.bg_color)
            y_offset = surface.get_rect().height // 2 - len(lines) * self.font.get_linesize() // 2
            for j in range(len(lines)):
                if i >= len(lines[j]):
                    message_surface = self.font.render(lines[j], True, self.font_color)
                else:
                    message_surface = self.font.render(lines[j][:i+1], True, self.font_color)
                message_rect = message_surface.get_rect(centerx=surface.get_rect().centerx, y=y_offset)
                surface.blit(message_surface, message_rect)
                y_offset += self.font.get_linesize()
            
            i += 1
            
            pygame.display.flip()
            time.sleep(self.typing_speed)
            self.clock.tick(60)


class TypingText:
    def __init__(self, text, x, y, color, font, font_size=32, center_x=False, center_y=False, typing_speed=0.1):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        self.font_size = font_size
        self.center_x = center_x
        self.center_y = center_y
        self.typing_speed = typing_speed
        self.writed = 1

    def draw(self, surface: pygame.Surface) -> pygame.Surface:
        for letter in range(self.writed):
            write = self.font.render(self.text[:self.writed], False, self.color)
            write_rect = write.get_rect()

            if self.center_x != False or self.center_y != False:
                write_rect.center = (self.center_x, self.center_y)
            else:
                write_rect.x = self.x
                write_rect.y = self.y

            surface.blit(write, write_rect)

            if self.writed != len(self.text):
                self.writed += 1


class RepeatedSprite:
    """
    RepeatedSprite

    Description: Creating Repeating Sprite

    sprite: pygame.Surface
    size: [tuple] (int,int)
    """
    def __init__(self,sprite:pygame.Surface,size:tuple):
        self.sprite=sprite
        self.size=size

    def get_output(self) -> pygame.Surface:
        output_surface=pygame.Surface((self.sprite.get_width()*self.size[0],self.sprite.get_height()*self.size[1]))
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                output_surface.blit(self.sprite,(x*self.sprite.get_width(),y*self.sprite.get_height()))

        return output_surface

        

class Object:
    "2D Game Object"
    def __init__(self):
        self.rects:list[pygame.Rect]=[]
        "Object Rects."

        self.animations:AnimationManager=AnimationManager()
        "Object Animations"


    def addrect(self,rect:pygame.Rect):
        "Add new rect for object."
        self.rects.append(rect)

    def collision_check(self,rect_id:int,check_rect:pygame.Rect) -> bool:
        if not rect_id in range(len(self.rects)):
            raise ToolError("Invalid Rect Id!")
        else:
            return self.rects[rect_id].colliderect(check_rect)