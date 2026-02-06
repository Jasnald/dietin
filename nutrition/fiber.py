import dataclasses
from ._base import Macro


@dataclasses.dataclass
class Fiber(Macro):
    """Fiber in grams."""
    
    amount: float = 0.0

    def set_amount(self, grams: float):
        """Sets fiber amount in grams."""
        self.amount = grams
        return self

    def set_distribution(self, **kwargs):
        """Fiber has no subcategories."""
        return self