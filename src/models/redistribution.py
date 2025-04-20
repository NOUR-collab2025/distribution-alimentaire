class Redistribution:
    def __init__(self, id, food_item_id, recipient_id, transport_agent_id, date, status):
        self.id = id
        self.food_item_id = food_item_id
        self.recipient_id = recipient_id
        self.transport_agent_id = transport_agent_id
        self.date = date
        self.status = status

    def __str__(self):
        return f"Redistribution({self.id}, status: {self.status})"
