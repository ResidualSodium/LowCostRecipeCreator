import re


def parse_recipe(selected_ingredients, servings):
    parsed_ingredients = {}
    print(f"Processing ingredients: {selected_ingredients}")  # Debugging line

    for ingredient in selected_ingredients:
        print(f"Processing ingredient: {ingredient}")  # Debugging line
        # Updated regular expression to handle different ingredient formats
        match = r'(?P<amount>[\d/\.]+)\s*(?P<measurement>\b(?:cups?|tablespoons?|teaspoons?|cloves?|packages?)\b)?\s*(?P<ingredient>.+)'
        # match = re.match(r"(\d+(\.\d+)?)\s*(\w+)?\s*(.*)", ingredient.strip())

        if match:
            print(f"Match found for: {ingredient}")  # Debugging line
            quantity = float(match.group('amount'))  # Get the numeric part of the quantity
            measurement = match.group('measurement') #getting the measurement for later alterations
            ingredient_name = match.group('ingredient') #get the ingredient type here 
            
            # Multiply the quantity by the servings
            adjusted_quantity = quantity * servings
            print(f"Adjusted quantity: {adjusted_quantity} for servings: {servings}")  # Debugging line

            # Format the adjusted ingredient
            adjusted_ingredient = f"{adjusted_quantity} {measurement} {ingredient_name}".strip()
            parsed_ingredients.append(adjusted_ingredient)
        else:
            print(f"No match found for: {ingredient}")  # Debugging line
            # If no match (non-quantifiable ingredient), just append as is
            weight_oz = convert_to_weight(amount, measurement, ingredient)
            parsed_ingredients.append({
                'ingredient_name': ingredient_name,
                'quantity' : quantity,
                'measurement' : measurement,
                'weight' : weight_oz
            })

    print(f"Adjusted Ingredients for {servings} servings: {parsed_ingredients}")  # Debugging line
    conert_to_weight(parsed_ingredients)

def convert_to_weight(parsed_ingredients):
    #density_db = density.csv  # Need to add in a density chart to convert to weights where applicable.

    parsed_ingredients = parsed_ingredients
    
    conversion_factors = {
        'cup' : 1,
        'tablespoon' or 'tablespoons' or 'tbsp' or tbsps : 1/16,
        'teaspoon' or 'teaspoons' or 'tsp' or 'tsps' : 1/48,
        'pints' or 'pint' : 2,
        'quart' or 'quarts' : 4,
        'gallon' or 'gallons': 8
        }    

    measurment = measurement.strip('s')

    conversion_factor = conversion_factors.get(measurement, 1)

    density = self.density_db.get(ingredient, 1)

    weight_oz = amount * conversion_factor * density

    
