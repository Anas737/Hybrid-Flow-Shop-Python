import copy
import random
from StringBuilder import StringBuilder


class Gene:

    def __init__(self, problem, data=None):
        self.currentProblem = problem

        # data is a matrix where rows are machines and columns are centers
        # if the machine 0 will be used by the job in the center 0 then data[center = 0][machine = 0] = 1 else 0

        if data is None:
            self.data = {}
        else:
            self.data = data

        self.jobIndex = 0
        self.center = 0

        # Initialize all directories !
        self.processed = {}
        self.startTimes = {}
        self.endTimes = {}

        for center in range(self.currentProblem.centerCount):
            self.startTimes[center] = 0
            self.endTimes[center] = 0

            self.processed[center] = False

        # Color for the Gant
        self.color = "FFFFFF"

    def IsProcessed(self):
        return all(processed is True for processed in self.processed.values())

    def Clone(self):  # Create a copy of the current object
        # clonedData = self.data.copy(); # Shallow copy # modifying list reflect in the original dictionary
        clonedData = copy.deepcopy(self.data)

        return Gene(self.currentProblem, clonedData)

    def MoveNext(self):  # Move to the next center
        self.center += 1

    def SetJobIndex(self, jobIndex):
        self.jobIndex = jobIndex

    def SetProcessed(self, center, isProcessed):
        self.processed[center] = isProcessed

    def SetStartTime(self, center, time):
        self.startTimes[center] = time

    def SetEndTime(self, center, time):
        self.endTimes[center] = time

    def SetColor(self, color):
        self.color = color

    def GetProcessed(self, center):
        return self.processed[center]

    def GetStartTime(self, center):
        return self.startTimes[center]

    def GetEndTime(self, center):
        return self.endTimes[center]

    def GetCenterMachine(self, center):
        machines = self.data[center]

        for i in range(0, len(machines)):
            if machines[i] == 1:
                return i

        return None

    def RandomGene(self):  # Generate a random gene
        maxMachineCount = max(self.currentProblem.resourcesCount.values())

        for center in range(self.currentProblem.centerCount):
            column = []
            randomIndex = random.randrange(0, self.currentProblem.resourcesCount[center])  # Generate a random index

            for j in range(maxMachineCount):
                column.append(1 if j == randomIndex else 0)

            self.data[center] = column

    def __str__(self):
        strBuilder = StringBuilder()

        strBuilder.AppendLine("************JobIndex = {}************".format(self.jobIndex))
        for center in range(self.currentProblem.centerCount):
            strBuilder.AppendLine("(Center = {}, StartTime = {} , EndTime = {}) | ".format(center,
                                                                                           self.startTimes[center],
                                                                                           self.endTimes[center]))

        maxMachineCount = max(self.currentProblem.resourcesCount.values)

        for machine in range(maxMachineCount):
            line = ""
            for center in range(self.currentProblem.centerCount):
                line += "{} ".format(self.data[center][machine])

            strBuilder.AppendLine(line)

        return str(strBuilder)
