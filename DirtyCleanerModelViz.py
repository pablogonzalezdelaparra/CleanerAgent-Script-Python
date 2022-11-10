"""
This programs helps to visualize the mulitagente model of
a cleaner robot in the broswer.

José Ángel García Gómez | A01745865
Pablo González de la Parra | A01745096

Created: 4 / 11 / 2022
"""
from DirtyCleanerModel import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agentPortrayal(agent):
    """
    Objective: Helps to visualize agents in the grid
    Parameters: agent -> Type of agent
    Return value: portrayal -> Style that agent should have
    """
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    return portrayal


# Initial variables
WIDTH = 30
HEIGHT = 30
PERCENTAGE_DIRTY_CELLS = 50
NUM_AGENTS = 10

# System definition
grid = CanvasGrid(agentPortrayal, WIDTH, HEIGHT, 750, 750)
server = ModularServer(DirtyCleanerModel,
                       [grid],
                       "Dirty Cleaner Model",
                       {"width": WIDTH,
                        "height": HEIGHT,
                        "percentageDirtyCells": PERCENTAGE_DIRTY_CELLS,
                        "numAgents": NUM_AGENTS})
server.port = 8521  # Default port
server.launch()
