def partition(arr,l,h):
      pivot = arr[h]
      x = l - 1
      for i in range(l,h):
            if arr[i] <= pivot:
                  x+=1
                  arr[x],arr[i] = arr[i],arr[x]
      arr[x+1],arr[h] = arr[h],arr[x+1]
      return x+1
def quicksort(a, l, h):
      if l < h:
            p = partition(a,l,h)
            quicksort(a,l,p-1)
            quicksort(a,p+1,h)
      return a
            
file5 = open('input5.txt','r')
f5 = open('output5','w')

n = int(file5.readline())

lst = [int(i)for i in file5.readline().split(' ')]

nlst = quicksort(lst,0,n-1)


for k in range(n):
      f5.write(f'{str(nlst[k])} ')

file5.close()
f5.close()