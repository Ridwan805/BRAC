import heapq

def dijkstra(s,q):
    visited[s] = 1
    piorq.append(s)

    while piorq:

        temp = heapq.heappop(piorq)
        
        for i in graph[temp]:
            n = i[0]
            we = i[1]
            if visited[n] == 0:
                visited[n] = 1
                        
            if q[temp]+we < q[n]:
                q[n] = q[temp]+we
                heapq.heappush(piorq, n)
    return q


file2 = open('input2.txt','r')
f2 = open('output2.txt','w')

v,e = [int(i)for i in file2.readline().split(' ')]

visited = [0]*(v+1)

graph = [[]for i in range(v+1)]

for i in range(e):
    f,s,w = [int(i)for i in file2.readline().split(' ')] 
    graph[f].append((s,w))
s1,s2 = [int(i)for i in file2.readline().split(' ')] 
infi = float('inf')

q1 = [infi for i in range(v+1)]
q1[s1] = 0

q2 = [infi for i in range(v+1)]
q2[s2] = 0

piorq = []

x = dijkstra(s1,q1)
y = dijkstra(s2,q2)

if len(x) -1 == x.count(infi) or len(y) -1 == y.count(infi):
    f2.write('Impossible')
else:
    for i in range(1,v+1):
        if x[i] == infi:
            x[i] = -1
        if y[i] == infi:
            y[i] = -1
    cn = [0]*(v+1)
    for i in range(1,v+1):
        if x[i] != -1 and y[i] != -1:
            a = max(x[i],y[i])
            cn[i] = a 
    cd = sorted(cn)
    for i in range(v+1):
        if cd[i] != 0:
            f2.write(f'Time: {cd[i]}\nNode: {cn.index(cd[i])}')
            break

file2.close()
f2.close()