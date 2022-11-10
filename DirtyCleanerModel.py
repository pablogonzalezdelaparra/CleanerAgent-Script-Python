"""
This programs implements the logic of not only the agents, but also the
model of a multiagente system of a cleaner robot trying to clean all the
dirty cells in a grid.

José Ángel García Gómez | A01745865
Pablo González de la Parra | A01745096

Created: 4 / 11 / 2022
"""
from mesa import Agent, Model, DataCollector
from mesa.space import MultiGrid
from mesa.time import StagedActivation


# Return number of dirty cells
def getDirtyCells(model):
    """
    Objective: Returns the amount of dirty cells in the grid
    Parameters: model -> Model of the multiagent system
    Return value: dirtyCells -> How many cells are currently left
    """
    return model.dirtyCells


# Cleaner agent (Vacuum)
class CleanerAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.nextState = None
        self.moves = 0

    # If cell is dirty, clean it (delete it from dic)
    def isCellDirty(self, agentPosition):
        """
        Objective: Checks if a certain cell is dirty
        Parameters: agentPosition -> Coordinate of cleaner agent
        Return value: Bool -> If a cell is dirty, return True
        """
        if agentPosition in self.model.dirtyCellsDic:
            del self.model.dirtyCellsDic[agentPosition]
            self.model.dirtyCells -= 1
            return True
        return False

    # Move agent if chosen cell is available
    def moveAgent(self, possibleStep):
        """
        Objective: Moves an agent to another cell on the grid
        Parameters: possibleStep -> Cell where agent should move to
        Return value: None
        """
        self.nextState = possibleStep
        self.model.grid.move_agent(self, self.nextState)
        self.moves += 1

    # Don't move agent if chosen cell is occupied
    def notMoveAgent(self):
        """
        Objective: Moves agent to current position (static)
        Parameters: None
        Return value: None
        """
        self.nextState = self.pos

    def step(self):
        """
        Objective: Contains the logic of each step from cleaner agent
        Parameters: None
        Return value: None
        """
        allowedToMove = False

        # Check if current cell is dirty
        if not self.isCellDirty(self.pos):
            # Get all neighbors from agent
            possibleSteps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False)
            # Choose one cell to try and move to
            possibleStep = self.random.choice(possibleSteps)
            # Check if possible step is not out of bounds
            if not self.model.grid.out_of_bounds(possibleStep):
                # Check content of possible step cell
                cellContent = self.model.grid.get_cell_list_contents(
                    possibleStep)
                # If there isn't another agent, move there
                if not cellContent:
                    allowedToMove = True
        if allowedToMove:
            self.moveAgent(possibleStep)
        else:
            self.notMoveAgent()

    def advance(self):
        """
        Objective: Executes in each step of the current model
        Parameters: None
        Return value: None
        """
        self.model.grid.move_agent(self, self.nextState)


class DirtyCleanerModel(Model):
    def __init__(self, width, height, percentageDirtyCells, numAgents):
        self.grid = MultiGrid(width, height, False)
        # Get number from percentage of dirty cells
        self.dirtyCells = int(((width * height) *
                              percentageDirtyCells) / 100)
        self.dirtyCellsDic = {}
        self.numSteps = 0
        self.schedule = StagedActivation(self)
        self.running = True  # Para la visualizacion usando navegador

        # Create dirty cells
        count = 0
        while count < self.dirtyCells:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            if (x, y) not in self.dirtyCellsDic:
                self.dirtyCellsDic[(x, y)] = True
                count += 1

        # Create Cleaner agents
        for uniqueId in range(numAgents):
            a = CleanerAgent(uniqueId, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (width//2, height//2))

        self.datacollector = DataCollector(
            model_reporters={"Dirty cells":
                             getDirtyCells},
            agent_reporters={"Moves": "moves"})

    def step(self):
        """
        Objective: Represents a step in time of the grid
        Parameters: None
        Return value: None
        """
        # If all cells are cleaned, halt
        if (self.dirtyCells > 0):
            self.numSteps += 1
        else:
            return
        self.datacollector.collect(self)
        self.schedule.step()
