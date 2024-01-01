def DFS_Traversal(list,source):
    visited[source] = 1
    
    for i in list[source]:
        if visited[i] == 0:              
            DFS_Traversal(list,i)
    stack.append(source)
               
              

file3 = open('input3.txt', 'r')
f3 = open('output3.txt','w')



v,e = [int(i) for i in file3.readline().split(' ')]

graph = [[]for i in range(v+1)]
tgraph = [[]for i in range(v+1)]
visited = [int(0)]*(v+1) 
stack =[]
g = []

for i in range(e):
    f,s = [int(i)for i in file3.readline().split(' ')]
    graph[f].append(s)
    tgraph[s].append(f)



DFS_Traversal(graph,1)

g = stack
g.reverse()
stack = []
visited = [int(0)]*(v+1)



for i in range(1,v+1):
    if visited[i] == 0:
        DFS_Traversal(tgraph,i)
        for i in stack:
           f3.write(f'{i} ')
        stack = []
        f3.write('\n')

file3.close()
f3.close()



