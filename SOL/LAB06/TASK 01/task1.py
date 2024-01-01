import heapq
def dijkstra(s):
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
                
file1 = open('input1.txt','r')
f1 = open('output1.txt','w')

v,e = [int(i)for i in file1.readline().split(' ')]

visited = [0]*(v+1)
graph = [[]for i in range(v+1)]

for i in range(e):
    f,s,w = [int(i)for i in file1.readline().split(' ')] 
    graph[f].append((s,w))
source = int(file1.readline())

infi = float('inf')

q = [infi for i in range(v+1)]
q[source] = 0

piorq = []


                  
dijkstra(source)

for i in range(1,v+1):
    if q[i] == infi:
      f1.write(f'{-1} ')  
    else:
        f1.write(f'{q[i]} ')  

file1.close()
f1.close()