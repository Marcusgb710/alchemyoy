from typing_extensions import SupportsIndex

class Items(list):

    def _pop(self, __index: SupportsIndex = -1):
        return super().pop(__index)

    def insert(self, __index: SupportsIndex, __object) -> None:
        return super().insert(__index, __object)

    def remove(self, __value) -> None:
        return super().remove(__value)

    def append(self, __object) -> None:
        return super().append(__object)
    
    def sort(self):
        return super().sort(key=lambda x : x.name)
    
    def get_last_item(self):
        return self[-1]
    
    def get_first_item(self):
        return self[0]
    
    def get(self, idx: int|float):
        return self[idx]
    
    
