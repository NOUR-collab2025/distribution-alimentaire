class Recipient:
    def __init__(self, id, name, location, contact_info, capacity, priority_level):
        self.id = id
        self.name = name
        self.location = location
        self.contact_info = contact_info
        self.capacity = capacity
        self.priority_level = priority_level

    def __str__(self):
        return f"Recipient({self.name}, priority: {self.priority_level})"
