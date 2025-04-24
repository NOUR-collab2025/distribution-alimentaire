from mesa.visualization import VisualizationElement
from agent import DonorAgent, RecipientAgent, TransportAgent

class GridVisualization(VisualizationElement):
    def __init__(self, model):
        self.model = model
        self.grid = model.grid
        self.canvas_element = self.create_canvas()

    def create_canvas(self):
        """Set up the visualization canvas"""
        canvas = {
            "agent_portrayal": self.agent_portrayal
        }
        return canvas

    def agent_portrayal(self, agent):
        """Define the visual representation of each agent."""
        portrayal = {"Shape": "circle", "r": 1}

        if isinstance(agent, DonorAgent):
            portrayal["Color"] = "blue"
        elif isinstance(agent, RecipientAgent):
            portrayal["Color"] = "green"
        elif isinstance(agent, TransportAgent):
            portrayal["Color"] = "red"

        return portrayal

    def render(self):
        """Render the grid"""
        for agent in self.model.custom_agents:
            portrayal = self.agent_portrayal(agent)
            print(f"Agent {agent.unique_id} portrayed as: {portrayal['Color']}")
