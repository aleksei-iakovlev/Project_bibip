from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
import os


class CarService:

    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        os.makedirs(root_directory_path, exist_ok=True)

    RECORD_SIZE = 500
    DATA_SIZE = RECORD_SIZE - 2 #(для учета \n)

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        
        line_number = 0

        with open(f"{self.root_directory_path}/models.txt", "a") as f:
            f.seek(line_number * (self.RECORD_SIZE))
            f.write(model.model_dump_json().ljust(self.DATA_SIZE) + "\n")

        with open(f"{self.root_directory_path}/models_index.txt", "a") as f:
            f.seek(line_number * (self.RECORD_SIZE))
            f.write(model.index().ljust(self.DATA_SIZE) + "\n")

        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:

        line_number = 0
    
        with open(f"{self.root_directory_path}/cars.txt", "a") as f:
            f.seek(line_number * (self.RECORD_SIZE))
            f.write(car.model_dump_json().ljust(self.DATA_SIZE) + "\n")

        with open(f"{self.root_directory_path}/cars_index.txt", "a") as f:
            f.seek(line_number * (self.RECORD_SIZE))
            f.write(car.index().ljust(self.DATA_SIZE) + "\n")

        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:

        line_number = 0

        with open(f"{self.root_directory_path}/sales.txt", "a") as f:
            f.seek(line_number * (self.RECORD_SIZE))
            f.write(sale.model_dump_json().ljust(self.DATA_SIZE) + "\n")

        with open(f"{self.root_directory_path}/sales_index.txt", "a") as f:
            f.seek(line_number * (self.RECORD_SIZE))
            f.write(sale.index().ljust(self.DATA_SIZE) + "\n")
        
        with open(f"{self.root_directory_path}/cars_index.txt", "r+") as f:
            line_number = -1
            for i, line in enumerate(f):
                if sale.car_vin in line:
                    line_number = i
                    break

        with open(f"{self.root_directory_path}/cars.txt", "r+") as f:

            f.seek(line_number * (self.RECORD_SIZE))
            line = f.read(self.DATA_SIZE)
            car = Car.model_validate_json(line)
            car.status = CarStatus.sold

            f.seek(line_number * (self.RECORD_SIZE))
            f.write(car.model_dump_json().ljust(self.DATA_SIZE) + "\n")

        return car

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:

        res = []
        car = None
        with open(f"{self.root_directory_path}/cars.txt", "r") as f:
            for line in f:
                c = Car.model_validate_json(line)
                if c.status == status:
                    car = c
                    res.append(car)
            return res

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:

        car = None
        model = None

        with open(f"{self.root_directory_path}/cars.txt", "r+") as f:
            for line in f:
                c = Car.model_validate_json(line)
                if vin == c.vin:
                    car = c
                    break

        if car is not None:
                
            with open(f"{self.root_directory_path}/models.txt", "r+") as f:
                for line in f:
                    m = Model.model_validate_json(line)
                    if m.id == car.model:
                        model = m
                        break
        
            if car.status == CarStatus.sold:
                try:
                    sale = None
                    with open(f"{self.root_directory_path}/sales.txt", "r+") as f:
                        for line in f:
                            s = Sale.model_validate_json(line)
                            if vin == s.car_vin:
                                sale = s
                                break
                    car_full_info = CarFullInfo(
                        vin=car.vin,
                        car_model_name=model.name,
                        car_model_brand=model.brand,
                        price=car.price,
                        date_start=car.date_start,
                        status=car.status,
                        sales_date=sale.sales_date,
                        sales_cost=sale.cost
                    )
                except FileNotFoundError:
                    return None
                
            else:
                car_full_info = CarFullInfo(
                    vin=car.vin,
                    car_model_name=model.name,
                    car_model_brand=model.brand,
                    price=car.price,
                    date_start=car.date_start,
                    status=car.status,
                    sales_date=None,
                    sales_cost=None
                )

            return car_full_info

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:

        with open(f"{self.root_directory_path}/cars_index.txt", "r", encoding="utf-8") as f:
            line_number = -1
            for i, line in enumerate(f):
                if vin in line.strip():
                    line_number = i
                    break

        with open(f"{self.root_directory_path}/cars.txt", "r+") as f:

            f.seek(line_number * (self.RECORD_SIZE))
            line = f.readline().strip()
            car = Car.model_validate_json(line)
            car.vin = new_vin

            f.seek(line_number * (self.RECORD_SIZE))
            f.write(car.model_dump_json().ljust(self.DATA_SIZE) + "\n")

        with open(f"{self.root_directory_path}/cars_index.txt", "r+") as f:

            f.seek(line_number * (self.RECORD_SIZE))
            f.write(car.index().ljust(self.DATA_SIZE) + "\n")

        return car
        

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        
        with open(f"{self.root_directory_path}/sales.txt", "r+") as f:
            
            for i, line in enumerate(f):

                sale = Sale.model_validate_json(line)

                if sales_number == sale.sales_number:
                    sale_line_number = i
        
        with open(f"{self.root_directory_path}/cars_index.txt", "r+") as f:
            
            car_line_number = -1
            for i, line in enumerate(f):
                if sale.car_vin in line.strip():
                    car_line_number = i
                    break
        
        with open(f"{self.root_directory_path}/cars.txt", "r+") as f:

            f.seek(car_line_number * (self.RECORD_SIZE))
            line = f.readline().strip()
            car = Car.model_validate_json(line)
            car.status = CarStatus.available

            f.seek(car_line_number * (self.RECORD_SIZE))
            f.write(car.model_dump_json().ljust(self.DATA_SIZE) + "\n")

        with open(f"{self.root_directory_path}/sales.txt", "r+") as f:

            f.seek(sale_line_number * (self.RECORD_SIZE))
            f.write("")
            f.truncate()

        with open(f"{self.root_directory_path}/sales_index.txt", "r+") as f:

            f.seek(sale_line_number * (self.RECORD_SIZE))
            f.write("")
            f.truncate()

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        
        with open(f"{self.root_directory_path}/models_index.txt", "r") as f:
            lis = []
            for j in f:
                lis.append(int(j.strip()))
            models_sales = dict.fromkeys(lis, 0)
        
        with open(f"{self.root_directory_path}/sales.txt", "r") as f:
            
            for y in f:

                sale = Sale.model_validate_json(y)
                
                with open(f"{self.root_directory_path}/cars_index.txt", "r+") as f:
                    line_number = -1
                    for i, line in enumerate(f):
                        if sale.car_vin in line:
                            line_number = i
                            break

                with open(f"{self.root_directory_path}/cars.txt", "r") as f:

                    f.seek(line_number * (self.RECORD_SIZE))
                    car_line = f.read(self.DATA_SIZE)
                    car = Car.model_validate_json(car_line)

                count = dict.pop(models_sales, car.model)
                models_sales[car.model] = count + 1
        
        sorted_models_sales = dict(sorted(models_sales.items(), key=lambda item: item[1], reverse=True))
        top_list = list(dict.keys(sorted_models_sales))

        with open(f"{self.root_directory_path}/models_index.txt", "r") as f:

            top_1_line_number = -1
            top_2_line_number = -1
            top_3_line_number = -1

            for i, line in enumerate(f):
                if top_list[0] == int(line):
                    top_1_line_number = i
                    continue
                if top_list[1] == int(line):
                    top_2_line_number = i
                    continue
                if top_list[2] == int(line):
                    top_3_line_number = i
                    continue

        with open(f"{self.root_directory_path}/models.txt", "r") as f:

            f.seek(top_1_line_number * (self.RECORD_SIZE))
            line = f.read(self.DATA_SIZE)
            top_1_model = Model.model_validate_json(line)

            top_1 = ModelSaleStats(
                car_model_name=top_1_model.name,
                brand=top_1_model.brand,
                sales_number=sorted_models_sales[top_list[0]]
            )

            f.seek(top_2_line_number * (self.RECORD_SIZE))
            line = f.read(self.DATA_SIZE)
            top_2_model = Model.model_validate_json(line)

            top_2 = ModelSaleStats(
                car_model_name=top_2_model.name,
                brand=top_2_model.brand,
                sales_number=sorted_models_sales[top_list[1]]
            )

            f.seek(top_3_line_number * (self.RECORD_SIZE))
            line = f.read(self.DATA_SIZE)
            top_3_model = Model.model_validate_json(line)

            top_3 = ModelSaleStats(
                car_model_name=top_3_model.name,
                brand=top_3_model.brand,
                sales_number=sorted_models_sales[top_list[2]]
            )
            
        res = [top_1, top_2, top_3]

        return res

