file3 = open('input3.txt','r')
f3 = open('output3.txt','w')

n = int(file3.readline())

st = []
end = []

for i in range(n):
      x = file3.readline().split() 
      st.append(int(x[0]))     
      end.append(int(x[1])) 

for j in range(n):
   for k in range(n-j-1): 
      if end[k] > end[k+1]:
          end[k], end[k+1] = end[k+1], end[k]
          st[k], st[k+1] = st[k+1], st[k]
          
l = []
c = 0

for h in range(n):
      if c <= st[h]:
            c = end[h]
            l.append(f'{st[h]} {end[h]}')
            

f3.write(f'{len(l)}\n')

for o in range(len(l)):
      f3.write(f'{l[o]}\n')

file3.close()
f3.close()