file1b = open('input1b.txt','r')
f1b = open('output1b.txt','w')

v,e = [int(i) for i in file1b.readline().split(' ')]

di = {}

for i in range(v+1):
      di.update({i:[]})
      
for j in range(e):
      st,end,weight = [int(i) for i in file1b.readline().split(' ')]
      di[st].append(str((end,weight)))
 
for h in range(v+1):
      if di[h] == []:
            f1b.write(f'{h} : \n')
      else:
            f1b.write(f'{h} : {" ".join(di[h])} \n')
            
file1b.close()
f1b.close()
            
            
      