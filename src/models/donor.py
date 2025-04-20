class Donor:
    def __init__(self, id, name, location, contact_info):
        self.id = id
        self.name = name
        self.location = location
        self.contact_info = contact_info

    def __str__(self):
        return f"Donor({self.name})"
