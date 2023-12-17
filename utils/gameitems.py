from utils.items import Items
import weakref
class GameItems:
    gameitem_ref = []
    def __init__(self):
        self.__class__.gameitem_ref.append(weakref.proxy(self))
        self.items = Items()

    def additem(self, item):
        self.items.append(item)