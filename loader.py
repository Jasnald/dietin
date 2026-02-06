import yaml
from pathlib import Path
from food import create_food


def load_library():
    """Reads all YAMLs in library/ and creates Food objects."""
    library = {}
    
    base_dir = Path(__file__).parent / 'library'
    
    for file_path in base_dir.glob('*.yaml'):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        
        for food_name, specs in data.items():
            library[food_name] = create_food(
                macros=specs['macros'],
                distributions=specs.get('distributions')
            )
    
    return library