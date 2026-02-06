import yaml
import dataclasses
from collections import defaultdict
from pathlib import Path
from loader import load_library


def calculate_nutrition(meal_list):
    """
    Calculates total nutrition from a list of meals.
    
    Args:
        meal_list: List of meal names (without .yaml extension)
    
    Returns:
        Dictionary with total macros
    """
    library = load_library()
    
    totals = {
        'protein': 0.0,
        'fat': 0.0,
        'carbohydrate': 0.0,
        'fiber': 0.0,
        'sugars': 0.0,
        'complex_carbs': 0.0,
        'calories': 0.0
    }
    
    print(f"Calculating nutrition for: {', '.join(meal_list)}\n")
    
    for meal_name in meal_list:
        meal_path = Path('meals') / f"{meal_name}.yaml"
        
        if not meal_path.exists():
            print(f"ERROR: Meal '{meal_name}' not found.")
            continue
        
        with open(meal_path, 'r', encoding='utf-8') as f:
            meal_data = yaml.safe_load(f)
        
        print(f"--- {meal_data.get('meal', meal_name)} ---")
        
        for item in meal_data.get('foods', []):
            food_name = item['name']
            servings = item['servings']
            
            food_obj = library.get(food_name)
            
            if not food_obj:
                print(f"WARNING: '{food_name}' not in library.")
                continue
            
            # Calculate amounts
            protein = food_obj.protein.amount * servings
            fat = food_obj.fat.amount * servings
            carbs = food_obj.carbohydrate.amount * servings
            fiber = food_obj.fiber.amount * servings
            
            sugars = food_obj.carbohydrate.sugars * servings
            complex = food_obj.carbohydrate.complex * servings
            
            # Update totals
            totals['protein'] += protein
            totals['fat'] += fat
            totals['carbohydrate'] += carbs
            totals['fiber'] += fiber
            totals['sugars'] += sugars
            totals['complex_carbs'] += complex
            
            # Display
            display_servings = f"{servings}x" if servings != 1 else ""
            print(f"  {display_servings}{food_name}: P={protein:.1f}g C={carbs:.1f}g F={fat:.1f}g Fiber={fiber:.1f}g")
        
        print()
    
    # Calculate total calories
    totals['calories'] = (
        totals['protein'] * 4 +
        totals['carbohydrate'] * 4 +
        totals['fat'] * 9
    )
    
    # Print summary
    print("=" * 60)
    print("DAILY TOTALS")
    print("=" * 60)
    print(f"Protein:         {totals['protein']:.1f}g")
    print(f"Carbohydrate:    {totals['carbohydrate']:.1f}g")
    print(f"  ├─ Sugars:     {totals['sugars']:.1f}g ({totals['sugars']/totals['carbohydrate']*100:.0f}%)" if totals['carbohydrate'] > 0 else "")
    print(f"  └─ Complex:    {totals['complex_carbs']:.1f}g ({totals['complex_carbs']/totals['carbohydrate']*100:.0f}%)" if totals['carbohydrate'] > 0 else "")
    print(f"Fat:             {totals['fat']:.1f}g")
    print(f"Fiber:           {totals['fiber']:.1f}g")
    print(f"\nTotal Calories:  {totals['calories']:.0f} kcal")
    
    # Macro ratios
    print("\n" + "=" * 60)
    print("MACRO DISTRIBUTION")
    print("=" * 60)
    protein_pct = (totals['protein'] * 4 / totals['calories']) * 100
    carb_pct = (totals['carbohydrate'] * 4 / totals['calories']) * 100
    fat_pct = (totals['fat'] * 9 / totals['calories']) * 100
    
    print(f"Protein:      {protein_pct:.1f}%")
    print(f"Carbohydrate: {carb_pct:.1f}%")
    print(f"Fat:          {fat_pct:.1f}%")
    
    return totals


if __name__ == "__main__":
    my_day = ['breakfast', 'lunch']
    calculate_nutrition(my_day)