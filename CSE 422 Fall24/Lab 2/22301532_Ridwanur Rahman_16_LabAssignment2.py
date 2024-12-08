#Task1

import random
file = open('input.txt', 'r')
f_line = file.readline().split()
output = open('output.txt','w')

def population(n, size):
  chromo= ""
  temp = size
  population=[]
  while n != 0:
    while temp != 0:
      chromo += (random.choice('01'))
      temp -= 1
    population.append(chromo)
    n -= 1
    chromo = ""
    temp = size
  return population

def check_fitness(slots,N,T):
    
    overlap = 0 
    consistency = 0

    each_slot = [slots[i * N:(i + 1) * N] for i in range(T)]
    #for overlap
    for es in each_slot:
        scheduled = es.count('1') 
        overlap += scheduled - 1
    #for consistency
    repeated_c = []
    for i in range(T):
        repeated_n = [k[i] for k in each_slot]
        repeated_c.append(repeated_n)
        
    for j in repeated_c:
        
        n = j.count(1)
        consistency += abs(n-1)

    fitness = -(overlap+consistency)
    
    return fitness

def parent_selection(popu):
  total = 0
  for i in popu.values():
    total += i
  total = abs(total)
  selected = []

  for par,fit in popu.items():
      
      prob = abs(fit/total)
      selected.append((round(prob,4),par))
  selected = sorted(selected, reverse= True)
  return selected[0][1] , selected[1][1]

def crossover(p1,p2):
  crossover_point = random.randint(0,len(p1)-1)
  c1 = p1[:crossover_point] + p2[crossover_point:]
  c2 = p2[:crossover_point] + p1[crossover_point:]
  return c1,c2

def mutation(c1,c2):
  fid = random.randint(0,len(c1)-1)
  sid = random.randint(0,len(c2)-1)

  nc1 = ''
  nc2 = ''
  if  c1[fid] == '0':
    nc1 += c1[:fid] + '1' + c1[fid+1:] 
  else:
    nc1 += c1[:fid] + '0' + c1[fid+1:] 
  
  if c2[sid] == '0':
    nc2 += c2[:sid] + '1' + c2[sid+1:]
  else:
    nc2 += c2[:sid] + '0' + c2[sid+1:]
  
  return nc1 , nc2

def  GA(population_size,N,T,generation):
  len_chromo = N*T
  populate = population(population_size, len_chromo)
  all = {}
  for i in populate:
    fit = check_fitness(i,N,T)
    all.update({i:fit})
  parent1, parent2 = parent_selection(all)

  best_sol = None
  fittest = float('-inf')
  for i in range(generation):
    offspring1, offspring2 = crossover(parent1,parent2)
    mutatedof1, mutatedof2 = mutation(offspring1,offspring2)

    fit_of1 = check_fitness(mutatedof1,N,T)
    fit_of2 = check_fitness(mutatedof2,N,T)

    if fit_of1 > fittest:
       best_sol = mutatedof1
       fittest = fit_of1
    
    if fit_of2 > fittest:
       best_sol = mutatedof2
       fittest = fit_of2
           

    offspring1 = mutatedof1
    offspring2 = mutatedof2
  
  return best_sol, fittest, populate



courses = int(f_line[0])
timeslots = int(f_line[1])
# l_chromo = courses * timeslots
if courses > timeslots:
   output.write('Number of courses should be less than or equal to Timeslots')

else:
  output.write('Task1\n')
  sol, fittest, populat = GA(300,courses,timeslots,150)
  output.write(f'{sol}\n{fittest}\n')

#Task2 

  p1, p2 = random.choice(populat), random.choice(populat)
  x1 = random.randint(0,len(p1)-1)
  x2 = random.randint(0,len(p1)-1)

  cross1 = p1[:x1] + p2[x1:x2] + p1[x2:]
  cross2 = p2[:x1] + p1[x1:x2] + p2[x2:]

  output.write('Task2\n')
  output.write(f'Here the crossover point are {x1} and {x2} and The parent are {p1} and {p2} and the crossover will be \n{cross1}\n{cross2}\n')




