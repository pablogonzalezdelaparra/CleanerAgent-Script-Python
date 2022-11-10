"""
This programs helps to analize the result from running
the multiagent system of a cleaner robot, as well as
storing these graphs in the same folder

José Ángel García Gómez | A01745865
Pablo González de la Parra | A01745096

Created: 4 / 11 / 2022
"""
from DirtyCleanerModel import *
import matplotlib.pyplot as plt

# Initial variables
WIDTH = 30
HEIGHT = 30
PERCENTAGE_DIRTY_CELLS = 50
NUM_AGENTS = [100, 150, 200]
MAX_STEPS = 2000

# Calling the model [numAgents] amount of times
for agent in NUM_AGENTS:
    model = DirtyCleanerModel(WIDTH, HEIGHT, PERCENTAGE_DIRTY_CELLS, agent)

    for _ in range(MAX_STEPS):
        model.step()

    # Get dirty cells from model
    dirtyCellsLeft = model.datacollector.get_model_vars_dataframe()

    # Calculate the percentage of clean cells left after run
    percentageCleanCells = int((((WIDTH * HEIGHT) - model.dirtyCells)
                                * 100) / (WIDTH * HEIGHT))

    # Get agent moves (steps)
    agentMoves = model.datacollector.get_agent_vars_dataframe()

    # Calculate moves for each agent
    allAgentMoves = agentMoves.xs(model.numSteps - 1, level="Step")

    # Plot dirty cells over time
    dirtyCellsLeft.plot()
    plt.title("Number of dirty cells over time")
    plt.xlabel("Time (Steps)")
    plt.ylabel("Number of dirty cells")
    plt.savefig(f'{agent}ag50.png')

    # Plot total agents moves
    allAgentMoves.plot(kind="bar")
    plt.title("Agents total moves")
    plt.ylabel("Moves (steps)")
    plt.xlabel("Agent ID")
    plt.savefig(f'{agent}ag50Bar.png')

    # Print statistics
    print(f"-----Datos iniciales-----")
    print(f"Habitación de : {WIDTH} * {HEIGHT} espacios")
    print(f"Número de celdas totales: {WIDTH * HEIGHT}")
    print(f"Número de agentes: {agent}")
    print(f"Porcentaje de celdas sucias: {PERCENTAGE_DIRTY_CELLS}%")
    print(f"Tiempo máximo: {MAX_STEPS} steps")
    print(f"-----Datos finales-----")
    print(f"Tiempo recorrido: {model.numSteps} steps")
    print(f"Porcentaje de celdas limpias: {percentageCleanCells}%")
