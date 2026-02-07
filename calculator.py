import yaml
from pathlib import Path
from loader import load_library, load_yaml

def find_meal_data(query_name):
    """
    Busca uma refeição pelo nome.
    Agora suporta arquivos com MÚLTIPLAS refeições separadas por '---'.
    """
    meals_dir = Path('meals')
    
    # Varre todos os arquivos .yaml na pasta meals
    for file_path in meals_dir.glob('*.yaml'):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                # O safe_load_all lê o arquivo em pedaços (separados por ---)
                # Convertemos para lista para poder procurar dentro
                docs = list(yaml.safe_load_all(f))
                
                for doc in docs:
                    # Verifica se o documento é válido e se tem o nome que queremos
                    if doc and doc.get('meal') == query_name:
                        print(f"   -> Encontrado dentro de '{file_path.name}'")
                        return doc
            except yaml.YAMLError as e:
                print(f"Erro ao ler {file_path.name}: {e}")

    return None

def calculate_meal_calories(totals):

    totals['calories'] = (
        totals['protein'] * 4 + 
        totals['carbohydrate'] * 4 + 
        totals['fat'] * 9
        )
    return totals['calories']

def print_nutrition_report(totals):

    print("=" * 40)
    print(f"Protein:      {totals['protein']:.1f}g")
    print(f"Carbs:        {totals['carbohydrate']:.1f}g")
    print(f"  ├─ Sugars:  {totals['sugars']:.1f}g")
    print(f"  └─ Complex: {totals['complex_carbs']:.1f}g")
    print(f"Fat:          {totals['fat']:.1f}g")
    print(f"Fiber:        {totals['fiber']:.1f}g")
    print("-" * 40)
    print(f"Calories:     {totals['calories']:.0f} kcal")
    
def totals_dict():
    return {
        'protein': 0.0, 'fat': 0.0, 'carbohydrate': 0.0, 
        'fiber': 0.0, 'sugars': 0.0, 'complex_carbs': 0.0, 'calories': 0.0
    }

def calculate_nutrient_values(multiplier, food_obj):

    p = food_obj.protein.amount * multiplier
    f = food_obj.fat.amount * multiplier
    c = food_obj.carbohydrate.amount * multiplier
    fib = food_obj.fiber.amount * multiplier
    
    sug = food_obj.carbohydrate.sugars * multiplier
    cplx = food_obj.carbohydrate.complex * multiplier
    return p, f, c, fib, sug, cplx

def update_totals(obj, params):

    p, f, c, fib, sug, cplx = params
    obj['protein'] += p
    obj['fat'] += f
    obj['carbohydrate'] += c
    obj['fiber'] += fib
    obj['sugars'] += sug
    obj['complex_carbs'] += cplx

def categories_iteration(categories, meal_data):

    item_list =[]
    for library_cat in categories:
        item_i = meal_data.get(library_cat, [])
        item_list.extend(item_i)

    return item_list

def macro_iteration(item_list, library, totals):

    for item in item_list:
        food_name = item['name']
        
        # Quantity Logic (Grams vs Servings)
        if 'grams' in item:
            multiplier = item['grams'] / 100.0
        elif 'servings' in item:
            multiplier = item['servings']
        else:
            multiplier = 1.0
        
        food_obj = library.get(food_name)   
        params = calculate_nutrient_values(multiplier, food_obj)
        update_totals(totals, params)

def add_to_daily(daily, meal):
    for key in daily:
        daily[key] += meal[key]

def calculate_nutrition(meal_list):
    library = load_library()
    
    totals = totals_dict()
    
    print(f"Calculating nutrition for: {', '.join(meal_list)}\n")
    
    for meal in meal_list:
        # Use the new search function
        meal_data = find_meal_data(meal)
        meal_total = totals_dict() 
        meal_title = meal_data.get('meal', meal)
        print(f"--- {meal_title} ---")
        
        # Categories to scan for food items
        library_cat = ['foods', 'protein', 'carbo', 'fat', 'vegetables', 'extras']
        
        macro_source_list = categories_iteration(library_cat, meal_data)

        macro_iteration(
            macro_source_list, 
            library, 
            meal_total
            )
        
        calculate_meal_calories(meal_total)
        
        print_nutrition_report(meal_total)
        
        add_to_daily(
            totals, 
            meal_total
            )

        
        print()
    
    # Calorie Calculation
    calculate_meal_calories(totals)
    
    # Final Report
    print_nutrition_report(totals)
    
    return totals

if __name__ == "__main__":
    # Agora você pode passar o NOME EXATO que está dentro do yaml
    # Exemplo: Se no lunch.yaml está 'meal: Marmita de Wrap (1/5)'
    my_day = ['Marmita de Wrap (1/5)', 'Marmita de Salmão (1/5)', 'Iogurte Turbinado', 'Pao_com_ovo', 'Whey_maquina'] 
    calculate_nutrition(my_day)