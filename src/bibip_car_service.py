from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from decimal import Decimal
import os
import json


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        os.makedirs(root_directory_path, exist_ok=True)

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:

        model_data = {
            'id': model.id,
            'name': model.name,
            'brand': model.brand
        }
        with open(f"{self.root_directory_path}/models.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(model_data) + "\n")

        model_index_data = {
            'id': model.id
        }
        with open(f"{self.root_directory_path}/models_index.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(model_index_data) + "\n")

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:

        car_data = {
            'vin': car.vin,
            'model': car.model,
            'price': str(car.price),
            'date_start': str(car.date_start),
            'status': car.status
        }
        with open(f"{self.root_directory_path}/cars.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(car_data) + "\n")
        
        car_index_data = {
            'car_vin': car.vin
        }
        with open(f"{self.root_directory_path}/cars_index.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(car_index_data) + "\n")

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:

        sale_data = {
            'sales_number': sale.sales_number,
            'car_vin': sale.car_vin,
            'sales_date': str(sale.sales_date),
            'cost': str(sale.cost)
        }
        with open(f"{self.root_directory_path}/sales.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(sale_data) + "\n")

        sale_index_data = {
            'sales_number': sale.sales_number
        }
        with open(f"{self.root_directory_path}/sales_index.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(sale_index_data) + "\n")

        with open(f"{self.root_directory_path}/cars_index.txt", "r+", encoding="utf-8") as f:
            lis = f.readlines()
            for i in lis:
                if sale.car_vin in i:
                    return i

        car_data = {
            'status': 'sold'
        }

        with open(f"{self.root_directory_path}/cars.txt", "r+", encoding="utf-8") as f:
            j = 0
            for line in f:
                j += 1
                if j == i:
                    line.write(json.dumps(car_data))

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        raise NotImplementedError

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        raise NotImplementedError

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        raise NotImplementedError

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        raise NotImplementedError

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        raise NotImplementedError
