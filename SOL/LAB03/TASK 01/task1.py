def mergesort(arr):
      if len(arr) <= 1:
            return arr
      else:
            mid = len(arr)//2
            l = mergesort(arr[:mid])
            r = mergesort(arr[mid:])
            return merge(l,r)

def merge(a,b):
      x,y = 0,0
      c = []
      l = len(a) + len(b)
      for i in range(l):
            if x < len(a) and y < len(b):
                  if int(a[x]) < int(b[y]):
                        c.append(a[x])
                        x += 1
                  else:
                        c.append(b[y])
                        y += 1
            else:
                  if x < len(a):
                        c.append(a[x])
                        x += 1
                  else:
                        c.append(b[y])
                        y+= 1 
      return c

file1 = open('input1.txt','r')
f1 = open('output1.txt','w')

n = file1.readline()

lst = file1.readline().split()

x = mergesort(lst)

f1.write(f'{" ".join(x)}')

file1.close()
f1.close()

