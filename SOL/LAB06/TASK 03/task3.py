def path(a):
    if lead[a] == a:
        return a
    return path(lead[a])


def union(a, b):
    u = path(a)
    v = path(b)
    if u != v:
        lead[u] = v
        team[v] += team[u]

    f3.write(f'{team[v]} \n')

file3 = open('input3.txt','r')
f3 = open('output3.txt','w')

v, e = [int(i)for i in file3.readline().split(' ')]
lead = [ i for i in range(v) ]
team = [ 1 for i in range(v) ]
for i in range(e):
    a, b = [int(i)for i in file3.readline().split(' ')]
    union(a, b)

file3.close()
f3.close()