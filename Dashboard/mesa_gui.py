from mesa import Agent, Model  
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from src.models import fooditem  # Assurez-vous d'importer votre modèle ici
from src.models import donor
from src.models import recipient

def agent_portrayal(agent):
    # Cette fonction définira la manière dont les agents seront visualisés
    if isinstance(agent, donor):
        portrayal = {"Shape": "circle", "r": 1, "Color": "green", "Layer": 1}
    elif isinstance(agent, recipient):
        portrayal = {"Shape": "circle", "r": 1, "Color": "blue", "Layer": 2}
    return portrayal

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)  # Dimensions de la grille
chart_element = ChartModule([("Food Delivered", "line")])

server = ModularServer(
    fooditem,
    [grid, chart_element],
    "Food Redistribution Model",
    {"N": 50, "width": 20, "height": 20}
)
server.launch()
