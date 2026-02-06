import dataclasses
from nutrition import Protein, Fat, Carbohydrate, Fiber, Macro


def fac(function):
    """Shortcut for dataclasses.field(default_factory=...)."""
    return dataclasses.field(default_factory=function)


@dataclasses.dataclass
class Food:
    """
    Represents a food item with all its macronutrients.
    """
    
    protein: Protein = fac(Protein)
    fat: Fat = fac(Fat)
    carbohydrate: Carbohydrate = fac(Carbohydrate)
    fiber: Fiber = fac(Fiber)

    def set_macros(self, **amounts):
        """
        Sets macro amounts in grams.
        Example: food.set_macros(protein=20, fat=10, carbohydrate=30, fiber=5)
        """
        for macro_name, grams in amounts.items():
            if hasattr(self, macro_name):
                macro = getattr(self, macro_name)
                if isinstance(macro, Macro):
                    macro.set_amount(grams)
        return self

    def set_distributions(self, **configs):
        """
        Sets distributions for macros that support it.
        Example: food.set_distributions(carbohydrate={'sugars': 0.6, 'complex': 0.4})
        """
        for macro_name, details in configs.items():
            if hasattr(self, macro_name):
                macro = getattr(self, macro_name)
                if isinstance(macro, Macro):
                    macro.set_distribution(**details)
        return self

    def calories(self):
        """Calculate total calories (protein: 4, carbs: 4, fat: 9)."""
        return (
            self.protein.amount * 4 +
            self.carbohydrate.amount * 4 +
            self.fat.amount * 9
        )

    def __str__(self):
        """Display non-zero macros."""
        parts = []
        
        for field in dataclasses.fields(self):
            macro = getattr(self, field.name)
            
            active_fields = []
            for subfield in dataclasses.fields(macro):
                value = getattr(macro, subfield.name)
                if value != 0.0:
                    active_fields.append(f"{subfield.name}={value}g")
            
            if active_fields:
                parts.append(f"{field.name.title()}: {', '.join(active_fields)}")
        
        if parts:
            parts.append(f"Total: {self.calories():.0f} kcal")
        
        return "\n".join(parts) if parts else "Empty food"

    def summary(self):
        """Quick overview of main macro amounts."""
        return (
            f"P: {self.protein.amount}g | "
            f"C: {self.carbohydrate.amount}g | "
            f"F: {self.fat.amount}g | "
            f"Fiber: {self.fiber.amount}g | "
            f"{self.calories():.0f} kcal"
        )


def create_food(macros: dict, distributions: dict = None):
    """Helper to create a food item in one call."""
    food = Food()
    food.set_macros(**macros)
    if distributions:
        food.set_distributions(**distributions)
    return food