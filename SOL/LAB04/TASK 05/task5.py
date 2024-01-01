file5 = open('input5.txt','r')
f5 = open('output5 .txt','w')


v, e, dest = [int(i)for i in file5.readline().split(' ')]
visited = [0 for i in range(v+1)]
level = [0 for i in range(v+1)]
parent = [0 for i in range(v+1)]
graph = [[]for i in range(v+1)]

for i in range(e):
    f, t = [int(i)for i in file5.readline().split(' ')]
    graph[f].append(t)
    graph[t].append(f)

def BFS_Traversal(graph, source):
    queue = []
    queue.append(source)
    visited[source] = 1
    parent[source] = source

    while queue:
        temp = queue.pop(0)
        for x in graph[temp]:
            if visited[x] == 0:
                visited[x] = 1
                level[x] = level[temp] + 1
                parent[x] = temp
                queue.append(x)

            if x == dest:
                break

source = 1
BFS_Traversal(graph, source)

f5.write(f"Time : {level[dest]}\n")

final = []
while True:
    final.append(dest)
    if dest == source:
        break
    dest = parent[dest]


'''while dest != source:
    final.append(dest)
    dest = parent[dest]
final.append(dest)'''
    
final.reverse()
f5.write('Shortest Path: ')
for x in final:
    f5.write(f'{x} ')

f5.close()
file5.close()