file2b = open('input2b.txt','r')
f2b = open('output2b.txt','w')

n1 = int(file2b.readline()) 
nl1 = file2b.readline().split()  
n2 = int(file2b.readline())
nl2 = file2b.readline().split()  

sortl = []
i = 0
j = 0

while i < n1 and j < n2:
      if int(nl1[i]) < int(nl2[j]):
            sortl.append((nl1[i]))
            i += 1
      elif int(nl1[i]) > int(nl2[j]):
            sortl.append((nl2[j]))
            j+= 1
      elif  int(nl1[i]) == int(nl2[j]):
           sortl.append((nl1[i]))
           sortl.append((nl1[i]))
           i += 1
           j += 1 
           
if i != n1:
      sortl += nl1[i:]
if j != n2:
      sortl += nl2[j:]  
      
for k in sortl:
      f2b.write(f'{k} ')
    
           