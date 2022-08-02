import math
from uvincenty import vincenty

def linearSearch(n, table):
    for i in range(len(table)):
        if table[i][0] == n:
            return i
    return -1

def partition(arr, low, high, column): 
    i = (low-1)         # index of smaller element 
    pivot = arr[high][column]     # pivot 
  
    for j in range(low, high): 
  
        # If current element is smaller than or 
        # equal to pivot 
        if arr[j][column] <= pivot: 
  
            # increment index of smaller element 
            i = i+1
            arr[i], arr[j] = arr[j], arr[i] 
  
    arr[i+1], arr[high] = arr[high], arr[i+1] 
    return (i+1) 
  
# The main function that implements QuickSort 
# arr[] --> Array to be sorted, 
# low  --> Starting index, 
# high  --> Ending index 
  
# Function to do Quick sort 
def quickSort(arr, low, high, column): 
    if len(arr) == 1: 
        return arr 
    if low < high: 
  
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition(arr, low, high, column) 
  
        # Separately sort elements before 
        # partition and after partition 
        quickSort(arr, low, pi-1, column) 
        quickSort(arr, pi+1, high, column)
