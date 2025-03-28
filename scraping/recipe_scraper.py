import recipe_scrapers
from urllib.request import urlopen

class ScrapeRecipe:
    def __init__(self, url):
        self.url = url
        self.recipe = None
        self.scrape_recipe()

    def scrape_recipe(self):
        try:
            # Retrieve HTML content from the URL
            html = urlopen(self.url).read().decode("utf-8")

            # Use scrape_html() with the retrieved HTML content
            scraper = recipe_scrapers.scrape_html(html, org_url=self.url)

            # Extract and store recipe information
            ingredients = scraper.ingredients() or []
            # Fixing common ingredient name errors
            ingredients = [ingredient.replace("ijon", "Dijon").replace("orcestershire", "Worcestershire") for ingredient in ingredients]

            self.recipe = {
                "title": scraper.title() or "No title available",
                "instructions": scraper.instructions() or "No instructions available",
                "ingredients": ingredients,
                "nutrients": scraper.nutrients() or "No nutrients data available"
            }
        except Exception as e:
            print(f"Error encountered in ScrapeRecipe for URL {self.url}: {e}")
            self.recipe = None  # Ensure `recipe` is None if there's an error

    def get_recipe(self):
        return self.recipe

# Test independently
if __name__ == "__main__":
    url = "https://www.allrecipes.com/recipe/45410/party-beans/"
    scraper = ScrapeRecipe(url)
    print(scraper.get_recipe())
