file2a = open('input2a.txt', 'r')
f2a = open('output2a.txt', 'w')

n1 = file2a.readline()
nl1 = file2a.readline().split()
n2 = file2a.readline()
nl2 = file2a.readline().split()

x = []
s = nl1 + nl2 

for i in s:
      x.append(int(i))

x.sort()

for j in x:
      f2a.write(f'{j} ')
      
file2a.close()
f2a.close()