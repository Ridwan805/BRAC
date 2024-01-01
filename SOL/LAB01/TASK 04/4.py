file4 = open('input4.txt', 'r')
f4 = open('output4.txt', 'w')

n = int(file4.readline())

trains = []
name = []
time = []


for i in range(n):
      t = file4.readline().strip()
      trains.append(t)
      name.append(t.split()[0])
      time.append(t.split()[-1])
          
for i in range(len(name)):
    for j in range(len(name)-i-1):
        if name[j] > name[j+1]:
            name[j], name[j+1] = name[j+1], name[j]
            trains[j], trains[j+1] = trains[j+1], trains[j]

        if name[j] == name[j+1]:
            if time[j] > time[j+1]:
                time[j], time[j+1] = time[j+1], time[j]
                trains[j], trains[j+1] = trains[j+1], trains[j]

for i in range(n):
    f4.write(f'{trains[i]}\n')
    
f4.close()
file4.close()

      
      