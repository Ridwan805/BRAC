file3 = open('input3.txt','r')
f3 = open('output3.txt','w')


v, e = [int(i)for i in file3.readline().split(' ')]
visited = [0 for i in range(v+1)]
graph = [[]for i in range(v+1)]

for i in range(e):
    f, t = [int(i)for i in file3.readline().split(' ')]
    graph[f].append(t)
    graph[t].append(f)


def DFS_Traversal(graph, source):
    visited[source] = 1
    f3.write(f'{source} ')
    for i in graph[source]:
        if visited[i] == 0:
            DFS_Traversal(graph, i)

source = 1
DFS_Traversal(graph, source)


file3.close()
f3.close()