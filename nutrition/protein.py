import dataclasses
from ._base import Macro


@dataclasses.dataclass
class Protein(Macro):
    """Protein macronutrient in grams."""
    
    amount: float = 0.0

    def set_amount(self, grams: float):
        """Sets protein amount in grams."""
        self.amount = grams
        return self

    def set_distribution(self, **kwargs):
        """Protein has no subcategories."""
        return self