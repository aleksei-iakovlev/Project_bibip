from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
import os


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        os.makedirs(root_directory_path, exist_ok=True)

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        
        line_number = 0

        with open(f"{self.root_directory_path}/models.txt", "a") as f:
            f.seek(line_number * (500))
            f.write(model.model_dump_json().ljust(498) + "\n")

        with open(f"{self.root_directory_path}/models_index.txt", "a") as f:
            f.seek(line_number * (500))
            f.write(model.index().ljust(498) + "\n")

        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:

        line_number = 0
    
        with open(f"{self.root_directory_path}/cars.txt", "a") as f:
            f.seek(line_number * (500))
            f.write(car.model_dump_json().ljust(498) + "\n")

        with open(f"{self.root_directory_path}/cars_index.txt", "a") as f:
            f.seek(line_number * (500))
            f.write(car.index().ljust(498) + "\n")

        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:

        line_number = 0

        with open(f"{self.root_directory_path}/sales.txt", "a") as f:
            f.seek(line_number * (500))
            f.write(sale.model_dump_json().ljust(498) + "\n")

        with open(f"{self.root_directory_path}/sales_index.txt", "a") as f:
            f.seek(line_number * (500))
            f.write(sale.index().ljust(498) + "\n")
        
        with open(f"{self.root_directory_path}/cars_index.txt", "r+") as f:
            line_number = -1
            for i, line in enumerate(f):
                if sale.car_vin in line:
                    line_number = i
                    break

        with open(f"{self.root_directory_path}/cars.txt", "r+") as f:

            f.seek(line_number * (500))
            line = f.read(498)
            car = Car.model_validate_json(line)
            car.status = CarStatus.sold

            f.seek(line_number * (500))
            f.write(car.model_dump_json().ljust(498) + "\n")

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
                except Exception:
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

            f.seek(line_number * (500))
            line = f.readline().strip()
            car = Car.model_validate_json(line)
            car.vin = new_vin

            f.seek(line_number * (500))
            f.write(car.model_dump_json().ljust(498) + "\n")

        with open(f"{self.root_directory_path}/cars_index.txt", "r+") as f:

            f.seek(line_number * (500))
            f.write(car.index().ljust(498) + "\n")

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

            f.seek(car_line_number * (500))
            line = f.readline().strip()
            car = Car.model_validate_json(line)
            car.status = CarStatus.available

            f.seek(car_line_number * (500))
            f.write(car.model_dump_json().ljust(498) + "\n")

        with open(f"{self.root_directory_path}/sales.txt", "r+") as f:

            f.seek(sale_line_number * (500))
            f.write("")
            f.truncate()

        with open(f"{self.root_directory_path}/sales_index.txt", "r+") as f:

            f.seek(sale_line_number * (500))
            f.write("")
            f.truncate()

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        raise NotImplementedError

#service = CarService('data')
#sold = CarStatus.sold
#print(service.get_cars(sold))
#print(service.get_car_info("5N1CR2TS0HW037674"))
#res = service.update_vin("KNAGM4A77D5316538", "UPDGM4A77D5316538")
#print(res)
