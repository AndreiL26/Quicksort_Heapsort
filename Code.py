# Written by Andrei Teodor Lazar -> UCL 2019
# Student Number: 18009942

import matplotlib.pyplot as plt
import time
import sys
import random
import statistics
sys.setrecursionlimit(1000000)

numberOfRuns = 10
inputSizes = [10**5, 2*10**5, 4*10**5, 8*10**5, 16*10**5, 32*10**5, 64*10**5, 10**7]

crt_quickSortComparisons = 0 
crt_heapSortComparisons = 0
crt_heapSortSwaps = 0
crt_quickSortSwaps = 0

quickSortAverageComparisons = [0.0] * len(inputSizes)
quickSortAverageSwaps = [0.0] * len(inputSizes)
quickSortAverageSum = [0.0] * len(inputSizes)
heapSortAverageSwaps = [0.0] * len(inputSizes)
heapSortAverageComparisons = [0.0] * len(inputSizes)
heapSortAverageSum = [0.0] * len(inputSizes)

quickSortComparisonsDeviation = [0.0] * len(inputSizes)
quickSortSwapsDeviation = [0.0] * len(inputSizes)
quickSortSumDeviation = [0.0] * len(inputSizes)
heapSortSwapsDeviation = [0.0] * len(inputSizes)
heapSortComparisonsDeviation = [0.0] * len(inputSizes)
heapSortSumDeviation = [0.0] * len(inputSizes)

quickSortAverageTimes = [0.0] * len(inputSizes)
heapSortAverageTimes = [0.0] * len(inputSizes)
quickSortTimesDeviation = [0.0] * len(inputSizes)
heapSortRunningTimesDeviation = [0.0] * len(inputSizes)

heapSortAllRunsComparisons = [[0] * numberOfRuns for i in range(len(inputSizes))]
heapSortAllRunsSwaps = [[0] * numberOfRuns for i in range(len(inputSizes))]
heapSortAllRunsSum = [[0] * numberOfRuns for i in range(len(inputSizes))]
heapSortAllRunsTimes = [[0] * numberOfRuns for i in range(len(inputSizes))]
quickSortAllRunsComparisons = [[0] * numberOfRuns for i in range(len(inputSizes))]
quickSortAllRunsSwaps = [[0] * numberOfRuns for i in range(len(inputSizes))]
quickSortAllRunsSum = [[0] * numberOfRuns for i in range(len(inputSizes))]
quickSortAllRunsTimes = [[0] * numberOfRuns for i in range(len(inputSizes))]

aux = []
array = []
filename = "/mnt/c/Users/40726/Desktop/run"

plt.rcParams.update({'font.size': 16})
def partition (array, left, right):
    global crt_quickSortComparisons
    global crt_quickSortSwaps
    pivot = array[right]
    i = left
    for j in range (left, right):
        crt_quickSortComparisons += 1
        if (array[j] < pivot):
            array[i], array[j] = array[j], array[i]
            crt_quickSortSwaps += 1
            i += 1
    array[i], array[right] = array[right], array[i]
    crt_quickSortSwaps += 1
    return i

def quickSort (array, left, right):
    if (left < right):
        q = partition (array, left, right)
        quickSort (array, left, q-1)
        quickSort (array, q+1, right)

def less (i, j, array):
    if ((i >= len(array)) or (j >= len(array))):
        return False
    if (array[i] < array[j]):
        return True
    return False

def sink (array, k, n):
    global crt_heapSortComparisons 
    global crt_heapSortSwaps
    while (2 * k <= n):
        j = 2 * k
        if (j < n and less(j, j + 1, array)):
            crt_heapSortComparisons += 1
            j += 1
        crt_heapSortComparisons += 1    
        if (not(less(k, j, array))):
            break
        array[k], array[j] = array[j], array[k]
        crt_heapSortSwaps += 1
        k = j

