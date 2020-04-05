__author__ = "EL BOUKHARI & EL AATABI"
import os
import csv


class Problem:
    def __init__(self, filePath):
        self.resourcesCount = {}  # Dictionary where key corresponds to the center and value to the number of machines
        self.jobsDuration = {}  # Dictionary where key corresponds to the center and value to a list of operations' duration for each job

        self.filePath = filePath

        # Load file

        rowIndex = 0

        tmpJobsDuration = {}
        tmpResourcesCount = {}

        with open(filePath, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                row = row[0]

                if rowIndex == 0:
                    self.centerCount = int(row) + 1  # Centers' number
                elif rowIndex == 1:
                    self.jobCount = int(row) + 1  # Machines' number
                else:
                    durations = []

                    strs = self.Clean(row.strip().split(' '))  # To remove whitespaces
                    for job in range(self.jobCount):
                        durations.append(int(strs[job]))

                    center = rowIndex - 2  # Because the first and second row are reserved for centers' number and machines' number

                    tmpResourcesCount[center] = int(strs[len(strs) - 1])
                    tmpJobsDuration[center] = durations

                rowIndex += 1

        csvFile.close()

        for center in range(self.centerCount):
            self.resourcesCount[center] = tmpResourcesCount[center]
            self.jobsDuration[center] = tmpJobsDuration[center]

    def GetResourceCount(self, center):  # Return the number of machines for the given center
        return self.resourcesCount[center]

    def GetJobDuration(self, center, jobIndex):  # Return the operation duration for the given center and job
        return self.jobsDuration[center][jobIndex]

    def Clean(self, strs): # Remove whitespaces
        result = []

        for str in strs:
            if str == "" or str == "":
                continue

            result.append(str)

        return result
