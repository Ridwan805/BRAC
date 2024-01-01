def max(arr):
      if len(arr) <= 1:
            return arr
      else:
            mid = len(arr)//2
            l = max(arr[:mid])
            r = max(arr[mid:])
            return findmax(l,r)

def findmax(l,r):
      if int(l[0]) > int(r[0]):
            return l
      else:
            return r
      
file2 = open('input2.txt','r')
f2 = open('output2.txt','w')

n = file2.readline()

lst = file2.readline().split()

x = max(lst)

f2.write(f'{x[0]}')

file2.close()
f2.close()
