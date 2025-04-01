class ParseIngredients:
    # Example density database (in oz per cup)
    density_db = {
        'dried shiitake mushrooms': 0.5,  # Example density
        'white miso paste': 9.0,          # Example density
        'soy sauce': 8.5,                 # Example density
        'rice vinegar': 8.0,              # Example density
        'garlic': 5.0,                    # Example density
        'ginger paste': 8.0,              # Example density
        'instant ramen noodles': 3.5      # Example density per package
    }
    
    def ingredient_parse(self, ingredient_list):
        pattern = r'(?P<amount>[\d/\.]+)\s*(?P<measurement>\b(?:cups?|tablespoons?|tbsp?|teaspoons?|tsp?|cloves?|packages?)\b)?\s*(?P<ingredient>.+)'
        
        dict_ingredients = []
        
        for ingredient_str in ingredient_list:
            match = re.match(pattern, ingredient_str)
            
            if match:
                amount = match.group('amount')
                measurement = match.group('measurement') or ''
                ingredient = match.group('ingredient').strip()
                
                try:
                    amount = float(eval(amount))
                except:
                    pass
                
                # Convert to weight in ounces
                weight_oz = self.convert_to_ounces(amount, measurement, ingredient)
                
                dict_ingredients.append({
                    'ingredient': ingredient,
                    'measurement': measurement,
                    'amount': amount,
                    'weight_oz': weight_oz
                })
        
        return dict_ingredients
    
    def convert_to_ounces(self, amount, measurement, ingredient):
        # Conversion factors
        conversion_factors = {
            'cup': 1,
            'tablespoon' or 'tbsp': 1/16,
            'teaspoon' or 'tsp': 1/48,
            'clove': 1/6,  # Example conversion for garlic
            'package': 3.5  # Example conversion for ramen noodles
        }
        
        # Normalize measurement to singular form
        measurement = measurement.rstrip('s')
        
        # Get the conversion factor
        conversion_factor = conversion_factors.get(measurement, 1)
        
        # Get the density of the ingredient
        density = self.density_db.get(ingredient, 1)
        
        # Calculate weight in ounces
        weight_oz = amount * conversion_factor * density
        
        return weight_oz

def main():
    ingredient_list = [
        '2 cups dried shiitake mushrooms',
        '1 tablespoon white miso paste',
        '1 tbsp white miso paste',
        '2 teaspoons soy sauce',
        '2 teaspoons rice vinegar',
        '1 clove garlic',
        '1/2 teaspoon ginger paste',
        '2(3.5-ounce) packages instant ramen noodles, seasoning packets discarded'
    ]
    
    parser = ParseIngredients()
    dict_ingredients = parser.ingredient_parse(ingredient_list)
    
    # Print the result
    for ingredient in dict_ingredients:
        print(ingredient)

main()
