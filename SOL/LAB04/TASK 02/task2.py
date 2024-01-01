file2 = open('input2.txt','r')
f2 = open('output2.txt','w')


v, e  = [int(i) for i in file2.readline().split(' ')]

visited = [0 for i in range(v+1)]

graph = [[]for i in range(v+1)]

for i in range(e):
    f, t = [int(i) for i in file2.readline().split(' ')]
    graph[f].append(t)
    graph[t].append(f)

def BFS_Traversal(graph, source):
    queue = []
    queue.append(source)
    visited[source] = 1

    while queue:
        temp = queue.pop(0)
        f2.write(f'{temp} ')

        for i in graph[temp]:
            if visited[i] == 0:
                visited[i] = 1
                queue.append(i)

source = 1
BFS_Traversal(graph, source)



file2.close()
f2.close()




