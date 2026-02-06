import dataclasses
from abc import ABC, abstractmethod


@dataclasses.dataclass
class Macro(ABC):
    """
    Abstract base class for macronutrients.
    """

    @abstractmethod
    def set_amount(self, grams: float) -> "Macro":
        """Sets total amount in grams."""
        pass

    @abstractmethod
    def set_distribution(self, **kwargs) -> "Macro":
        """Distributes into subcategories if applicable."""
        pass