from typing import Optional


class Sprite:
    def __init__(self, raw_data:dict):
        self.data = raw_data

    @property
    def raw(self) -> dict:
        return self.data
    
    @property
    def front_default(self) -> Optional[str]:
        return self.data.get('front_default')
    
    @property
    def front_female(self) -> Optional[str]:
        return self.data.get('front_female')

    @property
    def front_shiny(self) -> Optional[str]:
        return self.data.get('front_shiny')

    @property
    def back_default(self) -> Optional[str] :
        return self.data.get('back_default')
    
    @property
    def back_female(self) -> Optional[str]:
        return self.data.get('back_female')
