from mesa import Model
from mesa.space import MultiGrid
import pandas as pd
from agent import DonorAgent, RecipientAgent, TransportAgent

class FoodDeliveryModel(Model):
    def __init__(self, num_donors, num_recipients, num_transporters, width, height):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = []
        self.food_data = pd.read_csv("data/cleaned_food_wastage_data.csv")

        self.successful_deliveries = 0
        self.failed_attempts = 0

        self.create_agents(num_donors, num_recipients, num_transporters)

    def create_agents(self, num_donors, num_recipients, num_transporters):
        self.schedule = []

        for i in range(num_donors):
            food_amt = int(self.food_data.iloc[i % len(self.food_data)]["wastage_food_amount"])
            agent = DonorAgent(i, self, food_amt)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))  # Ne pas setter .pos à la main
            self.schedule.append(agent)

        for i in range(num_donors, num_donors + num_recipients):
            agent = RecipientAgent(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            self.schedule.append(agent)

        for i in range(num_donors + num_recipients, num_donors + num_recipients + num_transporters):
            agent = TransportAgent(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            self.schedule.append(agent)

    def step(self):
        for agent in self.schedule:
            agent.step()

    def get_grid_state(self):
        return {
            "cells": [
                {"x": a.pos[0], "y": a.pos[1], "status": type(a).__name__}
                for a in self.schedule
            ]
        }
