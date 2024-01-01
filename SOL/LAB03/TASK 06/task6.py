def partition(arr,l,h):
        pivot = int(arr[h])
        x = l-1 
        for i in range(l,h):
              if int(arr[i]) <= pivot:
                    x+=1
                    arr[x],arr[i] = arr[i],arr[x]
        arr[x+1],arr[h] = arr[h],arr[x+1]
        return x+1
    
def find(arr,k):   
      i=0
      j=len(arr)-1
      while i<j:
        p=partition(arr,i,j)
        if p == k:
            r=int(arr[p])
            return r-1
        if p > k:
           j=p-1
        else:
           i=p+1     
      return

file6 = open('input6.txt','r')
f6 = open('output6.txt','w')

n = int(file6.readline())

lst = [int(i)for i in file6.readline().split(' ')]

n2 = int(file6.readline())

lst2 = []

for i in range(n2):
      lst2.append(int(file6.readline()))
      

for i in range(n2):
      
      ind = lst2[i]
      kth = find(lst,ind)
      f6.write(f'{str(kth)}\n')



file6.close()
f6.close()