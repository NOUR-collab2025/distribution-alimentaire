class FoodItem:
    def __init__(self, id, name, quantity, expiration_date, category, donor_id):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.expiration_date = expiration_date
        self.category = category
        self.donor_id = donor_id

    def __str__(self):
        return f"FoodItem({self.name}, {self.quantity}kg, expires: {self.expiration_date})"
