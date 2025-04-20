class FoodItem:
    def __init__(self, name, quantity, expiration_day):
        self.name = name
        self.quantity = quantity
        self.expiration_day = expiration_day

    def is_expired(self, current_day):
        return current_day > self.expiration_day