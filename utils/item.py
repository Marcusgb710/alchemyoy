
class Item:
    
    def __init__(self, name, unlocked=False):
        
        self.name = name
        self.unlocked = unlocked

    def unlock(self) -> None:
        self.unlocked = True
    
    def lock(self) -> None:
        self.unlocked = False

    def __str__(self) -> str:
        return f"""
        name: {self.name},
        unlocked: {self.unlocked}
"""
    
    def __repr__(self) -> str:
        return f"Item(name: {self.name}, unlocked: {self.unlocked})"

type item = Item