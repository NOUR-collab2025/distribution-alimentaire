from mesa import Agent  # this is still the right import in stable 3.x
from math import dist  # or use your own if using Python <3.8
class DonorAgent(Agent):
    def __init__(self, unique_id, model,food_amt):
        self.unique_id = unique_id
        self.model = model
        self.food = food_amt  # Will be set by model
        self.delivered = False
        self.pos = None  # à ajouter dans chaque classe d'agent

        if hasattr(model, "register_agent"):
            model.register_agent(self)

    def step(self):
        # Example: reduce food over time
        if self.food > 0:
            self.food -= 1

class RecipientAgent(Agent):
    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.model = model
        self.food = 0
        self.pos = None  # à ajouter dans chaque classe d'agent

        if hasattr(model, "register_agent"):
            model.register_agent(self)

    def step(self):
        pass


class TransportAgent(Agent):
    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.model = model
        self.food = 0
        self.pos = None  # à ajouter dans chaque classe d'agent

        if hasattr(model, "register_agent"):
            model.register_agent(self)

    def step(self):
        if self.food == 0:
            # Seek donor with food (optimize by food amount minus distance)
            donors = [a for a in self.model.schedule if isinstance(a, DonorAgent) and a.food > 0]
            if donors:
                closest = max(donors, key=lambda d: d.food - dist(self.pos, d.pos))
                self.move_toward(closest.pos)

                if self.pos == closest.pos:
                    self.food = 1
                    closest.food -= 1
            else:
                self.model.failed_attempts += 1

        else:
            # Seek recipient (optimize by distance)
            recipients = [a for a in self.model.schedule if isinstance(a, RecipientAgent)]
            if recipients:
                closest = min(recipients, key=lambda r: dist(self.pos, r.pos))
                self.move_toward(closest.pos)

                if self.pos == closest.pos:
                    self.food = 0
                    closest.food += 1
                    self.model.successful_deliveries += 1
            else:
                self.model.failed_attempts += 1

    def move_toward(self, target_pos):
        dx = int((target_pos[0] - self.pos[0]) / max(abs(target_pos[0] - self.pos[0]), 1))
        dy = int((target_pos[1] - self.pos[1]) / max(abs(target_pos[1] - self.pos[1]), 1))
        new_pos = (self.pos[0] + dx, self.pos[1] + dy)
        self.model.grid.move_agent(self, new_pos)
        self.pos = new_pos