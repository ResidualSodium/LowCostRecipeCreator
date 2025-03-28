import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from gui.checklist_gui import ChecklistGUI  # Import the ChecklistGUI class
from scraping.recipe_scraper import ScrapeRecipe  # Import the ScrapeRecipe class

class RecipeScraperGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Recipe Scraper')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.instruction_label = QLabel('Enter Recipe URL:')
        layout.addWidget(self.instruction_label)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('Paste recipe URL here')
        layout.addWidget(self.url_input)

        self.scrape_button = QPushButton('Scrape Recipe', self)
        self.scrape_button.clicked.connect(self.on_scrape_button_click)
        layout.addWidget(self.scrape_button)

        self.feedback_label = QLabel('')
        layout.addWidget(self.feedback_label)

        self.setLayout(layout)

    def on_scrape_button_click(self):
        url = self.url_input.text()

        if url:
            self.scrape_recipe(url)
        else:
            self.feedback_label.setText('Please enter a valid URL.')

    def scrape_recipe(self, url):
        scraper = ScrapeRecipe(url)  # Create an instance of ScrapeRecipe class, not the module
        recipe = scraper.get_recipe()  # Get the scraped recipe

        if recipe:
            # Extract ingredients and pass them to ChecklistGUI
            ingredients = recipe.get("ingredients", [])
            print(f"Ingredients: {ingredients}")  # Debugging
            self.open_checklist_gui(ingredients)
        else:
            self.feedback_label.setText('Failed to scrape the recipe.')

    def open_checklist_gui(self, ingredients):
        # Ensure ChecklistGUI is opened correctly
        try:
            checklist_window = ChecklistGUI(ingredients)
            checklist_window.exec()  # Make sure the window blocks execution until closed
        except Exception as e:
            print(f"Error opening checklist GUI: {e}")

# Main function to run the application
def main():
    try:
        app = QApplication(sys.argv)
        window = RecipeScraperGUI()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error encountered in main GUI: {e}")

if __name__ == "__main__":
    main()
