import random

class CarRecommendationBot:
    def __init__(self):
        self.cars = [
            {'brand': 'Toyota', 'model': 'Corolla', 'price': 80000, 'owners': 1},
            {'brand': 'Mazda', 'model': '3', 'price': 95000, 'owners': 2},
            {'brand': 'Hyundai', 'model': 'i30', 'price': 85000, 'owners': 1},
            {'brand': 'Honda', 'model': 'Civic', 'price': 120000, 'owners': 3},
            {'brand': 'Ford', 'model': 'Focus', 'price': 90000, 'owners': 2},
            {'brand': 'Volkswagen', 'model': 'Golf', 'price': 110000, 'owners': 1}
        ]

    def recommend_cars(self, budget, owners, brand):
        recommendations = []
        for car in self.cars:
            if car['price'] <= budget and car['owners'] <= owners:
                if brand.lower() in car['brand'].lower():
                    recommendations.append(car)
                    if len(recommendations) == 3:
                        break
        return recommendations

    def start_chat(self):
        print("Welcome to the Car Recommendation Bot!")
        budget = int(input("Please enter your budget in NIS: "))
        owners = int(input("Please enter the maximum number of previous owners: "))
        brand = input("Please enter the car brand you prefer (or leave empty for any): ")

        suggestions = self.recommend_cars(budget, owners, brand)

        if suggestions:
            print("Here are your recommendations:")
            for suggestion in suggestions:
                print(f"{suggestion['brand']} {suggestion['model']} - {suggestion['price']} NIS")
        else:
            print("Sorry, we couldn't find any cars matching your criteria.")

if __name__ == '__main__':
    bot = CarRecommendationBot()
    bot.start_chat()