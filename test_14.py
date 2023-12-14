import math
i = 0
while i < 1000000000:
    if (i%100000 == 0):
        print(f'{math.floor(i/100000)}st 100k')
    i+=1
print('finished')