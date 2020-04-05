__author__ = "EL BOUKHARI & EL AATABI"

import time
import os
from os import listdir
from os.path import isfile, join
from colr import color

from StringBuilder import StringBuilder
from Metaheuristic.Problem import Problem
from Metaheuristic.Individual import Individual
from Metaheuristic.GAlgorithm import GAlgorithm

from Heuristic.Heuristic import Solve as HeuristiqueSolve


def main():
    # Start screen
    strBuilder = StringBuilder()

    # Algorithme
    strBuilder.Append(color("░█▀▀█ █░░ █▀▀▀ █▀▀█ █▀▀█ ░▀░ ▀▀█▀▀ █░░█ █▀▄▀█ █▀▀", fore="bf4e30"))
    strBuilder.AppendLine(color("▒█▄▄█ █░░ █░▀█ █░░█ █▄▄▀ ▀█▀ ░░█░░ █▀▀█ █░▀░█ █▀▀", fore="bf4e30"))
    strBuilder.AppendLine(color("▒█░▒█ ▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀ ░░▀░░ ▀░░▀ ▀░░░▀ ▀▀▀", fore="bf4e30"))
    # Génétique
    strBuilder.AppendLine(color("▒█▀▀█ █▀▀ █▀▀▄ █▀▀ ▀▀█▀▀ ░▀░ █▀▀█ █░░█ █▀▀", fore="c6ccb2"))
    strBuilder.AppendLine(color("▒█░▄▄ █▀▀ █░░█ █▀▀ ░░█░░ ▀█▀ █░░█ █░░█ █▀▀", fore="c6ccb2"))
    strBuilder.AppendLine(color("▒█▄▄█ ▀▀▀ ▀░░▀ ▀▀▀ ░░▀░░ ▀▀▀ ▀▀▀█ ░▀▀▀ ▀▀▀", fore="c6ccb2"))
    strBuilder.AppendLine()

    strBuilder.AppendLine("#" * 8 + " Programme créé par " + "#" * 8)
    strBuilder.AppendLine("• EL BOUKHARI Anas(Métaheuristique & Heuristique)")
    strBuilder.AppendLine("• EL AATABI Btihal(Métaheuristique)")
    strBuilder.AppendLine("• MANNAD Mohamed(Heuristique)")

    strBuilder.AppendLine("#" * 8 + " Encadré par " + "#" * 8)
    strBuilder.AppendLine("• CHAABANE Sondes")
    strBuilder.AppendLine("• BEKRAR Abdelghani")

    # Begin :
    instance_directory = ".//Instances"  # Instances' directory
    instance_files = [file for file in listdir(instance_directory) if
                      isfile(join(instance_directory, file))]  # Instances

    # Display :
    strBuilder.AppendLine("-" * 40)
    strBuilder.AppendLine("➡ Les instances disponibles: ")

    for instance_number in range(len(instance_files)):
        instance_basename = os.path.basename(instance_files[instance_number])
        instance_name = instance_basename.split('.')[0]  # Instance's name

        strBuilder.AppendLine("\t" * 2 + "[{}]: {}".format(instance_number, instance_name))

    strBuilder.AppendLine("➡ Veuillez choisir une instance: ")

    chosen_instance_index = int(input(strBuilder))
    chosen_instance = instance_directory + "//" + instance_files[chosen_instance_index]

    # Algorithm's parameters
    print("➡ Veuillez préciser: ")

    generationCount = int(input("\t" * 2 + "[1] Le nombre de génération: "))
    individualsCount = int(input("\t" * 2 + "[2] Le nombre d'individus de la population: "))
    crossProb = float(input("\t" * 2 + "[3] La probabilité de croisement: "))
    mutationProb = float(input("\t" * 2 + "[4] La probabilité de mutation: "))

    problem = Problem(chosen_instance)  # The problem
    alg = GAlgorithm(generationCount, individualsCount, mutationProb, crossProb)  # Initialization

    start_time = time.time()
    sol = alg.Solve(problem)  # Solve
    execution_time = time.time() - start_time

    print(sol)

    print("➡ Le temps d'execution: {}s".format(execution_time))


main()
