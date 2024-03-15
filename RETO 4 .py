class MenuItem:
    def __init__(self, name, price):
        self._name = name
        self._price = price

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_price(self):
        return self._price

    def set_price(self, price):
        self._price = price

    def calculate_total_price(self, quantity):
        return self._price * quantity, 0  # No discount for general menu items

class Beverage(MenuItem):
    def __init__(self, name, price, size):
        super().__init__(name, price)
        self._size = size

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

    def calculate_total_price(self, quantity):
        discount = 0
        if self.order.includes_main_course():
            discount = 0.1 * self._price * quantity  # Apply discount for beverages if order includes main course
        total_price = self._price * quantity - discount
        return total_price, discount

class Appetizer(MenuItem):
    pass


class MainCourse(MenuItem):
    pass


class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity):
        self.items.append((item, quantity))
        item.order = self  # Assign the order to the item
    
    def includes_main_course(self):
        return any(isinstance(item, MainCourse) for item, quantity in self.items)

    def print_order(self):
        print("Order:")
        for item, quantity in self.items:
            total_price, discount = item.calculate_total_price(quantity)
            print(f"{item.get_name()} x {quantity} - Total: {total_price}, Descuento: {discount}")

class Bill:
    def __init__(self, order):
        self.order = order

    def calculate_total(self):
        total_bill = 0
        for item, quantity in self.order.items:
            total_price, discount = item.calculate_total_price(quantity)
            total_bill += total_price
        return total_bill

    def print_bill(self):
        print("Order:")
        for item, quantity in self.order.items:
            total_price, discount = item.calculate_total_price(quantity)
            print(f"{item.get_name()} x {quantity} - Total: {total_price}, Descuento: {discount}")
        print("Total a pagar:", self.calculate_total())


class MedioPago:
    def __init__(self):
        pass

    def pagar(self, monto):
        raise NotImplementedError("Subclases deben implementar pagar()")

class Tarjeta(MedioPago):
    def __init__(self, numero, cvv):
        super().__init__()
        self.numero = numero
        self.cvv = cvv

    def pagar(self, monto):
        print(f"Pagando {monto} con tarjeta {self.numero[-4:]}")
        return 0  # La tarjeta puede pagar cualquier monto


class Efectivo(MedioPago):
    def __init__(self, monto_entregado):
        super().__init__()
        self.monto_entregado = monto_entregado
        self.monto_pagado = 0  # Agrega esta línea

    def pagar(self, monto):
        if self.monto_entregado >= monto:
            print(f"Pago realizado en efectivo. Cambio: {self.monto_entregado - monto}")
            self.monto_pagado = monto  # Actualiza el monto pagado
            return 0
        else:
            print(f"Fondos insuficientes. Faltan {monto - self.monto_entregado} para completar el pago.")
            self.monto_pagado = self.monto_entregado  # Actualiza el monto pagado con lo que se tenía en efectivo
            return monto - self.monto_entregado  # Devuelve el monto restante

menu = {
    "Vino": Beverage("Vino", 65000, "botella"),
    "Agua": Beverage("Agua", 3000, "botella"),
    "Cerveza": Beverage("Cerveza", 10000, "botella"),
    "Papas": Appetizer("Papas", 13000),
    "Alitas": Appetizer("Alitas", 25000),
    "Churazco": MainCourse("Churazco", 45000),
    "Reve eye": MainCourse("Reve eye", 65000),
    "Salmon": MainCourse("Salmon", 55000),
    "Pasta Carbonara": MainCourse("Pasta Carbonara", 35000),
    "Pasta Bolognesa": MainCourse("Pasta Bolognesa", 35000),
}

order = Order()
order.add_item(menu["Vino"], 1)
order.add_item(menu["Alitas"], 1)
order.add_item(menu["Churazco"], 1)
order.add_item(menu["Reve eye"], 1)

bill = Bill(order)
bill.print_bill()
# pago con tarjeta
total_a_pagar = bill.calculate_total()

# Pago en efectivo
efectivo = Efectivo(70000)  # Monto entregado
total_a_pagar = efectivo.pagar(total_a_pagar)
print(f"Valor pagado en efectivo: {efectivo.monto_pagado}")

# Si el efectivo no fue suficiente, paga el resto con tarjeta
if total_a_pagar > 0:
    tarjeta = Tarjeta("1234567890123456", 123)
    total_a_pagar = tarjeta.pagar(total_a_pagar)