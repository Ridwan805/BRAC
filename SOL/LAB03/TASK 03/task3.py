def divide(arr):

    if len(arr) > 1:
        mid = len(arr) // 2
        l = arr[:mid]
        r = arr[mid:]

        l, lcount = divide(l)
        r, rcount = divide(r)
        mlst, mcount = sol(l, r)

        return mlst, lcount + rcount + mcount
    else:
        return arr, 0

def sol(a, b):
    mlst = []
    i = 0
    j = 0
    k =0
    invc = 0

    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            mlst.append(a[i])
            i += 1
        else:
            mlst.append(b[j])
            j += 1
            invc += len(a) - i
        k += 1

    while i < len(a):
        mlst.append(a[i])
        i += 1
        k += 1

    while j < len(b):
        mlst.append(b[j])
        j += 1
        k += 1

    return mlst, invc
            
                  
file3 = open('input3.txt','r')
f3 = open('output3.txt','w')    

n = int(file3.readline())

lst = [i for i in file3.readline().split(' ')]   

a,b = divide(lst)


            
f3.write(f'{str(b)}')

file3.close()
f3.close()

      