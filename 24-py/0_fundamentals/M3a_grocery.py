###################################################################
# Implementation of Code in this section
# Hint: round(float, 2) will return a float with 2 d.p.
# Hint: "{:>12.2f}".format(float) will format float in 12 blank
#        placeholders, align to the right, formatted to 2 d.p.
###################################################################

# Your code here

# Final price modifiers const
TAX_GST: float = 1.07
TAX_CIGARETTE: float = 1.60
TAX_WINE: float = 1.50
TAX_BEER: float = 1.20
ENERGY_THRESHOLD: float = 10.0
ENERGY_PROMO: float = 0.80

class Grocery:
    def __init__(self, title, cost, price, stock):
        self._title: str = title
        self._cost: float = cost
        self._price: float = price
        self._stock: int = stock
    
    # Setters
    def set_title(self, new_title: str):
        self._title = new_title
    def set_cost(self, new_cost: float):
        self._cost = new_cost
    def set_price(self, new_price: float):
        self._price = new_price

    # Getters
    def get_title(self) -> str:
        return self._title
    def get_cost(self) -> float:
        return self._cost
    def get_price(self) -> float:
        return self._price
    def get_stock(self) -> int:
        return self._stock
    
    # Str
    def __str__(self) -> str:
        return "{:<20} | ${:>6.2f} | ${:>6.2f} | {:>6} | ${:>12.2f}".format(
            self.get_title(),
            self.get_cost(),
            self.get_price(),
            self.get_stock(),
            self.calculate_final_price()
        )

    def update_stock(self, change_in_stock: int):
        # Defaults to deducting stock 
        self._stock -= change_in_stock

    def calculate_final_price(self) -> float:
        price = self.get_price() * TAX_GST
        return round(price, 2)
    

class ElectricalAppliance(Grocery):
    def __init__(self, title, cost, price, stock, power):
        super().__init__(title, cost, price, stock)
        self._power: int = power

    def get_power(self) -> float:
        return self._power
    
    def calculate_final_price(self) -> float:
        price = self.get_price() * TAX_GST
        if self.get_power() <= ENERGY_THRESHOLD: price *= ENERGY_PROMO
        return round(price, 2)


class Cigarette(Grocery):
    def __init__(self, title, cost, price, stock, nicotine_content):
        super().__init__(title, cost, price, stock)
        self._nicotine_content: float = nicotine_content
    
    def get_nicotine_content(self) -> float:
        return self._nicotine_content
    
    def calculate_final_price(self) -> float:
        price = self.get_price() * TAX_GST * TAX_CIGARETTE
        return round(price, 2)
    

class Alcohol(Grocery):
    def __init__(self, title, cost, price, stock, type_):
        super().__init__(title, cost, price, stock)
        self._type: str = type_
    
    def get_type(self) -> str:
        return self._type
    
    def calculate_final_price(self) -> float:
        tax = TAX_BEER if self.get_type() == "beer" else TAX_WINE
        price = self.get_price() * TAX_GST * tax
        return round(price, 2)


class StoreManager:
    def __init__(self, curr_list_item):
        self._curr_list_item: list[Grocery] = curr_list_item
    
    def sell_item(self, sold_item: tuple, show_header: bool = True) -> float:
        """Sells an item of any quantity, returns subtotal sold"""
        title, quant = sold_item
        for g in self._curr_list_item:
            if g.get_title() == title:
                g.update_stock(quant)
                break
        
        # Round unit only after subtotal
        unitp: float = g.calculate_final_price()
        subp: float = round(unitp * quant, 2)
        unitp = round(unitp, 2)

        # Within sell_items function, can suppress header
        if show_header:
            print("{:<20} |  {:>10} | {:>15} |  {:>11}".format(
        "Title", "Unit Price", "Quantity Sold", "Final Price"))
        
        print("{:<20} | ${:>10.2f} | {:>15} | ${:>11.2f}".format(title, unitp, quant, subp))

        return subp
    
    
    def sell_items(self, sold_item_list: list[tuple]):
        """Sells items in a transaction"""
        ttl: float = 0
        for idx, g in enumerate(sold_item_list):
            ttl += self.sell_item(g, show_header=bool(idx == 0))
        print("{:<20} |  {:>10} | {:>15} | ${:>11.2f}".format("", "", "GRAND TOTAL", ttl))

    
    def stock_check(self):
        """Prints stocks that run 5 or below in quant"""
        print("{:<20} | ${:>10} | {:>15}".format("Title", "Unit Cost", "Quantity Left"))
        needs_stock: bool = False
        for g in self._curr_list_item:
            if g.get_stock() <= 5:
                print("{:<20} | ${:>10.2f} | {:>15}".format(g.get_title(), g.calculate_final_price(), g.get_stock()))
                needs_stock = True
        if not needs_stock:
            print("ALL GOOD!")


####################################################
# Please do not modify the code below
####################################################


def initialise_data():
    g1 = Grocery("Spoon", 1.5, 2.5, 15)
    g2 = Grocery("Fork", 1.7, 3.0, 5)
    g3 = Grocery("Shampoo", 5.2, 11, 11)
    g4 = Grocery("Power Cable", 6.5, 15, 12)

    ea1 = ElectricalAppliance("Normal Light Bulb 01", 2, 3, 3, 25)
    ea2 = ElectricalAppliance("Normal Light Bulb 02", 2.5, 4, 6, 30)
    ea3 = ElectricalAppliance("LED Light Bulb", 6, 10, 9, 5)
    ea4 = ElectricalAppliance("Desk Light", 30, 50, 2, 50)
    ea5 = ElectricalAppliance("LED Desk Light", 40, 60, 15, 10)

    c1 = Cigarette("Marlboro Red", 27.65, 35, 15, 0.7)
    c2 = Cigarette("Bomond Blue", 12.10, 15, 12, 0.7)
    c3 = Cigarette("Camel Filters", 23.38, 30, 23, 0.6)
    c4 = Cigarette("Yun Yan", 16.5, 23, 4, 0.65)

    a1 = Alcohol("Barefoot", 55, 86, 3, "wine")
    a2 = Alcohol("Great Wall", 45, 80, 5, "wine")
    a3 = Alcohol("Hardys", 57, 90, 6, "wine")
    a4 = Alcohol("Coors Light", 15, 27, 13, "beer")
    a5 = Alcohol("Tsingtao", 10, 20, 7, "beer")

    return [g1, g2, g3, g4, ea1, ea2, ea3, ea4, ea5, c1, c2, c3, c4, a1, a2, a3, a4, a5]


g_list = initialise_data()


def test_function_5_1():
    print("Begin test function 5.1\n")

    print("{:-^65}".format("Current Grocery List"))
    print("{:<20} |  {:>6} |  {:>6} | {:>6} |  {:>12}".format(
        "Title", "Cost", "Price", "Stock", "Final Price"))
    print("{:-^65}".format(""))

    for g in g_list:
        print(g)

    print("\nEnd of test function 5.1\n")


test_function_5_1()


def test_function_5_2():
    print("Begin test function 5.2\n")

    sm = StoreManager(g_list)
    sold_item_list = [("Spoon", 2), ("Fork", 3)]
    sm.sell_items(sold_item_list)

    print()
    sm.stock_check()

    print("\nEnd of test function 5.2\n")


test_function_5_2()
