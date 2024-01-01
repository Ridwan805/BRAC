file4 = open('input4.txt','r')
f4 = open('output4.txt','w')


x = file4.readline().split()
p = int(x[1])
t = int(x[0])


st = []
end = []

for i in range(t):
      a = file4.readline().split()
      st.append(int(a[0]))
      end.append(int(a[1]))
      
for j in range(t):
      for k in range(t-j-1):
            if end[k] > end[k+1]:
                  end[k],end[k+1] = end[k+1], end[k]
                  st[k],st[k+1] = st[k+1], st[k]


tup = []
for h in range(t):
      tup.append((st[h],end[h]))
      
lcur = [0]*p
total=0
can=[]

for i in range(t):
    for j in range(p):
        for k in range(i,t):
            if tup[k][0] == lcur[j] and i not in can:
                lcur[j] = tup[i][1]
                total+=1
                can.append(i)
                break
            
        if tup[i][0] > lcur[j] and i not in can:
            lcur[j] = tup[i][1]
            total+=1
            can.append(i)            
            break

f4.write(f'{total}')
f4.close()
file4.close()
                             


            
            
      

      
