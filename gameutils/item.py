from typing import override
import pygame

class Item:
    def __init__(self, x: int, y: int, w: int, h: int, img: pygame.Surface, item_info):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = img
        self.item_info = item_info

    def __str__(self) -> str:
        return f"X:{self.x}, Y:{self.y}, W:{self.w}, H:{self.h}, ITEM INFO: {self.item_info}"
    
    
    def check_for_pointer(self,x, y):
        radius = 16
        detaction_radius = abs(((self.x+self.img.get_width()/2)-x)**2 + ((self.y+self.img.get_height()/2)-y)**2) < radius**2
        return detaction_radius
    

    def set_pos(self, x:int, y: int) -> None:
        self.x = (x - self.img.get_width()/2)
        self.y = (y - self.img.get_height()/2)

    def clicked(self, x: int, y:int) -> bool:
        img_rect = self.img.get_rect()
        if x > self.x and x < self.x + img_rect.w and\
        y > self.y and y < self.y + img_rect.h:
            
            return True
        return False
    
    

    def draw(self, pygame:pygame, win:pygame.Surface) -> None:
        #OLD OBJECT TESTING pygame.draw.rect(win, (255, 255, 255), pygame.Rect(self.x, self.y, self.w, self.h))
        
        win.blit(self.img, (self.x, self.y))
        