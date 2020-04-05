__author__ = "EL BOUKHARI & EL AATABI"

import time
import random
from tqdm import tqdm
from collections import OrderedDict
from Metaheuristic.Individual import Individual
from Heuristic.Heuristic import Solve as HeuristicSolve


class GAlgorithm:

    def __init__(self, generationCount, individualsCount, crossProb, mutationProb):
        self.currentProblem = None

        self.generationCount = generationCount
        self.individualCount = individualsCount
        self.crossProb = crossProb
        self.mutationProb = mutationProb

    def Solve(self, problem):
        self.currentProblem = problem

        start_time = time.time()
        heuristic_individual = HeuristicSolve(problem)  # Heuristic individual(solution)
        execution_time = time.time() - start_time  # Heuristic execution time

        print("\033[1m{} La Solution Heuristique: {}\033[0m".format("~" * 15, "~" * 15))
        print(heuristic_individual) # Display heuristic solution
        print("➡ Le temps d'execution: {}s".format(execution_time))
        print("\033[1m{} La Solution Métaheuristique: {}\033[0m".format("~" * 15, "~" * 15))

        population = self.RandomPopulation(problem)  # Generate a random population (genesis)
        population.append(heuristic_individual)  # Insert heuristic individual in population

        self.Evaluation(population)  # Evualate all random individual except heuristic solution(because it's already processed)
        population = self.Selection(population)  # Selection

        for generation in tqdm(range(self.generationCount)):
            for i in range(self.individualCount // 2):

                parent1Index = 0
                parent2Index = 0

                while parent1Index == parent2Index:
                    parent1Index = random.randrange(0, self.individualCount)
                    parent2Index = random.randrange(0, self.individualCount)

                parent1 = population[parent1Index]
                parent2 = population[parent2Index]

                alpha = random.uniform(0, 1)  # Cross probability
                beta = random.uniform(0, 1)  # Mutation probability

                childs = []

                if alpha <= self.crossProb:
                    childs = self.Cross(parent1, parent2)
                else:
                    childs.append(parent1)
                    childs.append(parent2)

                if beta <= self.mutationProb:
                    childs[0] = self.Mutate(childs[0])
                else:
                    childs[1] = self.Mutate(childs[1])

                population.extend(childs)
                self.Evaluation(population)

                population = self.Selection(population)

        return population[0]  # Return the first individual (one of the best solutions)

    def Evaluation(self, population):  # Evaluate individuals

        for individual in population:
            if individual.IsProcessed():  # If the individual has already been processed
                continue  # Skip

            genesToProcess = individual.genes.copy()

            for center in range(self.currentProblem.centerCount):
                processedGenes = {}
                genesInProcess = {}

                lastGenes = {}  # Dictionary where the key is a resource and the value the first job to exit that resource

                while len(genesToProcess) > 0:  # Genes waiting to be processed
                    currentGene = genesToProcess.pop(0)  # Get the first gene in the list
                    requiredMachine = currentGene.GetCenterMachine(center)

                    individual.AddOrderedGene(center, requiredMachine, currentGene)

                    for resource in range(self.currentProblem.resourcesCount[center]):
                        if requiredMachine == resource:
                            delay = 0
                            if resource in lastGenes.keys():
                                if lastGenes[resource] is not None:
                                    delay = lastGenes[resource].GetEndTime(center)
                                    self.Update(center, resource, lastGenes, processedGenes, genesInProcess)

                            lastCenterEndTime = 0 if center == 0 else currentGene.GetEndTime(center - 1)

                            startTime = delay + max(lastCenterEndTime - delay, 0)

                            currentGene.SetStartTime(center, startTime)
                            currentGene.SetEndTime(center,
                                                   startTime + self.currentProblem.GetJobDuration(center,
                                                                                                  currentGene.jobIndex))

                            if requiredMachine not in genesInProcess:
                                genesInProcess[requiredMachine] = []

                            genesInProcess[requiredMachine].append(currentGene)

                    firstGenes = self.GetFirstGenes(center, genesInProcess)

                    lastGenes = firstGenes

                for element in genesInProcess:

                    processedGene = genesInProcess[element][-1]
                    processedGene.SetProcessed(center, True)

                    if element not in processedGenes:
                        processedGenes[element] = []

                    processedGenes[element].append(processedGene)

                genesToProcess = self.GenerateSortedQueue(center, processedGenes)

            # Last center
            lastGeneTime = 0

            for gene in individual.genes:
                x = gene.GetEndTime(self.currentProblem.centerCount - 1)
                if x > lastGeneTime:
                    lastGeneTime = x

            individual.SetMakespan(lastGeneTime)

    def Selection(self, population):

        newPopulation = []
        evaluation = {}

        for individual in population:
            evaluation[individual] = individual.GetMakespan()

        d_ascending = OrderedDict(sorted(evaluation.items(), key=lambda kv: kv[
            1]))  # Ascending ordered dictionary of jobs according to their makespan value

        for individual in d_ascending:
            if len(newPopulation) == self.individualCount:  # To not exceed the population size
                break

            newPopulation.append(individual)

        return newPopulation

    def Cross(self, parent1, parent2):  # 1 point-cross

        childs = []

        parent1Genes = parent1.genes
        parent2Genes = parent2.genes

        i = random.randrange(0, self.currentProblem.jobCount)

        child1 = Individual(self.currentProblem)
        child2 = Individual(self.currentProblem)

        # Child1

        child1.AddGenes(parent1Genes[0: i + 1])
        for gene in parent2Genes:
            if len(child1.genes) == self.currentProblem.jobCount:
                break

            if gene in child1.genes:
                continue

            child1.AddGene(gene)

        # Child2

        child2.AddGenes(parent2Genes[0: i + 1])
        for gene in parent1Genes:
            if len(child2.genes) == self.currentProblem.jobCount:
                break

            if gene in child2.genes:
                continue

            child2.AddGene(gene)

        # SetAllJobIndex
        child1.SetAllJobIndex()
        child2.SetAllJobIndex()

        childs.append(child1)
        childs.append(child2)

        return childs

    def Mutate(self, individual):  # Insertion mutation

        child = Individual(self.currentProblem)

        geneIndex = random.randrange(0, self.currentProblem.jobCount)
        positionIndex = random.randrange(0, self.currentProblem.jobCount)

        while geneIndex == positionIndex:
            positionIndex = random.randrange(0, self.currentProblem.jobCount)

        for i in range(positionIndex):
            if i == geneIndex:
                continue

            child.AddGene(individual.genes[i])

        child.AddGene(individual.genes[geneIndex])

        for i in range(positionIndex, self.currentProblem.jobCount):
            if i == geneIndex:
                continue

            child.AddGene(individual.genes[i])

        child.SetAllJobIndex()

        return child

    def RandomPopulation(self, problem):  # Create a random population

        population = []

        for i in range(self.individualCount):
            individual = Individual(problem)
            individual.RandomIndividual()

            population.append(individual)

        return population

    def Update(self, center, resource, lastGenes, processedGenes, genesInProcess):  # Update list / dictionary

        processedGene = lastGenes[resource]
        if resource not in processedGenes:
            processedGenes[resource] = []

        processedGenes[resource].append(processedGene)
        genesInProcess[resource].remove(processedGene)

    def GetFirstGene(self, center, processedGenes):  # First gene to exit the given center

        firstGeneResource = 0
        firstGene = None

        endTime = 9999

        for resource in processedGenes:
            for gene in processedGenes[resource]:
                if gene.GetEndTime(center) < endTime:
                    firstGene = gene
                    endTime = gene.GetEndTime(center)

                    firstGeneResource = resource

        processedGenes[firstGeneResource].remove(firstGene)

        return firstGene

    def GetFirstGenes(self, center,
                      genesInProcess):  # Dictionary where the key is a resource and the value the first job to exit that resource

        firstGenes = {}

        for resource in genesInProcess:

            firstGene = None
            endTime = 99999
            for gene in genesInProcess[resource]:
                if gene.GetEndTime(center) < endTime:
                    firstGene = gene
                    endTime = gene.GetEndTime(center)

            firstGene.SetProcessed(center, True)
            firstGenes[resource] = firstGene

        return firstGenes

    def GenerateSortedQueue(self, center, processedGenes):
        result = []

        while any(len(processedGenes[key]) > 0 for key in processedGenes):
            firstGene = self.GetFirstGene(center, processedGenes)
            result.append(firstGene)

        return result
