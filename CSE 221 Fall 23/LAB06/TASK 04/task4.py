def path(a):
    if rep[a] == a:
        return a
    return path(rep[a])


def union(a, b, c):
    u = path(a)
    v = path(b)
    if u != v:
        rep[u] = v
        return c
    return 0 
        

file4 = open('input4.txt','r')
f4 = open('output4.txt','w')

v,e = [int(i)for i in file4.readline().split(' ')]

g=[]
rep = [i for i in range(v+1)]
weight = 0 
for i in range(e):
    f,s,w = [int(i) for i in file4.readline().split(' ')]
    g.append((w,f,s))
g.sort()

for i in g:
   no = union(i[1],i[2],i[0])
   weight += no 

f4.write(f'{weight}')

file4.close()
f4.close()

        