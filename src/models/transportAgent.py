class TransportAgent:
    def __init__(self, id, name, vehicle_type, capacity, availability):
        self.id = id
        self.name = name
        self.vehicle_type = vehicle_type
        self.capacity = capacity
        self.availability = availability

    def __str__(self):
        return f"TransportAgent({self.name}, vehicle: {self.vehicle_type})"
