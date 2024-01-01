f2 = open('output2.txt', 'w')
file2 = open('input2.txt', 'r')
y = int(file2.readline())
l = file2.readline().split(' ')


def bubbleSort(arr): 
    
    flag = True
    while flag: 
        flag = False
        for i in range(1,y):    
            if arr[i-1] > arr[i]:  
              arr[i-1], arr[i] = arr[i], arr[i-1]
              flag = True        
    return arr  

n = []
for i in range(y):
  n.append(int(l[i]))       
arr = bubbleSort(n)              
arr2 = ', '.join([str(x) for x in arr])
f2.write(f'{arr2}')
f2.close()
file2.close()  

       
'''The given array must already be sorted to be the best case scenario for the bubble sort.
I'm using a flag to determine if the array is sorted or not. 
If the given array is sorted, there won't be any swapping; we'll be able to tell by our flag after only once traversing the array, 
at which point we'll end the outer loop.
This has an θ(n) time complexity because the array is only traversed once.'''