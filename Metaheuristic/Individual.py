__author__ = "EL BOUKHARI & EL AATABI"
from Metaheuristic.Gene import Gene
from StringBuilder import StringBuilder
from colr import color
import random


class Individual:
    def __init__(self, problem):
        self.currentProblem = problem

        self.makespan = 0  # Fitness
        self.genes = []  # Unordered individual' genes
        self.orderedGenes = {}  # Ordered individual' genes

        # Colors for the Gant
        self.colors = ["FF4040", "8A2BE2", "0000FF", "FF9912",
                       "DC143C", "FFB90F", "FF1493", "00C957",
                       "20B2AA", "8470FF", "00FA9A", "191970",
                       "004225", "8B1C62", "FFF68F", "66CD00",
                       "68838B", "006400", "7A8B8B", "D02090"]

    def IsProcessed(self):
        return all(gene.IsProcessed() for gene in self.genes)

    def AddGene(self, gene):
        geneClone = gene.Clone()

        geneCloneColor = self.colors[random.randrange(0, len(self.colors))]
        self.colors.remove(geneCloneColor)

        geneClone.SetColor(geneCloneColor)

        self.genes.append(geneClone)  # Add the gene's clone

    def AddGenes(self, genes):
        for gene in genes:
            self.AddGene(gene)

    def AddOrderedGene(self, center, machine, gene):
        if center not in self.orderedGenes.keys():
            self.orderedGenes[center] = {}

        if machine not in self.orderedGenes[center].keys():
            self.orderedGenes[center][machine] = []

        self.orderedGenes[center][machine].append(gene)

    def SetAllJobIndex(self):
        for jobIndex in range(len(self.genes)):
            self.genes[jobIndex].SetJobIndex(jobIndex)

    def SetMakespan(self, time):
        self.makespan = time

    def GetGeneByIndex(self, index):
        return self.genes[index]

    def GetMakespan(self):
        return self.makespan

    def RandomIndividual(self):
        for jobIndex in range(self.currentProblem.jobCount):
            gene = Gene(self.currentProblem)
            gene.RandomGene()

            self.AddGene(gene)

        self.SetAllJobIndex()

    def __str__(self):
        strBuilder = StringBuilder()

        for center in range(self.currentProblem.centerCount):
            strBuilder.AppendLine("<{} Center = {} {}>".format('-' * 7, center + 1, '-' * 7))
            for machine in range(self.currentProblem.resourcesCount[center]):
                strBuilder.AppendLine()
                strBuilder.Append("{}{} Machine = {} {} : ".format(" " * 2, '#' * 3, machine + 1, '#' * 3))
                lastGene = None

                if center > 0:
                    strBuilder.Append(" " * self.orderedGenes[center][machine][0].GetEndTime(center - 1))

                geneCount = 0
                for gene in self.orderedGenes[center][machine]:
                    if lastGene is not None:
                        delay = gene.GetStartTime(center) - lastGene.GetEndTime(center)
                        if delay > 0:
                            strBuilder.Append(
                                color("{}".format(" " * (gene.GetStartTime(center) - lastGene.GetEndTime(center))),
                                      fore="000000", back="FFFFFF"))

                    strBuilder.Append(color("{}".format(" " * (gene.GetEndTime(center) - gene.GetStartTime(center))),
                                            fore="000000", back=gene.color))
                    if geneCount == (len(self.orderedGenes[center][machine]) - 1):
                        strBuilder.Append(gene.GetEndTime(center))

                    lastGene = gene
                    geneCount += 1

                if machine < (self.currentProblem.resourcesCount[center] - 1):
                    strBuilder.AppendLine(" ")

            strBuilder.AppendLine("<{} Center = {} {} />".format('-' * 7, center + 1, '-' * 7))

        strBuilder.AppendLine("\033[1m{} Cmax = {} {}\033[0m".format("~" * 20, self.GetMakespan(), "~" * 20))
        return str(strBuilder)
