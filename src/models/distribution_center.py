class DistributionCenter:
    def __init__(self, id, name, location, capacity, current_stock):
        self.id = id
        self.name = name
        self.location = location
        self.capacity = capacity
        self.current_stock = current_stock

    def __str__(self):
        return f"DistributionCenter({self.name}, stock: {self.current_stock})"
