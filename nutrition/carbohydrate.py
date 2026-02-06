import dataclasses
from ._base import Macro


@dataclasses.dataclass
class Carbohydrate(Macro):
    """
    Carbohydrate macronutrient in grams.
    Can optionally subdivide into sugars and complex carbs.
    """
    
    amount: float = 0.0
    
    # Optional subdivision
    sugars: float = 0.0
    complex: float = 0.0

    def set_amount(self, grams: float):
        """Sets total carbohydrate amount in grams."""
        self.amount = grams
        return self

    def set_distribution(self, sugars: float = 0.0, complex: float = 0.0):
        """
        Optional: distribute carbs into sugars and complex.
        Args are percentages (0.0-1.0) of total amount.
        """
        self.sugars = sugars * self.amount
        self.complex = complex * self.amount
        return self