import dataclasses
from ._base import Macro


@dataclasses.dataclass
class Fat(Macro):
    """Fat macronutrient in grams."""
    
    amount: float = 0.0

    def set_amount(self, grams: float):
        """Sets fat amount in grams."""
        self.amount = grams
        return self

    def set_distribution(self, **kwargs):
        """Fat has no subcategories."""
        return self