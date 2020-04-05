__author__ = "EL BOUKHARI & MANNAD"
from Metaheuristic.Gene import Gene
from Metaheuristic.Individual import Individual


def Solve(problem):
    ncenter = problem.centerCount
    njobs = problem.jobCount

    # Codage centre 1

    center1 = {}

    for jobIndex in range(njobs):
        center1[jobIndex] = problem.GetJobDuration(0, jobIndex)

    n = njobs - 1
    # Codage d'heuristique pour le centre 1
    codage = {}

    sorted_dict = Sort(center1)  # dictionnaire ordonné

    keys = list(sorted_dict.keys())

    while keys:
        codage[keys[0]] = sorted_dict[keys[0]]
        codage[keys[-1]] = sorted_dict[keys[-1]]
        if len(keys) >= 2:
            keys.remove(keys[0])
            keys.remove(keys[-1])
        elif len(keys) == 1:
            keys.remove(keys[0])

    """
    codage c'est le dictionnaire qui represente l'ordre resultant
    par l'heuristique dont la cle et l'indice d'un element et le valeur est
    la durée de l'operation dans le centre
    ex: codage[indiceJob, durée]
    """

    # Application de l'heuristique
    data = {}
    machines = {}
    startTimes = {}
    endTimes = {}

    # Code du premier centre
    data[0] = {}
    machines[0] = {}
    startTimes[0] = {}
    endTimes[0] = {}

    maxMachineCount = max(problem.resourcesCount.values())
    machinesHistory = []

    for machine in range(problem.GetResourceCount(0)):
        machinesHistory.append(0)

    for jobIndex in codage:
        data[0][jobIndex] = []

        currentMachine = GetAvailableMachine(machinesHistory)

        machines[0][jobIndex] = currentMachine
        startTimes[0][jobIndex] = machinesHistory[currentMachine]

        endTime = machinesHistory[currentMachine] + codage[jobIndex]
        endTimes[0][jobIndex] = endTime
        machinesHistory[currentMachine] = endTime

        '''print("currentMachine: {}, startTime: {}, operationTime: {}, endTime: {}".format(currentMachine,
                                                                                         startTimes[0][jobIndex],
                                                                                         problem.GetJobDuration(0, jobIndex),
                                                                                         endTimes[0][jobIndex]))'''

        for machine in range(maxMachineCount):
            data[0][jobIndex].append(1 if machine == currentMachine else 0)

    # Code pour les centres suivants

    for center in range(1, ncenter):
        #print("-" * 8 + str(center) + "-" * 8)

        machinesHistory.clear()
        for machine in range(problem.GetResourceCount(center)):
            machinesHistory.append(0)

        data[center] = {}
        machines[center] = {}
        startTimes[center] = {}
        endTimes[center] = {}

        codage = Sort(endTimes[center - 1])
        for jobIndex in codage:
            data[center][jobIndex] = []

            currentMachine = GetAvailableMachine(machinesHistory, endTimes[center - 1][jobIndex])

            machines[center][jobIndex] = currentMachine
            startTime = machinesHistory[currentMachine] + max(
                endTimes[center - 1][jobIndex] - machinesHistory[currentMachine], 0)
            startTimes[center][jobIndex] = startTime

            endTime = startTimes[center][jobIndex] + problem.GetJobDuration(center, jobIndex)
            endTimes[center][jobIndex] = endTime
            machinesHistory[currentMachine] = endTime

            '''print("currentMachine: {}, startTime: {}, operationTime: {}, endTime: {}".format(currentMachine,
                                                                                             startTimes[center][
                                                                                                 jobIndex],
                                                                                             problem.GetJobDuration(
                                                                                                 center, jobIndex),
                                                                                             endTimes[center][
                                                                                                 jobIndex]))'''

            for machine in range(maxMachineCount):
                data[center][jobIndex].append(1 if machine == currentMachine else 0)

    # Create individual
    genesData = {}
    for center in data:
        for jobIndex in data[center]:
            if jobIndex not in genesData.keys():
                genesData[jobIndex] = []

            genesData[jobIndex].append(data[center][jobIndex])

    individual = Individual(problem)

    # Unordered genes
    for jobIndex in range(njobs):
        gene = Gene(problem, genesData[jobIndex])
        individual.AddGene(gene)

    # Ordered genes
    for center in data:
        for jobIndex in data[center]:
            gene = individual.GetGeneByIndex(jobIndex)

            gene.SetProcessed(center, True)
            gene.SetStartTime(center, startTimes[center][jobIndex])
            gene.SetEndTime(center, endTimes[center][jobIndex])

            machine = machines[center][jobIndex]
            individual.AddOrderedGene(center, machine, gene)

    individual.SetAllJobIndex()
    # Last center
    lastGeneTime = 0

    for gene in individual.genes:
        x = gene.GetEndTime(ncenter - 1)
        if x > lastGeneTime:
            lastGeneTime = x

    individual.SetMakespan(lastGeneTime)

    return individual

    # Fonction pour ordnner une liste sous forme de dictionnaire


def Sort(dict):
    r = {}

    for i in dict:
        minIndex = 0
        minValue = 9999

        for j in dict:
            if dict[j] < minValue and j not in r.keys():
                minIndex = j
                minValue = dict[j]

        r[minIndex] = minValue

    return r


def GetAvailableMachine(availableMachines, endTime = 0):
    for machine in range(len(availableMachines)):
        if availableMachines[machine] < endTime:
            return machine

    minValue = min(availableMachines)
    return availableMachines.index(minValue)
