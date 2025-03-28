from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton, QLabel, QLineEdit
from PyQt6.QtGui import QIntValidator  # Correct import for integer validation


class ChecklistGUI(QDialog):  # Assuming QDialog is being used
    def __init__(self, ingredients, parent=None):
        super().__init__(parent)
        self.ingredients = ingredients
        print(f"Ingredients in ChecklistGUI: {self.ingredients}")  # Debugging line
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ingredient Checklist')

        layout = QVBoxLayout()

        # Create a label for instructions
        self.instruction_label = QLabel('Select the ingredients you have:')
        layout.addWidget(self.instruction_label)

        # Create checkboxes for each ingredient
        self.checkboxes = []  # Store references to checkboxes
        for ingredient in self.ingredients:
            if ingredient:  # Skip empty ingredients
                checkbox = QCheckBox(ingredient)
                self.checkboxes.append(checkbox)
                layout.addWidget(checkbox)

        # Create a label and input box for servings
        self.servings_label = QLabel('Enter the number of servings:')
        layout.addWidget(self.servings_label)

        # Create a QLineEdit for the servings box and restrict to numeric input
        self.servings_input = QLineEdit(self)
        self.servings_input.setPlaceholderText("Enter servings")

        # Set the validator to only allow integers
        self.servings_input.setValidator(QIntValidator(1, 100, self))  # You can change the range as needed
        layout.addWidget(self.servings_input)

        # Create a button to close the checklist
        self.done_button = QPushButton('Done', self)
        self.done_button.clicked.connect(self.on_done_button_click)
        layout.addWidget(self.done_button)

        self.setLayout(layout)

    def on_done_button_click(self):
        # Filter out the checked ingredients (those that are selected)
        unselected_ingredients = [checkbox.text() for checkbox in self.checkboxes if not checkbox.isChecked()]

        servings = self.servings_input.text()  # Get the value from the servings input

        if not unselected_ingredients:
            print("No ingredients selected (all ingredients were checked).")
            return

        if not servings.isdigit():
            print("Please enter a valid number for servings.")
            return

        servings = int(servings)  # Convert servings to an integer
        print(f"Unselected Ingredients: {unselected_ingredients}, Servings: {servings}")  # Debugging line

        # Pass the unselected ingredients and servings to the recipe parser
        from scraping.recipe_parser import parse_recipe  # Import parse_recipe from the parser
        adjusted_ingredients = parse_recipe(unselected_ingredients, servings)  # Receive the adjusted ingredients

        # Debugging the parsed results
        print(f"Adjusted Ingredients: {adjusted_ingredients}")

        self.close()  # Close the checklist window after processing
