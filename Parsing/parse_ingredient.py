"""Current density is a placeholder for updates later. Will need to alter how that is parsed and what the weights are based on density. 
    This is used to get the weigh in ouces, so that we can get the lowest quantity / amount needed to satisfy the ingredient in thte list."""

import re
import pandas as pd

class ParseIngredients:
    def __init__(self, density_file):
        # Load density data from CSV file
        self.density_db = self.load_density_data(density_file)
    
    def load_density_data(self, density_file):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(density_file)
        
        # Convert the DataFrame to a dictionary
        density_dict = pd.Series(df.density.values, index=df.ingredient).to_dict()
        
        return density_dict
    
    def ingredient_parse(self, ingredient_list):
        pattern = r'(?P<amount>[\d/\.]+)\s*(?P<measurement>\b(?:cups?|tablespoons?|teaspoons?|cloves?|packages?)\b)?\s*(?P<ingredient>.+)'
        
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
            'tablespoon': 1/16,
            'teaspoon': 1/48,
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
    ingredient_list = ingredients_list #double check this is the correct var.
    
    # Path to the CSV file containing density data
    density_file = 'ingredient_densities.csv'
    
    parser = ParseIngredients(density_file)
    dict_ingredients = parser.ingredient_parse(ingredient_list)
    
    # Print the result
    for ingredient in dict_ingredients:
        print(ingredient)

main()
