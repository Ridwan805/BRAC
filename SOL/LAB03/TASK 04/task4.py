def divide(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        l = arr[:mid]
        r = arr[mid:]

        divide(l)
        divide(r)

        i = 0
        j = 0
        k = 0

        while i < len(l) and j < len(r):
            if l[i] < r[j]:
                arr[k] = l[i]
                i += 1
            else:
                arr[k] = r[j]
                j += 1
            k += 1

        while i < len(l):
            arr[k] = l[i]
            i += 1
            k += 1

        while j < len(r):
            arr[k] = r[j]
            j += 1
            k += 1

        return arr

    else:
      return arr


def squaremax(arr):
    arr = divide(arr)
    max = arr[len(arr)-1]
    msumm = -99999
    if arr[0] > 0:
        for i in arr:
            if i**2 + max > msumm:
                msumm = i**2 + max
    else:
        for i in arr:
            if i < 0:
                if i**2 + max > msumm:
                    msumm = i**2 + max
                if i + max**2 > msumm:
                    msumm = i + max**2
    return msumm

file4 = open('input4.txt','r')
f4 = open('output4.txt','w')    

n = int(file4.readline())

lst = [int(i) for i in file4.readline().split(' ')]   

                        
y = squaremax(lst)

f4.write(f'{str(y)}')
f4.close()
file4.close()