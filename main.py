
from typing import NewType
from utils.gameitems import GameItems
from utils.items import Items
from gameutils.item import Item
import json
import pygame
import os
import sys


class LilAlchemyPy:

    def __init__(self):
        self.__fps = 120
        self.__gameoption ="GUI"
        self.path = os.path.join(os.getcwd(),"lilalchemypy", "recipies.json")
        with open(self.path, "r") as f:
            receps = json.load(f)
            self.json_recepies = receps["items"]
            f.close()
        self.items = Items()
        self.gui_items = Items()
        self.window_items = Items()
        self.win = pygame.display
        self.clock = pygame.time.Clock()
        self.run = True
        self.current_hovered_selection = None
        self.selection1 = None
        self.selection2 = None
        self.current_input_text = "Enter a selection or press Q to Exit: "
        self.item_gui_y = 0

    def change_input_text(self, text):
        self.current_input_text = text

    def gameinit(self):
        for inst in GameItems.gameitem_ref:
            inst: GameItems = inst
            self.items += inst.items
            GameItems.gameitem_ref.remove(inst)
            del inst
    

    def isitem(self):
        return isinstance(self.selection1, Item) and isinstance(self.selection2, Item)

    def get_item_by_name(self, name: str):
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
    def get_jitem_by_name(self, name):
        if name.lower() in self.json_recepies.keys():

            return self.json_recepies[name.lower()]
        
    def check_recepies(self, selection1, selection2, i):
        
        if selection1.name.lower() in i.keys():
                selection1_obj = i[(selection1.name.lower())]
                recepies = selection1_obj["recepies"]
                #result = [x if selection2.name.lower() == x["name"].lower() else None for x in recepies]
                for recepie in recepies:
                    if recepie["name"].lower() == selection2.name.lower():
                        return recepie

    def unlock_item(self, name):
        if self.isitem():
            for item in self.gui_items:
                if item.item_info.name.lower() == name.lower():
                    item.item_info.unlocked = True
                    return
            return  
        for item in self.items:
            if item.name.lower() == name.lower():
                item.unlocked = True
                return

    def check_for_combo(self):
        if isinstance(self.selection1, Item) and isinstance(self.selection2, Item):
            selection_check = self.check_recepies(self.selection1.item_info, self.selection2.item_info, self.json_recepies)
            if selection_check == None:
                selection_check = self.check_recepies(self.selection2.item_info, self.selection1.item_info, self.json_recepies)
            if selection_check != None:
                item_info = self.get_item_by_name(selection_check["result"].lower())
                item_info.unlocked = True
                img = pygame.image.load(os.path.join(os.getcwd(), "lilalchemypy", "imgs",self.get_jitem_by_name(selection_check["result"].lower())["png"]))
                _item_ = Item(20, self.gui_items[-1].y+img.get_height(), 0, 0, img, item_info)
                
                return _item_
            
            return False

        
        selection_check = self.check_recepies(self.selection1, self.selection2, self.json_recepies)
        if selection_check == None:
            selection_check = self.check_recepies(self.selection2, self.selection1, self.json_recepies)

        
        if selection_check != None:
            self.unlock_item(selection_check["result"])  
            return selection_check["result"]
        return False

    def cli(self):
         while self.run:
            for i, item in enumerate(self.items):
                if item.unlocked:
                    print(f"[{i}] {item.name}")
            user_input = input(self.current_input_text)

            match user_input:
                case "q":
                    self.run = False

                case _:
                    if user_input.isdigit():
                        if self.selection1 == None and self.selection2 == None:
                            self.change_input_text("Enter a selection or press Q to Exit: ")
                        try:
                            self.change_input_text("Now Pick The Second Item or Press Q To quit ")
                            if self.selection1 != None:
                                self.selection2 = self.items[int(user_input)]
                                #print(f"{self.selection1} and {self.selection2}")
                                p = self.check_for_combo()
                                print(p)
                                self.selection1 = None
                                self.selection2 = None
                                continue
                            self.selection1 = self.items[int(user_input)]
                        except IndexError:
                            print("Item Index Does Not Exist")
