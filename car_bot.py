import requests

class CarSelectionBot:
    def __init__(self, budget, owner_count, brand):
        self.budget = budget
        self.owner_count = owner_count
        self.brand = brand
        self.urls = {
            'auto.ru': 'https://auto.ru/cars/',
            'drom.ru': 'https://www.drom.ru/',
            'avvo.ru': 'https://avto.ru/'
        }

    def get_car_links(self):
        # This method would ideally use an API or scrape data to find cars
        # For now, it returns linked sources based on the provided criteria
        print(f"Searching for {self.brand} cars in the price range {self.budget} with {self.owner_count} owners...")
        return self.urls

    def display_links(self):
        links = self.get_car_links()
        for site, url in links.items():
            print(f"Check {site} for cars: {url}")

# Example usage
if __name__ == "__main__":
    budget = int(input("Enter your budget: "))
    owner_count = int(input("Enter number of owners (0 for new): "))
    brand = input("Enter car brand: ")
    car_bot = CarSelectionBot(budget, owner_count, brand)
    car_bot.display_links()