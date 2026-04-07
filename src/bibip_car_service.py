from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
import os


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        os.makedirs(root_directory_path, exist_ok=True)

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        with open(f"{self.root_directory_path}/models.txt", "a+") as f:
            data = f"{model.id};{model.name};{model.brand}".ljust(98) + "\n"
            f.write(data)
        with open(f"{self.root_directory_path}/models_index.txt", "a+") as f:
            data = f"{model.id}".ljust(98) + "\n"
            f.write(data)

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        with open(f"{self.root_directory_path}/cars.txt", "a+") as f:
            data = f"{car.vin};{car.model};{car.price};{car.date_start};{car.status}".ljust(98) + "\n"
            f.write(data)
        with open(f"{self.root_directory_path}/cars_index.txt", "a+") as f:
            data = f"{car.vin}".ljust(98) + "\n"
            f.write(data)

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        with open(f"{self.root_directory_path}/sales.txt", "a+") as f:
            data = f"{sale.sales_number};{sale.car_vin};{sale.sales_date};{sale.cost}".ljust(98) + "\n"
            f.write(data)
        with open(f"{self.root_directory_path}/sales_index.txt", "a+") as f:
            data = f"{sale.sales_number};{sale.car_vin}".ljust(98) + "\n"
            f.write(data)

            index_list = os.readlines(f"{self.root_directory_path}/sales_index.txt")
            index_vin_car = index_list.index(sale.car_vin)

        with open(f"{self.root_directory_path}/car.txt", "r+") as f:
            f.seek(index_vin_car * 100)
            data = f"{car.vin};{car.model};{car.price};{car.date_start};{car.status}".ljust(98) + "\n"
            f.write(data)




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