#pygame code goes here

    def rmvitems(self, obj):
        for items in self.window_items:
            if items == obj:
                self.window_items.remove(items)


    def player_controls(self, mouse: pygame.mouse, items):
        _mouse = mouse.get_pressed()
        #print(self.current_hovered_selection)
        for event in pygame.event.get():
                if event.type  == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button ==4:
                        for i in self.gui_items:
                            i.y -= i.img.get_height()//6

                    if event.button == 5:
                        for i in self.gui_items:
                            i.y += i.img.get_height()//6

                    if event.button == 1:
                        print(event)
                        for window_item in self.window_items:
                                _item: Item = window_item
                                if window_item.clicked(event.pos[0], event.pos[1]):
                                    self.selection1 = _item
                                    return
                                    
                        for item in items:
                            _item: Item = item
                            if _item.item_info.unlocked:
                                if _item.clicked(event.pos[0], event.pos[1]):
                                        
                                        self.selection1 = Item(event.pos[0], event.pos[1], 0, 0, _item.img, _item.item_info)
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                   
                    if self.selection1 != None:
                        self.window_items.append(self.selection1)
                    if self.selection1 != None and self.current_hovered_selection != None:
                        self.selection2 = self.current_hovered_selection
                    
                    if self.selection1 != None and self.selection2 != None:
                        i = self.check_for_combo()
                        
                        
                        if isinstance(i, Item) and i.item_info.name.lower() not in [x.item_info.name.lower() for x in self.gui_items]:
                        
                            print(i)
                            self.gui_items.append(i)
                            self.item_gui_y += i.img.get_height()
                            self.rmvitems(self.selection1)
                            self.rmvitems(self.selection2)
                    self.selection1 = None
                    self.selection2 = None
                    
                    self.current_hovered_selection = None
                    
        

        if _mouse == (1, 0, 0) and self.selection1 != None:
            mouse_pos = mouse.get_pos()
            self.selection1.set_pos(mouse_pos[0], mouse_pos[1])
            for window_item in self.window_items:
                if window_item is self.selection1:
                    continue
                if window_item.check_for_pointer(self.selection1.x+self.selection1.img.get_width()/2, self.selection1.y+self.selection1.img.get_height()/2):
                    
                    self.current_hovered_selection = window_item
                    return
                self.current_hovered_selection = None
                
                
            
            

            
        
    def redraw(self, win: pygame.surface.Surface, items) -> None:
        win.fill((120, 81, 169))

        if self.selection1 != None:
            self.selection1.draw(pygame, win)

        if self.window_items:
            for item in self.window_items:
                item.draw(pygame, win)

        for item in self.gui_items:
            if item.item_info.unlocked:
                
                item.draw(pygame, win)

        pygame.display.update()

    def gui(self):
        win = self.win.set_mode((500, 500))
  
        for item in self.items:
                if item.unlocked:
                    item_png = self.json_recepies[item.name.lower()]["png"]
                    img = pygame.image.load(os.path.join(os.getcwd(), "lilalchemypy", "imgs",item_png))
                    _item = Item(20, self.item_gui_y, 15, 15, img, item)
                    self.item_gui_y += img.get_height()
                    self.gui_items.append(_item)
                    
        
        while self.run:
            

            self.player_controls(pygame.mouse, self.gui_items)


            self.redraw(win, self.gui_items)
                
    
#pygame code goes here   
    def main(self):
        import items
        self.gameinit()

        match self.__gameoption:
            case "CLI":
                self.cli()
            case "GUI":
                self.gui()
            case _:
                print("PizzaPizza")






if __name__ == "__main__":
    
    lilalchemy = LilAlchemyPy()
    lilalchemy.main()
    print(len(GameItems.gameitem_ref))