def heapSort (array):
    global crt_heapSortSwaps
    n = len(array) - 1
    for k in range (n//2 , 0, -1):
        sink (array, k , n)
    
    while (n > 1):
        array[1], array[n] = array[n], array[1]
        crt_heapSortSwaps += 1
        n -= 1
        sink (array, 1, n)

def runForInput (inputSize, ix):
    global crt_quickSortComparisons
    global crt_heapSortComparisons
    global crt_quickSortSwaps
    global crt_heapSortSwaps
    global experimentNumber
    
    array = []
    for i in range (0, inputSize):
        array.append(random.randint(1,10 ** 12))

    aux = array.copy()
    aux.append(0)
    for i in range (len(aux) - 1, 0, -1):
        aux[i] = aux[i-1] 
    aux[0] = -1

    start = time.time()
    quickSort(array, 0, len(array) - 1)
    end = time.time()
    quickSortRunningTimes.append(end-start)

    start = time.time()
    heapSort(aux)
    end = time.time()
    heapSortTimes.append(end-start) 

    heapSortComparisons.append(crt_heapSortComparisons)
    heapSortSwaps.append(crt_heapSortSwaps)
    heapSortSum.append(crt_heapSortSwaps + crt_heapSortComparisons)

    quickSortComparisons.append(crt_quickSortComparisons)
    quickSortSwaps.append(crt_quickSortSwaps)
    quickSortSum.append(crt_quickSortComparisons + crt_quickSortSwaps)

    heapSortAllRunsComparisons[ix][experimentNumber] += crt_heapSortComparisons
    heapSortAllRunsSwaps[ix][experimentNumber] += crt_heapSortSwaps
    heapSortAllRunsSum[ix][experimentNumber] += crt_heapSortComparisons + crt_heapSortSwaps

    quickSortAllRunsComparisons[ix][experimentNumber] += crt_quickSortComparisons
    quickSortAllRunsSwaps[ix][experimentNumber] += crt_quickSortSwaps
    quickSortAllRunsSum[ix][experimentNumber] += crt_quickSortComparisons + crt_quickSortSwaps

    heapSortAllRunsTimes[ix][experimentNumber] = heapSortAllRunsTimes[ix][experimentNumber] + heapSortTimes[ix]
    quickSortAllRunsTimes[ix][experimentNumber] += quickSortRunningTimes[ix]

def plotRunGraphs():
    for i in range(len(inputSizes)):
        inputSizes[i] = inputSizes[i]//(10**4)
        heapSortSum[i] = heapSortSum[i]//(10**6)
        quickSortSum[i] = quickSortSum[i]//(10**6)

    plt.figure(1,figsize=(12,12))
    plt.plot(inputSizes, quickSortRunningTimes, color='red', label='Quicksort')
    plt.plot(inputSizes, heapSortTimes, color='blue', label='Heapsort')
    plt.xlabel('Input Size (in tens of thousands) ')
    plt.ylabel('Running Time (seconds)')
    plt.title("Quicksort with right pivot vs Heapsort running time")
    plt.legend()
    plt.savefig(filename + (str)(experimentNumber) + "_runningTime.png")

    plt.figure(2,figsize=(12,12))
    plt.plot(inputSizes, quickSortSum, color='red', label='Quicksort')
    plt.plot(inputSizes, heapSortSum, color='blue', label='Heapsort')
    plt.xlabel('Input Size (in tens of thousands) ')
    plt.ylabel('Number of comparisons and swaps (in millions)')
    plt.title("Quicksort with right pivot vs Heapsort comparisons and swaps")
    plt.legend()
    plt.savefig(filename + (str)(experimentNumber) + "_comparisons.png")
    plt.close('all')

def runExperiment(experimentNumber):
    global crt_quickSortComparisons
    global crt_quickSortSwaps
    global crt_heapSortComparisons
    global crt_heapSortSwaps

    crt_quickSortComparisons = 0
    crt_quickSortSwaps = 0
    crt_heapSortComparisons = 0
    crt_heapSortSwaps = 0
    ix = 0
    for i in inputSizes:
        runForInput(i, ix)
        ix += 1
    plotRunGraphs()
    
def plotAverageGraphs():
    plt.figure(1,figsize=(12,12))
    plt.plot(inputSizes, quickSortAverageTimes, color='red', label='Quicksort')
    plt.plot(inputSizes, heapSortAverageTimes, color='blue', label='Heapsort')
    for ix in range (len(inputSizes)):
        aux = inputSizes[ix]
        a = quickSortAverageTimes[ix] - quickSortTimesDeviation[ix]
        b = quickSortAverageTimes[ix] + quickSortTimesDeviation[ix]
        c = heapSortAverageTimes[ix] - heapSortRunningTimesDeviation[ix]
        d = heapSortAverageTimes[ix] + heapSortRunningTimesDeviation[ix]
        z = [c, d]
        y = [a, b]
        x1 = [aux, aux]
        x2 = [aux-0.5, aux-0.5]
        plt.plot(x1,y, color='red')
        plt.plot(x2,z, color='blue')
    plt.xlabel('Input Size (in tens of thousands) ')
    plt.ylabel('Average Running Time (seconds)')
    plt.title("Quicksort with right pivot vs Heapsort average running time")
    plt.legend()
    plt.savefig(filename + "_averageTime.png")

    for i in range(len(inputSizes)):
        quickSortAverageComparisons[i] = quickSortAverageComparisons[i]//(10**4)
        quickSortAverageSwaps[i] =  quickSortAverageSwaps[i]//(10**4)
        quickSortAverageSum[i] = quickSortAverageSum[i]//(10**6)

        heapSortAverageComparisons[i] = heapSortAverageComparisons[i]//(10**4)
        heapSortAverageSwaps[i] = heapSortAverageSwaps[i]//(10**4)
        heapSortAverageSum[i] = heapSortAverageSum[i]//(10**6)

    plt.figure(2,figsize=(12,12))
    plt.plot(inputSizes, quickSortAverageComparisons, color='red', label='Quicksort')
    plt.plot(inputSizes, heapSortAverageComparisons, color='blue', label='Heapsort')
    for ix in range (len(inputSizes)):
        aux = inputSizes[ix]
        a = quickSortAverageComparisons[ix] - quickSortComparisonsDeviation[ix]
        b = quickSortAverageComparisons[ix] + quickSortComparisonsDeviation[ix]
        c = heapSortAverageComparisons[ix] - heapSortComparisonsDeviation[ix]
        d = heapSortAverageComparisons[ix] + heapSortComparisonsDeviation[ix]
        z = [c, d]
        y = [a, b]
        x1 = [aux, aux]
        plt.plot(x1,y, color='red')
        plt.plot(x2,z, color='blue')

    plt.xlabel('Input Size (in tens of thousands) ')
    plt.ylabel('Average Number of comparisons (in tens of thousands)')
    plt.title("Quicksort with right pivot vs Heapsort average comparisons")
    plt.legend()
    plt.savefig(filename + "_averageComparisons.png")

    plt.figure(3,figsize=(12,12))
    plt.plot(inputSizes, quickSortAverageSwaps, color='red', label='Quicksort')
    plt.plot(inputSizes, heapSortAverageSwaps, color='blue', label='Heapsort')
    for ix in range (len(inputSizes)):
        aux = inputSizes[ix]
        a = quickSortAverageSwaps[ix] - quickSortSwapsDeviation[ix]
        b = quickSortAverageSwaps[ix] + quickSortSwapsDeviation[ix]
        c = heapSortAverageSwaps[ix] - heapSortSwapsDeviation[ix]
        d = heapSortAverageSwaps[ix] + heapSortSwapsDeviation[ix]
        z = [c, d]
        y = [a, b]
        x1 = [aux, aux]
        plt.plot(x1,y, color='red')
        plt.plot(x2,z, color='blue')

    plt.xlabel('Input Size (in tens of thousands) ')
    plt.ylabel('Average Number of swaps (in tens of thousands)')
    plt.title("Quicksort with right pivot vs Heapsort average swaps")
    plt.legend()
    plt.savefig(filename + "_averageSwaps.png") 

    plt.figure(4,figsize=(12,12))
    plt.plot(inputSizes, quickSortAverageSum, color='red', label='Quicksort')
    plt.plot(inputSizes, heapSortAverageSum, color='blue', label='Heapsort')
    for ix in range (len(inputSizes)):
        aux = inputSizes[ix]
        a = quickSortAverageSum[ix] - quickSortSumDeviation[ix]
        b = quickSortAverageSum[ix] + quickSortSumDeviation[ix]
        c = heapSortAverageSum[ix] - heapSortSumDeviation[ix]
        d = heapSortAverageSum[ix] + heapSortSumDeviation[ix]
        z = [c, d]
        y = [a, b]
        x1 = [aux, aux]
        plt.plot(x1,y, color='red')
        plt.plot(x2,z, color='blue')

    plt.xlabel('Input Size (in tens of thousands) ')
    plt.ylabel('Average Number of comparisons and swaps (in millions)')
    plt.title("Quicksort with right pivot vs Heapsort average comparisons and swaps")
    plt.legend()
    plt.savefig(filename + "_averageSum.png")

    plt.close('all')

def computeAveragesandDeviations(): 

    for i in range (len(inputSizes)):
        quickSortComparisonsDeviation[i] = statistics.stdev(quickSortAllRunsComparisons[i])/(10**4)
        quickSortSwapsDeviation[i] = statistics.stdev(quickSortAllRunsSwaps[i])/(10**4)
        quickSortSumDeviation[i] = statistics.stdev(quickSortAllRunsSum[i])/(10**6)
        quickSortTimesDeviation[i] = statistics.stdev(quickSortAllRunsTimes[i])

        heapSortComparisonsDeviation[i] = statistics.stdev(heapSortAllRunsComparisons[i])/(10**4)
        heapSortSwapsDeviation[i] = statistics.stdev(heapSortAllRunsSwaps[i])/(10**4)
        heapSortSumDeviation[i] = statistics.stdev(heapSortAllRunsSum[i])/(10**6)
        heapSortRunningTimesDeviation[i] = statistics.stdev(heapSortAllRunsTimes[i])

        for j in range (numberOfRuns):
            quickSortAverageComparisons[i] += quickSortAllRunsComparisons[i][j]/numberOfRuns
            quickSortAverageSwaps[i] += quickSortAllRunsSwaps[i][j]/numberOfRuns
            quickSortAverageSum[i] += quickSortAllRunsSum[i][j]/numberOfRuns

            heapSortAverageComparisons[i] += heapSortAllRunsComparisons[i][j]/numberOfRuns
            heapSortAverageSwaps[i] += heapSortAllRunsSum[i][j]/numberOfRuns
            heapSortAverageSum[i] += heapSortAllRunsSum[i][j]/numberOfRuns

            heapSortAverageTimes[i] += heapSortAllRunsTimes[i][j]/numberOfRuns
            quickSortAverageTimes[i] += quickSortAllRunsTimes[i][j]/numberOfRuns

    
    f = open("data.txt", "w")
    
    f.write("Heapsort average sum:\n")
    for i in range (len(inputSizes)):
        f.write((str)(heapSortAverageSum[i]))
        f.write("\n")

    f.write("Heapsort sum deviation:\n")
    for i in range (len(inputSizes)):
        f.write((str)(heapSortSumDeviation[i]))
        f.write("\n")
    
    f.write("Quicksort average sum:\n")
    for i in range (len(inputSizes)):
        f.write((str)(quickSortAverageSum[i]))
        f.write("\n")

    f.write("Quicksort sum deviation:\n")
    for i in range (len(inputSizes)):
        f.write((str)(quickSortSumDeviation[i]))
        f.write("\n")


    f.write("Heapsort average time:\n")
    for i in range (len(inputSizes)):
        f.write((str)(heapSortAverageTimes[i]))
        f.write("\n")
    
    f.write("Heapsort time deviation:\n")
    for i in range (len(inputSizes)):
        f.write((str)(heapSortRunningTimesDeviation[i]))
        f.write("\n")

    f.write("Quicksort average time:\n")
    for i in range (len(inputSizes)):
        f.write((str)(quickSortAverageTimes[i]))
        f.write("\n")

    f.write("Quicksort time deviation:\n")
    for i in range (len(inputSizes)):
        f.write((str)(quickSortTimesDeviation[i]))
        f.write("\n")    



for experimentNumber in range (0, numberOfRuns):
    quickSortComparisons = []
    quickSortSwaps = []
    quickSortSum = []
    quickSortRunningTimes = []
    heapSortComparisons = []
    heapSortSwaps = []
    heapSortTimes = []
    heapSortSum = []
    inputSizes = [10**5, 2*10**5, 4*10**5, 8*10**5, 16*10**5, 32*10**5, 64*10**5, 10**7]
    runExperiment(experimentNumber)

computeAveragesandDeviations()
plotAverageGraphs()