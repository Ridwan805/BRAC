f1a = open("output1a.txt", "w")
f1a.write("Now the file has more content!\n")
file1a = open('input1a.txt', 'r' )
line = file1a.readline()
x = int(line)
for i in range(x):
  num = file1a.readline().strip()
  if int(num)%2 == 0: 
    f1a.writelines(f'{int(num)} is an Even Number\n') 
  else:
    f1a.writelines(f'{int(num)} is an Odd Number\n')
f1a.close()
file1a.close()