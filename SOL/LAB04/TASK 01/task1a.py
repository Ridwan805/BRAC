import numpy as np
file1a = open('input1a.txt','r')
f1a = open('output1a.txt','w')

v,e = [int(i) for i in file1a.readline().split(' ')]

mat = np.zeros((v+1,v+1), dtype=int)

for j in range(e):
      st,end,weight = [int(i) for i in file1a.readline().split(' ')]
      mat[st][end] = weight
      
for k in range(v+1):
      for h in range(v+1):
          f1a.write(f'{mat[k][h]} ')
      f1a.write('\n')
      
file1a.close()
f1a.close()  
      
