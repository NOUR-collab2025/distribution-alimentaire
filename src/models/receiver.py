class Receiver:
    def __init__(self, name):
        self.name = name
        self.stock = []

    def receive(self, food_item, env):
        self.stock.append(food_item)
        print(f"[t={env.now}] {self.name} reçoit {food_item.quantity}x {food_item.name}")
