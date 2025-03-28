import re


def parse_recipe(selected_ingredients, servings):
    parsed_ingredients = []
    print(f"Processing ingredients: {selected_ingredients}")  # Debugging line

    for ingredient in selected_ingredients:
        print(f"Processing ingredient: {ingredient}")  # Debugging line
        # Updated regular expression to handle different ingredient formats
        match = re.match(r"(\d+(\.\d+)?)\s*(\w+)?\s*(.*)", ingredient.strip())

        if match:
            print(f"Match found for: {ingredient}")  # Debugging line
            quantity = float(match.group(1))  # Get the numeric part of the quantity
            unit = match.group(3) if match.group(3) else ""  # Handle unit (e.g., cup, ounce)
            ingredient_name = match.group(4).strip()  # Get the rest of the ingredient

            # Multiply the quantity by the servings
            adjusted_quantity = quantity * servings
            print(f"Adjusted quantity: {adjusted_quantity} for servings: {servings}")  # Debugging line

            # Format the adjusted ingredient
            adjusted_ingredient = f"{adjusted_quantity} {unit} {ingredient_name}".strip()
            parsed_ingredients.append(adjusted_ingredient)
        else:
            print(f"No match found for: {ingredient}")  # Debugging line
            # If no match (non-quantifiable ingredient), just append as is
            parsed_ingredients.append(ingredient.strip())

    print(f"Adjusted Ingredients for {servings} servings: {parsed_ingredients}")  # Debugging line
    return parsed_ingredients
